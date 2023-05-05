from game.buildings import Building
import pygame as pg

class WaterStructure(Building):
    def __init__(self, *coor, world, neededResources, waterSupplyRadius):
        super(WaterStructure, self).__init__(*coor, world)
        self.neededResources = neededResources
        self.waterSuppplyRadius = waterSupplyRadius


############### Reservoir ###############
class Reservoir(WaterStructure):
    name = "Reservoir"
    def __init__(self, *coor, world):
        super(Reservoir, self).__init__(3, 3, *coor, world, 80, 10)


    def isConnectedToReservoir(self):
        # to check if this Reservoir is connected to another reservoir
        for y in range(self.posy-1, self.posy+self.sizey+2):
            currentBuildings = [self.world.get_building(self.posx-1, y), self.world.get_building(self.posx+1, y)]
            for currentBuilding in currentBuildings:
                if (isinstance(currentBuilding, Aqueduct)):
                    if (currentBuilding.isConnectedToReservoir()): return True
        for x in range(self.posx, self.posx+self.sizex+1):
            currentBuildings = [self.world.get_building(x, self.posy), self.world.get_building(x, self.posy+1)]
            for currentBuilding in currentBuildings:
                if (isinstance(currentBuilding, Aqueduct)):
                    if (currentBuilding.isConnectedToReservoir()): return True
        return False

    def isNearWater(self):
        pass  # to check if this reservoir is near water supply

    def isActivated(self):
        return self.isNearWater() or self.isConnectedToReservoir()


#########################################

############### Aqueduct ###############
class Aqueduct(WaterStructure):
    name = "Aqueduct"
    def __init__(self, *pos, resource_manager):
        super(Aqueduct, self).__init__(1, 1, *pos, None, 8, 0)


    def isConnectedToReservoir(self):
        # to check if this Aqueduct is connected to a reservoir
        for y in range(self.posy-1, self.posy+self.sizey+2):
            currentBuildings = [self.world.get_building(self.posx-1, y), self.world.get_building(self.posx+1, y)]
            for currentBuilding in currentBuildings:
                if (isinstance(currentBuilding, Reservoir)): return True
                if (isinstance(currentBuilding, Aqueduct)):
                    if (currentBuilding.isConnectedToReservoir()): return True
        for x in range(self.posx, self.posx+self.sizex+1):
            currentBuildings = [self.world.get_building(x, self.posy), self.world.get_building(x, self.posy+1)]
            for currentBuilding in currentBuildings:
                if (isinstance(currentBuilding, Reservoir)): return True
                if (isinstance(currentBuilding, Aqueduct)):
                    if (currentBuilding.isConnectedToReservoir()): return True
        return False




########################################

############### Fountain ###############
class Fountain(WaterStructure):
    name = "Fountain"
    def __init__(self, *coor, world):
        super(Fountain, self).__init__(1, 1, *coor, world, 15, 3)


    def isSupplied(self):
        pass  # Check if this fountain is supplied by reservoir

########################################

############### Well ###############
class Well:
    name = "well"
    image = pg.image.load("assets/graphics/buildings/well.png")
    def __init__(self, pos, resource_manager):
        # We start by a small tent in order to level up as the game gets more advanced
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources += 1
            self.resource_cooldown = now

####################################