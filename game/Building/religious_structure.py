from game.buildings import Building
import pygame as pg


class ReligiousStructure(Building):
    def __init__(self, *coor, world, neededResources):
        super(ReligiousStructure, self).__init__(*coor, world)
        self.neededResources = neededResources

############### Reservoir ###############
class Ceres(ReligiousStructure):
    name = "Ceres"
    image = pg.image.load("assets/graphics/buildings/ceres_small.png")
    def __init__(self, *coor, world):
        super(Ceres, self).__init__(3, 3, *coor, world, 80, 10)