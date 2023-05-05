from game.buildings import Building
from enum import *
import pygame as pg


class Housing_Levels(Enum):
    # There are many housing levels that require different services
    # However, we will only include the first four since it's long
    # to implement/not necessarily required.

    small_tent = 1
    large_tent = 2
    small_shack = 3
    large_shack = 4


class House_Size:
    sizex: int()
    sizey: int()

    def __init__(self, x, y):
        self.sizex = x
        self.sizey = y


size = {Housing_Levels.small_tent: House_Size(1, 1), Housing_Levels.large_tent: House_Size(1, 1),
        Housing_Levels.small_shack: House_Size(1, 1), Housing_Levels.large_shack: House_Size(1, 1)}


class House(Building):
    # We import the building class (Heritage)
    name = "house"

    def __init__(self, x, y, pos, resource_manager, buildings, entities, world):
        self.level = Housing_Levels.small_tent
        # We start by a small tent in order to level up as the game gets more advanced
        self.name = "housePanel"
        self.houses = ["house1", "house2", "house3", "house4", "house5", "house6", "house7"]
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(str(self))
        self.resource_cooldown = pg.time.get_ticks()
        self.entities = entities
        self.world = world
        self.previous_time = pg.time.get_ticks()

        super().__init__(size[self.level].sizex, size[self.level].sizey, x, y, pos, resource_manager, buildings)

    def __repr__(self):
        return "house"

    def update(self):
        now = pg.time.get_ticks()
        # destroy panel after few seconds
        if now - self.resource_cooldown > 10000 and self.worker is None:
            self.regress()
        # upgrade the panel in a house
        elif self.worker is not None and self.name == "housePanel" and self.worker.house_reached:
            self.name = "house1"
            self.clock = now

        if self.name != "housePanel":
            super().burn(now)
            self.improve()

    def improve(self):  # the condition / type of housing could improve(get better)

        now = pg.time.get_ticks()
        if now - self.previous_time > 10000:
            if self.name != "house7":
                current_index = self.houses.index(self.name)
                next_index = (current_index + 1) % len(self.houses)
                self.name = self.houses[next_index]
                self.previous_time = now

    def regress(self):  # the condition / type of housing could regress(get worst)
        self.buildings[self.x][self.y] = None
        self.world[self.x][self.y]["collision"] = False
        for worker in self.entities:
            if worker == self.worker:
                self.entities.remove(self.worker)
        self.entities.remove(self)
