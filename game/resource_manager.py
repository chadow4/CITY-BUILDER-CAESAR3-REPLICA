from .Building.water_strcuture import *
from .Building.health_related import *
from .Building.religious_structure import *
from .Building.prefecture import *
import pygame as pg



class ResourceManager:


    def __init__(self):

        # resources
        self.resources = 10000

        #costs
        self.costs = {
            "road": 7,
            "house": 3,
            "shovel": 2,
            Well.name: 10,
            Barber.name: 10,
            Ceres.name: 10,
            Prefecture.name: 30
        }

    def apply_cost_to_resource(self, building):
        self.resources -= self.costs[building]

    def is_affordable(self, building):
        affordable = True
        if self.costs[building] > self.resources:
            affordable = False
        return affordable

