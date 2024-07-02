from lib.global_variables import field_width, field_height, fps, enemy_graphic, player_graphic


class ItemMap:
    def __init__(self):
        self.item_map = [[None for row in range(field_width)] for col in range(field_height)]
        self.item_sum = 0

class BulMap:
    def __init__(self):
        self.bul_map = [[{"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16} for row in range(field_width)] for col in range(field_height)]
    def add_new_bul(self, frame, pos, bul_dam, bul_vel):
        if bul_vel > 0:
            col = len(enemy_graphic)
            owner = "e"
        elif bul_vel < 0:
            col = field_height - len(player_graphic) - 1
            owner = "p"
        self.bul_map[col][pos]["owner"] = owner
        self.bul_map[col][pos]["shot"] = frame
        self.bul_map[col][pos]["dam"] = bul_dam
        self.bul_map[col][pos]["vel"] = bul_vel
    def advance_frame(self, frame):
        new_map = BulMap().bul_map
        for col in range(len(self.bul_map)):
            for row, info in enumerate(self.bul_map[col]):
                if (info["owner"] == "e") and (col < (field_height - 1)):
                    if (frame - self.bul_map[col][row]["shot"]) % (fps // abs(self.bul_map[col][row]["vel"])) == 0:
                        if (self.bul_map[col + 1][row]["owner"] != "p") and (new_map[col + 1][row]["owner"] != "p"):
                            new_map[col + 1][row] = info
                        else:
                            new_map[col + 1][row] = {"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16}
                    else:
                        new_map[col][row] = info
                elif (info["owner"] == "p") and (col > 0):
                    if (frame - self.bul_map[col][row]["shot"]) % (fps // abs(self.bul_map[col][row]["vel"])) == 0:
                        if (self.bul_map[col - 1][row]["owner"] != "e") and (new_map[col - 1][row]["owner"] != "e"):
                            new_map[col - 1][row] = info
                        else:
                            new_map[col - 1][row] = {"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16}
                    else:
                        new_map[col][row] = info
        self.bul_map = new_map