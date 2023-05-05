from game.buildings import Building
import pygame as pg

class Prefecture(Building):
    name = "prefecture"
    def __init__(self, x, y, pos, resource_manager, buildings, entities, world):
        self.entities = entities
        self.world = world
        super().__init__(1, 1, x, y, pos, resource_manager, buildings)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        
    def __repr__(self):
        return "Prefecture"

    #Same as previous, we still need to link it to the walkers. In this case, the prefect.
