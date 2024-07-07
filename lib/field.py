from lib.global_variables import field_width, field_height, refresh_rate, player_graphic, enemy_graphic, bul_graphic, fast_bul_graphic, fastest_bul_graphic, no_col_bul, no_col_fast_bul, no_col_fastest_bul, item_graphic
from lib.maps import ItemMap, BulMap
from lib.entities import Creature, Item
from random import randint as rd
from sys import stdout
from time import sleep


class Field:
    def __init__(self,*, enemy=Creature(), player=Creature(), item_map=ItemMap(), bul_map=BulMap(), clear = 0):
        self.field = []
        self.field.append("-" * (field_width + 2))
        for b in enemy_graphic:
            text = "|" + " " * (enemy.pos["x"] - (len(b) // 2)) + b
            text += " " * (field_width - (len(text) - 1)) + "|"
            self.field.append(text)
        for blank in range(field_height - len(enemy_graphic) - len(player_graphic)):
            self.field.append("|" + " " * field_width + "|")
        for p in player_graphic:
            text = "|" + " " * (player.pos["x"] - (len(p) // 2)) + p
            text += " " * (field_width - (len(text) - 1)) + "|"
            self.field.append(text)
        self.field.append("-" * (field_width + 2))
        for row, i_row in enumerate(item_map.item_map):
            curr_row = self.field[row + 1]
            for col, i_col in enumerate(i_row):
                if i_col:
                    self.field[row + 1] = curr_row[:col + 1] + item_graphic + curr_row[col + 2:]
                curr_row = self.field[row + 1]
        for row, b_row in enumerate(bul_map.bul_map):
            curr_row = self.field[row + 1]
            for col, b_col in enumerate(b_row):
                if b_col["owner"]:
                    if self.field[row + 1][col + 1] == " ":
                        vel = abs(b_col["vel"])
                        if vel <= 16:
                            self.field[row + 1] = curr_row[:col + 1] + 'a' + curr_row[col + 2:]
                        elif vel <= 32:
                            self.field[row + 1] = curr_row[:col + 1] + 'b' + curr_row[col + 2:]
                        else:
                            self.field[row + 1] = curr_row[:col + 1] + 'c' + curr_row[col + 2:]
                    elif self.field[row + 1][col + 1] == item_graphic:
                        item_map.item_map[row][col].get_dam(own=bul_map.bul_map[row][col]["owner"], dam=bul_map.bul_map[row][col]["dam"])
                        bul_map.bul_map[row][col] = {"owner" : "", "shot" : -1, "dam" : 1}
                    elif row < len(enemy_graphic):
                        enemy.get_dam(dam=bul_map.bul_map[row][col]["dam"])
                        bul_map.bul_map[row][col] = {"owner" : "", "shot" : -1, "dam" : 1}
                    elif row > field_height - len(player_graphic) - 1:
                        player.get_dam(dam=bul_map.bul_map[row][col]["dam"])
                        bul_map.bul_map[row][col] = {"owner" : "", "shot" : -1, "dam" : 1}
                curr_row = self.field[row + 1]
        if clear:
            for row, f_row in enumerate(self.field):
                new_row = ""
                for f_col in f_row:
                    if f_col == 'a':
                        new_row += no_col_bul
                    elif f_col == 'b':
                        new_row += no_col_fast_bul
                    elif f_col == 'c':
                        new_row += no_col_fastest_bul
                    else:
                        new_row += f_col
                self.field[row] = new_row
        else:
            for row, f_row in enumerate(self.field):
                new_row = ""
                for f_col in f_row:
                    if f_col == 'a':
                        new_row += bul_graphic
                    elif f_col == 'b':
                        new_row += fast_bul_graphic
                    elif f_col == 'c':
                        new_row += fastest_bul_graphic
                    else:
                        new_row += f_col
                self.field[row] = new_row

    def print_field(self):
        for _ in self.field:
            stdout.write("\033[F")
        print(*(self.field), sep="\n")
        stdout.flush()


def main():
    player = Creature(hp=10, width=len(player_graphic), pos=rd(1,23), vel=8, bul_dam=1, bul_vel=-8, burst=True, rapid_fire=3, reload=3)
    enemy = Creature(hp=100, width=len(enemy_graphic), pos=rd(2,22), vel=4, bul_dam=1, bul_vel=16, burst=False, rapid_fire=20, reload=3)
    field = Field(player=player, enemy=enemy)
    print(*player_graphic, sep="\n")
    print(*enemy_graphic, sep= "\n")
    print(bul_graphic)
    print(player.pos, enemy.pos)
    print("\n" * 9)
    field.print_field()
    print("enemy hp:",enemy.hp,"player hp:",player.hp)
    stdout.flush()
    frame = 0
    for i in range (16):
        sleep(refresh_rate)
        player.change_pos(rd(1,23), frame)
        enemy.change_pos(rd(2,22), frame)
        field = Field(player=player, enemy=enemy)
        stdout.write("\033[F")
        field.print_field()
        print("enemy hp:",f"{enemy.hp:3}","player hp:",f"{player.hp:2}")
        stdout.flush()
        frame += 1
    player.change_pos(rd(1,23), frame)
    enemy.change_pos(rd(2,22), frame)
    bul_map = BulMap()
    bul_map.advance_frame(frame=frame)
    bul_map.add_new_bul(frame=frame, pos=enemy.pos["x"], bul_dam=enemy.bul_dam, bul_vel=enemy.bul_vel)
    bul_map.add_new_bul(frame=frame, pos=player.pos["x"], bul_dam=player.bul_dam, bul_vel=player.bul_vel)
    sleep(refresh_rate)
    field = Field(player=player, enemy=enemy, bul_map=bul_map)
    stdout.write("\033[F")
    field.print_field()
    print("enemy hp:",f"{enemy.hp:3}","player hp:",f"{player.hp:2}")
    stdout.flush()
    frame += 1
    sleep(refresh_rate)
    for i in range (200):
        sleep(refresh_rate)
        bul_map.advance_frame(frame=frame)
        player.change_pos(rd(1,23), frame)
        enemy.change_pos(rd(2,22), frame)
        field = Field(player=player, enemy=enemy, bul_map=bul_map)
        stdout.write("\033[F")
        field.print_field()
        print("enemy hp:",f"{enemy.hp:3}","player hp:",f"{player.hp:2}")
        stdout.flush()
        frame += 1

if __name__ == "__main__":
    main()