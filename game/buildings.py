
import random
from dataclasses import *
from datetime import *
from enum import *
from math import floor
import pygame as pg

class Building:
    # We start by defining a class Building that will be general to all the classes that will follow

    def __init__(self, sizex, sizey, x, y, pos, resource_manager, buildings):
        self.sizex = sizex
        self.sizey = sizey
        self.x = x  # position on the map
        self.y = y
        self.pos = pos
        self.buildings = buildings
        self.resource_manager = resource_manager
        self.worker = None
        # self.resource_manager.apply_cost_to_resource(self.name) put this function in ALL other class

        self.collapse_stage = 0
        self.burn_stage = 0
        self.burn_cooldown = random.randint(3, 9)
        self.clock = 0

        self.collapsed = False
        self.start_burning = None
        self.burning = False
        self.burning_time = 0

        self.connect_road = None

    def burn(self, clock):
        if (clock - self.clock > self.burn_cooldown * 1000) and not self.burning:
            self.burn_stage += 1
            self.burn_cooldown = random.randint(2, 6)
            self.clock = clock
        if self.burn_stage > 9:
            self.burn_stage = 10
            self.burning = True

# Engineers_Post
class Engineers_Post(Building):
    # We import the building class (Heritage)

    def __init__(self, posx, posy):
        super().__init__(1, 1, posx, posy)

    def __repr__(self):
        return "Engineers_Post"

    # We still need to link it to engineers, in other words, to the walkers.


# House

class Housing_Levels(Enum):
    # There are many housing levels that require different services
    # However, we will only include the first four since it's long
    # to implement/not necessarily required.

    small_tent = 1
    large_tent = 2
    small_shack = 3
    large_shack = 4


@dataclass  # shorter/clearer code block
class House_Size:
    sizex: int()
    sizey: int()


size = {Housing_Levels.small_tent: House_Size(1, 1), Housing_Levels.large_tent: House_Size(1, 1),
        Housing_Levels.small_shack: House_Size(1, 1), Housing_Levels.large_shack: House_Size(1, 1)}




# Prefecture

# class Prefecture(Building):
#     # We start by importing the building class (Heritage)
#
#     def __init__(self, posx, posy):
#         super().__init__(1, 1, posx, posy)
#
#     def __repr__(self):
#         # Represents the object prefecture in the class Prefecture as a string
#
#         return "Prefecture"
#
#     # Same as previous, we still need to link it to the walkers. In this case, the prefect.


# Road

# We consider roads as buildings +/- a few specifications


