from game.buildings import Building
import pygame as pg


class Road(Building):
    # We start by importing the building class (Heritage)
    name = 'road'
    def __init__(self, x, y, pos, resource_manager, buildings):
        # Here, we have 1,1 since these are the measurements of a road

        self.name = "left_right_road"
        self.resource_cooldown = pg.time.get_ticks()
        self.adjdacent_roads = [None, None, None, None]

        super().__init__(1, 1, x, y, pos, resource_manager, buildings)
        self.connect_road = self

    def update(self):
        pass

    def __repr__(self):
        # Represents the object road in the class Road as a string

        return "road"

    def set_name(self, name: str) -> None:
        self.name = name
