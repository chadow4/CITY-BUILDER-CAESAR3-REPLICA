import pygame as pg
from enum import Enum
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from random import randint
from .buildings import Building
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    NONE = -1

class BasicWorker:
    def __init__(self, pos_x, pos_y, world, buildings, workers):
        self.world = world
        self.workers = workers
        self.buildings : list[list[Building | None]] = buildings
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.old_pos_x = pos_x
        self.old_pos_y = pos_y
        self.default_pos_x = pos_x
        self.default_pos_y = pos_y
        self.name = "basic_worker"
        self.image = None
        self.move_timer = pg.time.get_ticks()
        self.path = []  # May be used to find a path
        self.length_current_path = 0
        self.max_length_path = 30   # Number of tile to walk before half turn
        self.current_direction = Direction.NONE     # indicate the current direction of the worker
        self.valid_tiles = []    # Matrix of nearby tiles where the walker can go
        self.tile_per_frame = 1/12
        self.current_frame = 0
        self.next_building = None

    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > 1000 * self.tile_per_frame:
            self.move_timer = now
            if self.path:
                self.go_to()
            else:
                self.random_patrol()

    # Return a path (list of tile which leads to the final tile)
    def pathSearch(self, pos_x, pos_y):
        grid = Grid(matrix=self.world_to_grid())
        start = grid.node(self.pos_y, self.pos_x)
        end = grid.node(pos_y, pos_x)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, run = finder.find_path(start, end, grid)
        print(path)
        if not path:
            return []
        path.pop(0)
        return path

    # Allow to go at a self.path position
    def go_to(self):
        if self.path:
            y, x = self.path[0]
            self.current_direction = self.findDirection((self.pos_x, self.pos_y), (x, y))
            self.current_frame += 1
            if self.current_frame == round(1 / self.tile_per_frame):
                self.move(self.current_direction)
                self.path.pop(0)
        self.length_current_path = 0

    # Allow to walker to patrol
    def random_patrol(self):
        # Donne une direction par défaut
        if self.current_direction == Direction.NONE:
            self.searchDirection()
        # start of the patrol
        if self.length_current_path <= self.max_length_path:    # If the length path is reached stop the loop
            if self.next_building is None or str(self.next_building) != "road":   # Test if a road is built on the next tile
                self.searchDirection()
                if self.current_direction == Direction.NONE:
                    return
            elif self.valid_tiles.count(True) > 2 and self.current_frame == 0:
                self.searchRandomDirection()
            self.current_frame += 1
            # Move by one tile
            self.next_building = self.continueToWalk()
            if self.current_frame == round(1 / self.tile_per_frame):
                self.move(self.current_direction)
                self.length_current_path += 1
                self.valid_tiles = self.roadsAround(round(self.pos_x), round(self.pos_y))

        else:
            self.path = self.pathSearch(self.default_pos_x, self.default_pos_y)  # It returns at the initial position

    # Function returning the opposite direction of the walker
    def opposedDirection(self):
        if self.current_direction.value == -1:
            return Direction(-1)
        return Direction((self.current_direction.value + 2) % 4)

    # search a valid direction
    def searchDirection(self):
        #On regarde combien de direction sont valides
        i = self.valid_tiles.count(True)
        for d, value in enumerate(self.valid_tiles):
            if value and i > 1 and (Direction(d) != self.opposedDirection()):
                self.current_direction = Direction(d)
                return
            elif value and i <= 1:
                self.current_direction = Direction(d)
                return
        self.current_direction = Direction.NONE

    def searchRandomDirection(self):
        i = self.valid_tiles.count(True)
        i = randint(0, i-1)
        for d, value in enumerate(self.valid_tiles):
            if value and i == 0 and (Direction(d) != self.opposedDirection()):
                print(Direction(d))
                self.current_direction = Direction(d)
                return
            if value:
                i -+ 1

    # Find the direction of workers with the next position
    def findDirection(self, pos, next_pos):
        if next_pos[0] - pos[0] == 1:
            return Direction.RIGHT
        if next_pos[0] - pos[0] == -1:
            return Direction.LEFT
        if next_pos[1] - pos[1] == 1:
            return Direction.UP
        if next_pos[1] - pos[1] == -1:
            return Direction.DOWN
        if (next_pos[1] - pos[1] == 0) and (next_pos[0] - pos[0] == 0):
            return self.opposedDirection()
        else:
            raise NameError("Error in the search of the direction")

    # Function which move the workers of 1 tile_per_frame
    def move(self, direction):
        self.old_pos_x, self.old_pos_y = round(self.pos_x), round(self.pos_y)
        match direction.value:
            case 0:  # UP
                self.pos_y += 1
            case 1:  # RIGHT
                self.pos_x += 1
            case 2:  # DOWN
                self.pos_y -= 1
            case 3:  # LEFT
                self.pos_x -= 1
            case _:
                pass
        # Manage when the worker is out of map
        if self.pos_x == 0 and self.current_direction == Direction(3):
            self.current_direction = Direction(1)
        if self.pos_x == len(self.world)-1 and self.current_direction == Direction(1):
            self.current_direction = Direction(3)
        if self.pos_y == 0 and self.current_direction == Direction(2):
            self.current_direction = Direction(0)
        if self.pos_y == len(self.world)-1 and self.current_direction == Direction(0):
            self.current_direction = Direction(2)

        self.workers[round(self.pos_x)][round(self.pos_y)].append(self)
        self.workers[self.old_pos_x][self.old_pos_y].remove(self)
        self.current_frame = 0

    # return position of worker between tiles
    def mini_move(self):
        if self.current_direction == Direction.UP:
            return 0, self.current_frame
        if self.current_direction == Direction.RIGHT:
            return self.current_frame, 0
        if self.current_direction == Direction.DOWN:
            return 0, -self.current_frame
        if self.current_direction == Direction.LEFT:
            return -self.current_frame, 0
        else:
            return 0, 0

    def world_to_grid(self):
        matrix = []
        for grid_x in range(len(self.world)):
            matrix.append([])
            for grid_y in range(len(self.world[grid_x])):
                if self.buildings[grid_x][grid_y] is None:
                    matrix[grid_x].append(0)
                elif str(self.buildings[grid_x][grid_y]) == "road":
                    matrix[grid_x].append(1)
                else:
                    matrix[grid_x].append(0)
        return matrix

    # return if nearby tiles are road or not
    def roadsAround(self, pos_x, pos_y):
        nearby_road = []  # array of nearby_road
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # directions = [(UP),(RIGHT),(DOWN),(LEFT)]
        # loop for check the different road nearby and append True or False in the array

        list_of_road = ["left_right_road", "top_bottom_road", "top_to_left_road", "top_to_right_road",
                        "bottom_to_right_road", "bottom_to_left_road", "right_bottom_left_road",
                        "top_bottom_left_road", "top_right_bottom_road", "top_right_left_road", "all_directions_road"]
        for dx, dy in directions:
            # manage out of range
            if pos_x + dx > len(self.world)-1:
                nearby_road.append(False)
            elif pos_y + dy > len(self.world)-1:
                nearby_road.append(False)
            elif (self.buildings[pos_x + dx][pos_y + dy] is not None) and (
                    self.buildings[pos_x + dx][pos_y + dy].name in list_of_road):
                nearby_road.append(True)
            else:
                nearby_road.append(False)
        return nearby_road

    # allow to workers to get the type of building on the next tile
    def continueToWalk(self):
        match self.current_direction.value:
            case 0:  # UP
                return self.get_building(int(self.pos_x), int(self.pos_y + 1))
            case 1:  # RIGHT
                return self.get_building(int(self.pos_x + 1), int(self.pos_y))
            case 2:  # DOWN
                return self.get_building(int(self.pos_x), int(self.pos_y - 1))
            case 3:  # LEFT
                return self.get_building(int(self.pos_x - 1), int(self.pos_y))
            case _:
                pass

    # function returning the type of building at location x, y
    def get_building(self, x, y):
        return self.buildings[x][y]

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return "basic_worker"


class Migrant(BasicWorker):
    def __init__(self, dest_x, dest_y, world, buildings, workers):
        self.created = False
        self.house_reached = False
        super().__init__(0, round(len(world)/2), world, buildings, workers)
        self.name = "basic_worker"
        self.path = self.pathSearch(dest_x, dest_y)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > 240 * self.tile_per_frame and self.created:
            self.move_timer = now
            self.go_to()

            if not self.path and not self.house_reached and self.pos_x == self.default_pos_x and self.pos_y == self.default_pos_y:
                for worker in self.workers[self.pos_x][self.pos_y]:
                    if worker is self:
                        self.workers[self.pos_x][self.pos_y].remove(self)
            # if the migrant reach his destination we delete it
            if not self.path and self in self.workers[self.pos_x][self.pos_y]:
                self.workers[self.pos_x][self.pos_y].remove(self)
                self.house_reached = True
        else:
            self.to_create()

    def to_create(self):
        if not self.created and len(self.workers[self.pos_x][self.pos_y]) < 1:
            self.workers[self.pos_x][self.pos_y].append(self)
            self.created = True

class Prefet(BasicWorker):
    def __init__(self, x, y, world, buildings, workers):
        super().__init__(x, y, world, buildings, workers)
        self.workers[x][y].append(self)


    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > 480 * self.tile_per_frame:
            self.move_timer = now
            if self.path:
                self.go_to()
            else:
                self.random_patrol()
            if self.current_frame == 0:
                self.stop_fire()

    def stop_fire(self):
        match (self.current_direction.value + 1) % 4:
            # Déplacements horizontaux
            case 0:
                if self.buildings[self.pos_x][self.pos_y+1] is not None:
                    self.buildings[self.pos_x][self.pos_y+1].burn_stage = 0
                    self.buildings[self.pos_x][self.pos_y + 1].burning
                if self.buildings[self.pos_x][self.pos_y-1] is not None:
                    self.buildings[self.pos_x][self.pos_y-1].burn_stage = 0
                    self.buildings[self.pos_x][self.pos_y - 1].burning = False
                if self.buildings[self.pos_x-1][self.pos_y+1] is not None:
                    self.buildings[self.pos_x-1][self.pos_y+1].burn_stage = 0
                    self.buildings[self.pos_x-1][self.pos_y + 1].burning = False
                if self.buildings[self.pos_x-1][self.pos_y-1] is not None:
                    self.buildings[self.pos_x-1][self.pos_y-1].burn_stage = 0
                    self.buildings[self.pos_x-1][self.pos_y - 1].burning = False
            case 2:
                if self.buildings[self.pos_x][self.pos_y + 1] is not None:
                    self.buildings[self.pos_x][self.pos_y + 1].burn_stage = 0
                    self.buildings[self.pos_x][self.pos_y + 1].burning = False
                if self.buildings[self.pos_x][self.pos_y - 1] is not None:
                    self.buildings[self.pos_x][self.pos_y - 1].burn_stage = 0
                    self.buildings[self.pos_x][self.pos_y - 1].burning = False
                if self.buildings[self.pos_x + 1][self.pos_y + 1] is not None:
                    self.buildings[self.pos_x + 1][self.pos_y + 1].burn_stage = 0
                    self.buildings[self.pos_x + 1][self.pos_y + 1].burning = False
                if self.buildings[self.pos_x + 1][self.pos_y - 1] is not None:
                    self.buildings[self.pos_x + 1][self.pos_y - 1].burn_stage = 0
                    self.buildings[self.pos_x+1][self.pos_y - 1].burning = False
            # Déplacements verticaux
            case 1:
                if self.buildings[self.pos_x+1][self.pos_y] is not None:
                    self.buildings[self.pos_x+1][self.pos_y].burn_stage = 0
                    self.buildings[self.pos_x+1][self.pos_y].burning
                if self.buildings[self.pos_x-1][self.pos_y] is not None:
                    self.buildings[self.pos_x-1][self.pos_y].burn_stage = 0
                    self.buildings[self.pos_x-1][self.pos_y].burning = False
                if self.buildings[self.pos_x - 1][self.pos_y + 1] is not None:
                    self.buildings[self.pos_x - 1][self.pos_y + 1].burn_stage = 0
                    self.buildings[self.pos_x - 1][self.pos_y + 1].burning = False
                if self.buildings[self.pos_x + 1][self.pos_y + 1] is not None:
                    self.buildings[self.pos_x + 1][self.pos_y + 1].burn_stage = 0
                    self.buildings[self.pos_x + 1][self.pos_y + 1].burning = False
            case 3:
                if self.buildings[self.pos_x-1][self.pos_y] is not None:
                    self.buildings[self.pos_x-1][self.pos_y].burn_stage = 0
                    self.buildings[self.pos_x-1][self.pos_y].burning = False
                if self.buildings[self.pos_x+1][self.pos_y] is not None:
                    self.buildings[self.pos_x+1][self.pos_y ].burn_stage = 0
                    self.buildings[self.pos_x+1][self.pos_y].burning = False
                if self.buildings[self.pos_x + 1][self.pos_y - 1] is not None:
                    self.buildings[self.pos_x + 1][self.pos_y - 1].burn_stage = 0
                    self.buildings[self.pos_x + 1][self.pos_y - 1].burning = False
                if self.buildings[self.pos_x - 1][self.pos_y - 1] is not None:
                    self.buildings[self.pos_x - 1][self.pos_y - 1].burn_stage = 0
                    self.buildings[self.pos_x - 1][self.pos_y - 1].burning = False