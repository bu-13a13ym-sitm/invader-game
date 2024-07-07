from lib.global_variables import field_width, field_height, fps, enemy_graphic, player_graphic


class ItemMap:
    def __init__(self):
        self.item_map = [[None for col in range(field_width)] for row in range(field_height)]
        self.item_sum = 0

class BulMap:
    def __init__(self):
        self.bul_map = [[{"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16} for col in range(field_width)] for row in range(field_height)]
    def add_new_bul(self, frame, pos, bul_dam, bul_vel):
        if bul_vel > 0:
            row = len(enemy_graphic)
            owner = "e"
        elif bul_vel < 0:
            row = field_height - len(player_graphic) - 1
            owner = "p"
        self.bul_map[row][pos]["owner"] = owner
        self.bul_map[row][pos]["shot"] = frame
        self.bul_map[row][pos]["dam"] = bul_dam
        self.bul_map[row][pos]["vel"] = bul_vel
    def advance_frame(self, frame):
        new_map = BulMap().bul_map
        for row in range(len(self.bul_map)):
            for col, info in enumerate(self.bul_map[row]):
                if (info["owner"] == "e") and (row < (field_height - 1)):
                    if (frame - self.bul_map[row][col]["shot"]) % (fps // abs(self.bul_map[row][col]["vel"])) == 0:
                        if (self.bul_map[row + 1][col]["owner"] != "p") and (new_map[row + 1][col]["owner"] != "p"):
                            new_map[row + 1][col] = info
                        else:
                            new_map[row + 1][col] = {"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16}
                    else:
                        new_map[row][col] = info
                elif (info["owner"] == "p") and (row > 0):
                    if (frame - self.bul_map[row][col]["shot"]) % (fps // abs(self.bul_map[row][col]["vel"])) == 0:
                        if (self.bul_map[row - 1][col]["owner"] != "e") and (new_map[row - 1][col]["owner"] != "e"):
                            new_map[row - 1][col] = info
                        else:
                            new_map[row - 1][col] = {"owner" : "", "shot" : -1, "dam" : 1, "vel" : 16}
                    else:
                        new_map[row][col] = info
        self.bul_map = new_map