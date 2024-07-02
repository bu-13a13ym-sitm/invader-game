from random import randint as rd


field_width = 25
field_height = 15
refresh_rate = 1 / (16 * 4)
fps = int(1 / refresh_rate)
max_items = 2

player_graphic = ("/■\\",
                  "■■■")

enemy_graphic = ("■ ■ ■",
                " \\■/ ",
                "  ■  ")

bul_graphic = "\033[32mo\033[0m"
fast_bul_graphic = "\033[36m0\033[0m"
fastest_bul_graphic = "\033[33m|\033[0m"
no_col_bul = "o"
no_col_fast_bul = "0"
no_col_fastest_bul = "|"
item_graphic = "*"

easy = {"ehp"           : 25,
        "evel"          : 4,
        "ebul_vel"      : 8,
        "erapid_fire"   : 7,
        "ereload"       : 4,
        "estart"        : 5,
        "php"           : 10,
        "pvel"          : 16,
        "pbul_vel"      : -32,
        "prapid_fire"   : 5,
        "preload"       : 1}
nomal = {"ehp"          : 50,
         "evel"         : 8,
         "ebul_vel"     : 16,
         "erapid_fire"  : 10,
         "ereload"      : 3,
         "estart"       : 3,
         "php"          : 8,
         "pvel"         : 16,
         "pbul_vel"     : -32,
         "prapid_fire"  : 4,
         "preload"      : 1.5}
hard = {"ehp"           : 100,
        "evel"          : 16,
        "ebul_vel"      : 32,
        "erapid_fire"   : 15,
        "ereload"       : 1.5,
        "estart"        : 1.5,
        "php"           : 5,
        "pvel"          : 16,
        "pbul_vel"      : -16,
        "prapid_fire"   : 3,
        "preload"       : 2}

effect_keys = ("target", "function", "reset", "hp", "effect_val", "sustain")

effects = {
    "pvel_up"           : {key : val for key, val in zip(effect_keys, ("player", "change_vel", "reset_vel", 5, 2, 5))},
    "pbul_dam_up"       : {key : val for key, val in zip(effect_keys, ("player", "change_bul_dam", "reset_bul_dam", 5, 2, 5))},
    "pbul_vel_up"       : {key : val for key, val in zip(effect_keys, ("player", "change_bul_vel", "reset_bul_vel", 5, 2, 5))},
    "evel_down"         : {key : val for key, val in zip(effect_keys, ("enemy", "change_vel", "reset_vel", 5, 0.5, 5))},
    "ebul_vel_down"     : {key : val for key, val in zip(effect_keys, ("enemy", "change_bul_vel", "reset_bul_vel", 5, 0.5, 5))},
    #"wall"              : {key : val for key, val in zip(effect_keys, ("none", "none", "reset_none", 10, 0, 0))}
}

def sec_to_frame(sec):
    return sec * fps


def main():
    print(len(bul_graphic))


if __name__ == "__main__":
    main()