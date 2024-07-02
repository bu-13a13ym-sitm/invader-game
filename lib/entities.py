from time import sleep
from math import pow
from threading import Thread
from random import randint as rd
from lib.global_variables import field_width, field_height, refresh_rate, fps, player_graphic, enemy_graphic, item_graphic, effects, sec_to_frame
from lib.maps import ItemMap, BulMap



def scale(n):
    return 27.500 * pow(pow(2, 1/12), n)

class Entity:
    def __init__(self,
                 *,
                 hp=0,
                 width=0,
                 pos=(rd(2, field_width - 3),rd(3, field_height - 3))):
        self.max_hp = hp
        self.hp = hp
        self.width = width
        self.pos = {key : value for key, value in zip(("x", "y"), pos)}
    def get_dam(self, dam = 1):
        if self.hp - dam <= self.max_hp:
            self.hp -= dam
        else:
            self.hp = self.max_hp
    def change_pos(self, new_pos, frame):
        pos = self.pos
        half_width = self.width//2
        if (pos != new_pos) and ((new_pos >= half_width) and (new_pos < field_width - half_width)) and ((frame % (fps // self.vel)) == 0):
            if new_pos > self.pos["x"]:
                self.pos["x"] += 1
            elif new_pos < self.pos["x"]:
                self.pos["x"] -= 1

class Creature(Entity):
    def __init__(self,
                 *,
                 hp=1,
                 width=len(player_graphic),
                 pos=rd(2, 22),
                 vel = 4,
                 bul_dam=1,
                 bul_vel=4,
                 burst=False,
                 rapid_fire=0,
                 reload=0):
        super().__init__(hp=hp,
                         width=width,
                         pos=(pos, 0))
        self.prim_vel = vel
        self.vel = vel
        self.prim_bul_dam = bul_dam
        self.bul_dam = bul_dam
        self.prim_bul_vel = bul_vel
        self.bul_vel = bul_vel
        self.burst = burst
        self.fire_rate = (int(not self.burst) + 1) * (fps / bul_vel)
        self.rapid_fire = rapid_fire
        self.firing = False
        self.rapid_fire_start = -1
        self.fire_count = 0
        self.reload = sec_to_frame(reload)
        self.reloading = False
        self.reload_start = -1
    def change_vel(self, multipul):
        if self.vel <= fps:
            self.vel *= multipul
    def reset_vel(self):
        self.vel = self.prim_vel
    def change_bul_dam(self, multipul):
        self.bul_dam *= multipul
    def reset_bul_dam(self):
        self.bul_dam = self.prim_bul_dam
    def change_bul_vel(self, multipul):
        if self.bul_vel <= fps:
            self.bul_vel *= multipul
    def reset_bul_vel(self):
        self.bul_vel = self.prim_bul_vel
    def fire_se(self, pwm):
        vel = abs(self.bul_vel)
        count = -1
        while (vel := vel //2) != 1:
            count += 1
        pwm.start(50)
        pwm.ChangeFrequency(scale(27 + 12 * count))
        sleep(1/64 - 3/256)
        pwm.ChangeFrequency(scale(27 + 12 * (count - 1)))
        sleep(1/64 - 1/256)
        pwm.stop()
    def fire_se_manager(self, pwm):
        fire_se_thread = Thread(target=self.fire_se, args=(pwm,))
        fire_se_thread.start()
        fire_se_thread.join()
    def begin_rapid_fire(self, frame, pwm, bul_map=BulMap()):
        self.firing = True
        bul_map.add_new_bul(frame=frame, pos=self.pos["x"], bul_dam=self.bul_dam, bul_vel=self.bul_vel)
        self.fire_se_manager(pwm)
        self.fire_count += 1
        self.rapid_fire_start = frame
    def rapid_fire_manager(self, frame, pwm, bul_map=BulMap()):
        if abs(frame - self.rapid_fire_start) % self.fire_rate == 0:
            bul_map.add_new_bul(frame=frame, pos=self.pos["x"], bul_dam=self.bul_dam, bul_vel=self.bul_vel)
            self.fire_se_manager(pwm)
            self.fire_count += 1
    def end_rapid_fire(self, frame=-1):
        self.firing = False
        self.rapid_fire_start = -1
        self.fire_count = 0
        self.reloading = True
        self.reload_start = frame
    def reload_manager(self, frame=-1):
        if abs(frame - self.reload_start) == self.reload:
            self.reloading = False
            self.reload_start = -1
    def fire(self, frame, pwm, bul_map=BulMap(), input=rd(0,16)):
        if self.reloading:
            self.reload_manager(frame)
        elif self.firing:
            if self.fire_count < self.rapid_fire:
                self.rapid_fire_manager(frame, pwm, bul_map)
            else:
                self.end_rapid_fire(frame)
        elif not input:
            self.begin_rapid_fire(frame, pwm, bul_map)

def try_get_dam(get_dam):
    def wrapper(cls, own="", dam=1):
        if own == "p":
            get_dam(cls, own=own, dam=dam)
    return wrapper

class Item(Entity):
    def __init__(self,
                 *,
                 width=len(item_graphic),
                 pos=(rd(2, field_width - 3), rd(3, field_height - 3)),
                 effect=list(effects.keys())[rd(0, len(effects) - 1)],
                 player=Creature(),
                 enemy=Creature(),
                 item_map=ItemMap(),
                 bul_map=BulMap(),
                 item_list=[]):
        self.entities = {"player" : player,
                         "enemy" : enemy,
                         "none" : self}
        target, self.function, self.reset, self.hp, self.effect_val, self.sustain = effects[effect].values()
        self.target = self.entities[target]
        super().__init__(hp=self.hp,
                         width=width,
                         pos=pos)
        self.break_thread = Thread(target=self.detect_item_break, kwargs={"item_map" : item_map, "bul_map" : bul_map, "item_list" : item_list})
        self.break_thread.start()
    def __del__(self):
        self.break_thread.join()
    def add_new_item(self, item_map=ItemMap(), bul_map=BulMap()):
        if self.hp > 0:
            x, y = self.pos.values()
            item_map.item_map[y][x] = self
            item_map.item_sum += 1
            owner, shot, dam, vel = bul_map.bul_map[y][x].values()
            if owner:
                self.get_dam(own=owner, dam=dam)
                bul_map.bul_map[y][x] = {"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16}
    def detect_item_break(self, item_map=ItemMap(), bul_map=BulMap(), item_list=[]):
        self.add_new_item(item_map, bul_map)
        while self.hp > 0:
            sleep(refresh_rate)
        x, y = self.pos.values()
        item_map.item_map[y][x] = None
        getattr(self.target, self.function)(self.effect_val)
        sleep(self.sustain)
        getattr(self.target, self.reset)()
        item_map.item_sum -= 1
        item_list.remove(self)
        del self
    @try_get_dam
    def get_dam(self, own="", dam=1):
        super().get_dam(dam=dam)
    #for wall
    def none(self, multipul):
        pass
    def reset_none(self):
        pass