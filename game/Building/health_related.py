from game.buildings import Building
import pygame as pg

class HealthStructure(Building):
    def __init__(self, *coor, world, neededResources):
        super(HealthStructure, self).__init__(*coor, world)
        self.neededResources = neededResources

############### Reservoir ###############
class Barber:
    name = "Barber"
    image = pg.image.load("assets/graphics/buildings/Security_00021.png")

    def __init__(self, pos, resource_manager):
        # We start by a small tent in order to level up as the game gets more advanced
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_cooldown = now
            super().burn(now)



#########################################

# ############### Aqueduct ###############
# class Aqueduct(WaterStructure):
#     name = "Aqueduct"
#     def __init__(self, *coor, world):
#         super(Aqueduct, self).__init__(1, 1, *coor, world, 8, 0)
#
#
#     def isConnectedToReservoir(self):
#         # to check if this Aqueduct is connected to a reservoir
#         for y in range(self.posy-1, self.posy+self.sizey+2):
#             currentBuildings = [self.world.get_building(self.posx-1, y), self.world.get_building(self.posx+1, y)]
#             for currentBuilding in currentBuildings:
#                 if (isinstance(currentBuilding, Reservoir)): return True
#                 if (isinstance(currentBuilding, Aqueduct)):
#                     if (currentBuilding.isConnectedToReservoir()): return True
#         for x in range(self.posx, self.posx+self.sizex+1):
#             currentBuildings = [self.world.get_building(x, self.posy), self.world.get_building(x, self.posy+1)]
#             for currentBuilding in currentBuildings:
#                 if (isinstance(currentBuilding, Reservoir)): return True
#                 if (isinstance(currentBuilding, Aqueduct)):
#                     if (currentBuilding.isConnectedToReservoir()): return True
#         return False
#
#
#
#
# ########################################
#
# ############### Fountain ###############
# class Fountain(WaterStructure):
#     name = "Fountain"
#     def __init__(self, *coor, world):
#         super(Fountain, self).__init__(1, 1, *coor, world, 15, 3)
#
#
#     def isSupplied(self):
#         pass  # Check if this fountain is supplied by reservoir
#
# ########################################
#
# ############### Well ###############
# class Well(WaterStructure):
#     name = "Well"
#     def __init__(self, *coor, world):
#         super(Well, self).__init__(1, 1, *coor, world, 5, 2)
#
#
# ####################################