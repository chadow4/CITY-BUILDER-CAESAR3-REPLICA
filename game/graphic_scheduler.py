import random

import pygame as pg

from .Building.health_related import *

# dict of other textures :

other_tiles: dict[str, pg.Surface | list[pg.Surface]] = {
    "field": pg.image.load("assets/graphics/field.png").convert_alpha(),

    # Pannel enter et exit
    "panel_start": pg.image.load("assets/graphics/LandStartArrow.png").convert_alpha(),
    "panel_exit": pg.image.load("assets/graphics/LandExitArrow.png").convert_alpha(),

    ## road
    # 2 connections
    "left_right_road": pg.image.load("assets/graphics/Road1.png").convert_alpha(),  # 1
    "top_bottom_road": pg.image.load("assets/graphics/Road2.png").convert_alpha(),  # 2

    "top_to_left_road": pg.image.load("assets/graphics/Road9.png").convert_alpha(),  # 9
    "top_to_right_road": pg.image.load("assets/graphics/Road10.png").convert_alpha(),  # 10
    "bottom_to_right_road": pg.image.load("assets/graphics/Road8.png").convert_alpha(),  # 8
    "bottom_to_left_road": pg.image.load("assets/graphics/Road11.png").convert_alpha(),  # 11

    # 3 connections
    "right_bottom_left_road": pg.image.load("assets/graphics/Road6.png").convert_alpha(),  # 6
    "top_bottom_left_road": pg.image.load("assets/graphics/Road5.png").convert_alpha(),  # 5
    "top_right_bottom_road": pg.image.load("assets/graphics/Road3.png").convert_alpha(),  # 3
    "top_right_left_road": pg.image.load("assets/graphics/Road4.png").convert_alpha(),  # 4

    # 4 connections
    "all_directions_road": pg.image.load("assets/graphics/Road7.png").convert_alpha(),  # 7

    # different kind of house (pattern: house + House.worker.house_reached)
    "housePanel": pg.image.load("assets/graphics/building00.png").convert_alpha(),
    "house1": pg.image.load("assets/graphics/house1.png").convert_alpha(),
    "house2": pg.image.load("assets/graphics/house2.png").convert_alpha(),
    "house3": pg.image.load("assets/graphics/house3.png").convert_alpha(),
    "house4": pg.image.load("assets/graphics/house4.png").convert_alpha(),
    "house5": pg.image.load("assets/graphics/house5.png").convert_alpha(),
    "house6": pg.image.load("assets/graphics/house6.png").convert_alpha(),
    "house7": pg.image.load("assets/graphics/house7.png").convert_alpha(),
    "house_fire": pg.image.load("assets/graphics/buildings/house/house_fire.png").convert_alpha(),

    # overlay and fire
    "level_fire_floor": pg.image.load("assets/graphics/overlay/Land2a_00001.png").convert_alpha(),
    "level_fire_base":  pg.image.load("assets/graphics/overlay/Sprites_00020.png").convert_alpha(),
    "level_fire_wall":  pg.image.load("assets/graphics/overlay/Sprites_00019.png").convert_alpha(),
    "level_fire_roof":  pg.image.load("assets/graphics/overlay/Sprites_00018.png").convert_alpha(),


    ######### pattern of worker's picture: basic_worker + Direction.value + current_frame #########
    # sprite if worker.direction is None
    "basic_worker-10": pg.image.load("assets/graphics/Workers/citizen02_00095.png").convert_alpha(),
    # vers le down_right
    "basic_worker10": pg.image.load("assets/graphics/Workers/citizen02_00003.png").convert_alpha(),
    "basic_worker11": pg.image.load("assets/graphics/Workers/citizen02_00011.png").convert_alpha(),
    "basic_worker12": pg.image.load("assets/graphics/Workers/citizen02_00019.png").convert_alpha(),
    "basic_worker13": pg.image.load("assets/graphics/Workers/citizen02_00027.png").convert_alpha(),
    "basic_worker14": pg.image.load("assets/graphics/Workers/citizen02_00035.png").convert_alpha(),
    "basic_worker15": pg.image.load("assets/graphics/Workers/citizen02_00043.png").convert_alpha(),
    "basic_worker16": pg.image.load("assets/graphics/Workers/citizen02_00051.png").convert_alpha(),
    "basic_worker17": pg.image.load("assets/graphics/Workers/citizen02_00059.png").convert_alpha(),
    "basic_worker18": pg.image.load("assets/graphics/Workers/citizen02_00067.png").convert_alpha(),
    "basic_worker19": pg.image.load("assets/graphics/Workers/citizen02_00075.png").convert_alpha(),
    "basic_worker110": pg.image.load("assets/graphics/Workers/citizen02_00083.png").convert_alpha(),
    "basic_worker111": pg.image.load("assets/graphics/Workers/citizen02_00091.png").convert_alpha(),
    # vers le top_right
    "basic_worker20": pg.image.load("assets/graphics/Workers/citizen02_00001.png").convert_alpha(),
    "basic_worker21": pg.image.load("assets/graphics/Workers/citizen02_00009.png").convert_alpha(),
    "basic_worker22": pg.image.load("assets/graphics/Workers/citizen02_00017.png").convert_alpha(),
    "basic_worker23": pg.image.load("assets/graphics/Workers/citizen02_00025.png").convert_alpha(),
    "basic_worker24": pg.image.load("assets/graphics/Workers/citizen02_00033.png").convert_alpha(),
    "basic_worker25": pg.image.load("assets/graphics/Workers/citizen02_00041.png").convert_alpha(),
    "basic_worker26": pg.image.load("assets/graphics/Workers/citizen02_00049.png").convert_alpha(),
    "basic_worker27": pg.image.load("assets/graphics/Workers/citizen02_00057.png").convert_alpha(),
    "basic_worker28": pg.image.load("assets/graphics/Workers/citizen02_00065.png").convert_alpha(),
    "basic_worker29": pg.image.load("assets/graphics/Workers/citizen02_00073.png").convert_alpha(),
    "basic_worker210": pg.image.load("assets/graphics/Workers/citizen02_00081.png").convert_alpha(),
    "basic_worker211": pg.image.load("assets/graphics/Workers/citizen02_00089.png").convert_alpha(),
    # vers le top_left
    "basic_worker30": pg.image.load("assets/graphics/Workers/citizen02_00095.png").convert_alpha(),
    "basic_worker31": pg.image.load("assets/graphics/Workers/citizen02_00007.png").convert_alpha(),
    "basic_worker32": pg.image.load("assets/graphics/Workers/citizen02_00015.png").convert_alpha(),
    "basic_worker33": pg.image.load("assets/graphics/Workers/citizen02_00023.png").convert_alpha(),
    "basic_worker34": pg.image.load("assets/graphics/Workers/citizen02_00031.png").convert_alpha(),
    "basic_worker35": pg.image.load("assets/graphics/Workers/citizen02_00039.png").convert_alpha(),
    "basic_worker36": pg.image.load("assets/graphics/Workers/citizen02_00047.png").convert_alpha(),
    "basic_worker37": pg.image.load("assets/graphics/Workers/citizen02_00055.png").convert_alpha(),
    "basic_worker38": pg.image.load("assets/graphics/Workers/citizen02_00063.png").convert_alpha(),
    "basic_worker39": pg.image.load("assets/graphics/Workers/citizen02_00071.png").convert_alpha(),
    "basic_worker310": pg.image.load("assets/graphics/Workers/citizen02_00079.png").convert_alpha(),
    "basic_worker311": pg.image.load("assets/graphics/Workers/citizen02_00087.png").convert_alpha(),
    # vers le down_left
    "basic_worker00": pg.image.load("assets/graphics/Workers/citizen02_00005.png").convert_alpha(),
    "basic_worker01": pg.image.load("assets/graphics/Workers/citizen02_00013.png").convert_alpha(),
    "basic_worker02": pg.image.load("assets/graphics/Workers/citizen02_00021.png").convert_alpha(),
    "basic_worker03": pg.image.load("assets/graphics/Workers/citizen02_00029.png").convert_alpha(),
    "basic_worker04": pg.image.load("assets/graphics/Workers/citizen02_00037.png").convert_alpha(),
    "basic_worker05": pg.image.load("assets/graphics/Workers/citizen02_00045.png").convert_alpha(),
    "basic_worker06": pg.image.load("assets/graphics/Workers/citizen02_00053.png").convert_alpha(),
    "basic_worker07": pg.image.load("assets/graphics/Workers/citizen02_00061.png").convert_alpha(),
    "basic_worker08": pg.image.load("assets/graphics/Workers/citizen02_00069.png").convert_alpha(),
    "basic_worker09": pg.image.load("assets/graphics/Workers/citizen02_00077.png").convert_alpha(),
    "basic_worker010": pg.image.load("assets/graphics/Workers/citizen02_00085.png").convert_alpha(),
    "basic_worker011": pg.image.load("assets/graphics/Workers/citizen02_00093.png").convert_alpha(),

    "House": pg.image.load("assets/graphics/buildings/house/house_lv0.png").convert_alpha(),
    "basic_worker": pg.image.load("assets/graphics/Workers/citizen02_00063.png").convert_alpha(),
    "well": pg.image.load("assets/graphics/buildings/well.png"),
    "barber": Barber.image,
    "prefecture": pg.image.load("assets/graphics/buildings/prefecture.png").convert_alpha()
}


def fill_grass_textures() -> None:
    other_tiles["grass"] = []
    for i in range(31, 90):
        other_tiles["grass"].append(pg.image.load("assets/graphics/Land1a_002" + str(i) + ".png").convert_alpha())


def fill_tree_textures() -> None:
    other_tiles["tree"] = []
    for i in range(35, 70):
        other_tiles["tree"].append(pg.image.load("assets/graphics/Land1a_000" + str(i) + ".png").convert_alpha())


def fill_water_textures() -> None:
    other_tiles["water"] = []
    for i in range(120, 128):
        other_tiles["water"].append(pg.image.load("assets/graphics/Land1a_00" + str(i) + ".png").convert_alpha())


def fill_rock_textures() -> None:
    other_tiles["rock"] = []
    for i in range(71, 80):
        other_tiles["rock"].append(pg.image.load("assets/graphics/land3a_000" + str(i) + ".png").convert_alpha())


def load_image():
    fill_tree_textures()
    fill_grass_textures()
    fill_water_textures()
    fill_rock_textures()
    return other_tiles


def get_texture(texture_name: str, texture_index: int = -1) -> pg.Surface:
    texture = other_tiles.get(texture_name)

    if texture is None:
        raise NameError("Error while loading the texture. Key ", texture_name, " does not exists!")

    if isinstance(texture, list):
        if texture_index == -1:
            texture = random.choice(texture)
        else:
            try:
                texture = texture[texture_index]
            except IndexError:
                print("Index ", texture_index, " not found in texture ", texture_name)
    return texture
