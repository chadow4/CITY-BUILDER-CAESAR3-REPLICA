import noise
import sys
import math
from .worker import *
from .buildings import *
from .graphic_scheduler import load_image, get_texture
from .settings import TILE_SIZE
from .Building.road import *
from .Building.house import *
from .Building.water_strcuture import *
from .Building.health_related import *
from .Building.prefecture import *

"""
World Class
"""


class World:
    # Constructor World Method
    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.perlin_scale = grid_length_x / 2

        self.workers: list[list[list[BasicWorker] | []]] = [[[] for x in range(self.grid_length_x)] for y in
                                                            range(self.grid_length_y)]
        self.buildings: list[list[Building | None]] = [[None for x in range(self.grid_length_x)] for y in
                                                       range(self.grid_length_y)]

        self.grass_tiles = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = load_image()
        self.world = self._create_world()

        self.temp_tile = None
        self.examine_tile = None
        self.start_pos = None
        self.end_pos = None
        self.mouse_action = None
        self.was_pressed_before = False
        self.keyOPressed = False
        self.keyOPressed_before = False

        self.miniMap = MiniMap(self.width * 0.168537, self.height * 0.2059777, self.buildings, self.grid_length_x,
                               self.grid_length_y, self.world)

    """
    ----------------------
    | cart_to_iso Method |
    ----------------------
 
        The function takes as input two real numbers x and y, which represent the Cartesian coordinates of a point. It 
        then calculates the isometric coordinates iso_x and iso_y of the point 
    """

    def _cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    """
    ------------------------
    | grid_to_world Method |
    ------------------------
     
        This method convert a pair of grid coordinates (grid_x, grid_y) to world coordinates, represented as an 
        isometric polygon. 
        
    """

    def _grid_to_world(self, grid_x, grid_y):
        # The method first creates a list rect of the four corner points of a rectangle with its top left corner at the
        # grid position (grid_x, grid_y) and sides of length TILE_SIZE.
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        # It then applies the _cart_to_iso method to each point in rect to convert the points from Cartesian
        # coordinates to isometric coordinates. The resulting list is stored in iso_poly.
        iso_poly = [self._cart_to_iso(x, y) for x, y in rect]
        # Finally, the method computes the minimum x and y values of the points in iso_poly, and generates a random
        # integer between 1 and 100. It also computes a value perlin using the Perlin noise function pnoise2
        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)
        texture_id = -1
        if self.buildings[grid_x][grid_y] is not None:
            tile = ""
        elif grid_x == 0 and grid_y == round(self.grid_length_y / 2) + 1:
            tile = "panel_start"
        elif grid_x == self.grid_length_x - 1 and grid_y == round(self.grid_length_y / 2) + 1:
            tile = "panel_exit"
        elif (perlin >= 35) or (perlin <= -40):
            tile = "water"
            texture_id = random.randint(0, 7)
        elif (perlin >= 20) or (perlin <= -30):
            tile = "tree"
            texture_id = random.randint(0, 34)
        else:
            if r == 1 or r == 2 or r == 3:
                tile = "tree"
                texture_id = random.randint(0, 34)
            elif r == 4:
                tile = "rock"
                texture_id = random.randint(0, 8)
            elif 15 < r < 17:
                tile = "field"
            else:
                tile = ""

        # add collision on the main road

        collision = False if tile == "" else True
        if grid_y == self.grid_length_y / 2:
            collision = True

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "texture_id": texture_id,
            "collision": collision
        }

        return out

    """
    ----------------------
    | cart_to_iso Method |
    ----------------------
    
        This function appears to create a world with grid made up of tiles. Each tile is represented by a dictionary 
        with a key "render_pos" that contains the rendering coordinates of the tile. 
        
    """

    def _create_world(self):
        # The function starts by initializing an empty list called "world". It then loops through the values of "grid_x"
        # from 0 to "self.grid_length_x" (inclusive) and, for each value of "grid_x", adds an empty list to "world".
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            # For each value of "grid_y" from 0 to "self.grid_length_y" (inclusive), the function calculates the
            # rendering coordinates of the corresponding tile using the "_grid_to_world" method. It then creates a
            # world tile using these rendering coordinates and adds it to the corresponding list in "world".
            for grid_y in range(self.grid_length_y):
                # If "grid_y" is equal to half of "self.grid_length_y", the function  create a "Road" object and add
                # it to the "self.buildings" dictionary at the corresponding position.
                if grid_y == round(self.grid_length_y / 2):
                    self.buildings[grid_x][grid_y] = Road(grid_x, grid_y, render_pos, self.resource_manager,
                                                          self.buildings)
                world_tile = self._grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]

                self.grass_tiles.blit(get_texture("grass"),
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        # return world which is a list of lists of world tiles.
        return world

    """
    -----------------
    | update Method |
    -----------------

      This function loads and returns images from files. It uses the pg library to load images and convert 
      their pixels with transparency. 

    """

    def update(self, camera):
        keys = pg.key.get_pressed()  # get keys Pressed
        mouse_pos = pg.mouse.get_pos()  # get mouse position
        mouse_action = pg.mouse.get_pressed()  # get if click is pressed

        # usefully for display the level of fire
        if keys[pg.K_o]:
            if not self.keyOPressed_before:
                if self.keyOPressed:
                    self.keyOPressed = False
                else:
                    self.keyOPressed = True
                self.keyOPressed_before = True
        else:
            self.keyOPressed_before = False

        if mouse_action[2]:  # right click action
            self.hud.selected_tile = None
            self.examine_tile = None
            self.hud.examined_tile = None

        self.temp_tile = None

        # if one button in hud is selected
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            # if the mouse is out of the map
            if grid_pos[0] > self.grid_length_x - 1:
                grid_pos = self.grid_length_x - 1, grid_pos[1]
            if grid_pos[1] > self.grid_length_y - 1:
                grid_pos = grid_pos[0], self.grid_length_y - 1
            if grid_pos[0] < 0:
                grid_pos = 0, grid_pos[1]
            if grid_pos[1] < 0:
                grid_pos = grid_pos[0], 0
            # if we can place tile
            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()  # get image of selected button in HUD
                img.set_alpha(100)
                # if (0 < grid_pos[0] < self.grid_length_x-1) and (0 < grid_pos[1] < self.grid_length_y-1):
                building = self.buildings[grid_pos[0]][grid_pos[1]]  # set building with coordinate of object
                if mouse_action[0] and (building is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building

                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision,
                    "road": None
                }
                # if right button clicked
                if not self.was_pressed_before and mouse_action[0]:
                    self.was_pressed_before = True  # set was pressed to True
                    self.start_pos = grid_pos  # set start position at current pos
                    self.end_pos = grid_pos  # set end position at current pos
                # if right button not clicked
                if self.was_pressed_before and not mouse_action[0]:
                    self.was_pressed_before = False  # set was pressed to False
                    self.end_pos = grid_pos  # set end position at current pos for manage the multiple layout
                    # get value of start_x, end_x, start_y and end_y
                    start_x = min(self.start_pos[0], self.end_pos[0])
                    end_x = max(self.start_pos[0], self.end_pos[0])
                    start_y = min(self.start_pos[1], self.end_pos[1])
                    end_y = max(self.start_pos[1], self.end_pos[1])
                    # get coordinates where a road would be built
                    road_pos = self.start_pos[0], self.end_pos[1]

                    # pose multiple
                    while start_x <= end_x:
                        while start_y <= end_y:
                            render_pos = self.world[start_x][start_y][
                                "render_pos"]  # get render position for all x,y selected
                            collision = self.world[start_x][start_y]["collision"]  # get collision for all x,y selected
                            self.temp_tile["render_pos"] = render_pos

                            if not collision:
                                # select road button in HUD
                                if self.hud.selected_tile["name"] == "road" and (
                                        start_x == road_pos[0] or start_y == road_pos[1]):
                                    ent = Road(start_x, start_y, render_pos, self.resource_manager,
                                               self.buildings)  # create object Road
                                    ############################
                                    road = self.roadsAround(start_x, start_y)
                                    if any(road):
                                        x, y = start_x, start_y

                                        # une route en BAS (marche)
                                        if road[0]:
                                            if self.buildings[x][y + 1].name == "left_right_road":
                                                if self.buildings[x + 1][y + 1] is None:
                                                    self.buildings[x][y + 1].set_name("bottom_to_left_road")
                                                elif self.buildings[x - 1][y + 1] is None:
                                                    self.buildings[x][y + 1].set_name("bottom_to_right_road")
                                                else:
                                                    self.buildings[x][y + 1].set_name("top_right_left_road")
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y + 1].name == "right_bottom_left_road":
                                                self.buildings[x][y + 1].set_name("all_directions_road")
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y + 1].name == "top_bottom_road":
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y + 1].name == "top_to_right_road":
                                                self.buildings[x][y + 1].set_name("top_bottom_left_road")
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y + 1].name == "top_to_left_road":
                                                self.buildings[x][y + 1].set_name("top_right_bottom_road")

                                        #
                                        # # # une route à gauche
                                        if road[1]:
                                            if self.buildings[x + 1][y].name == "top_bottom_road":
                                                if self.buildings[x + 1][y - 1] is None:
                                                    self.buildings[x + 1][y].set_name("top_to_right_road")
                                                elif self.buildings[x + 1][y + 1] is None:
                                                    self.buildings[x + 1][y].set_name("bottom_to_left_road")
                                                else:
                                                    self.buildings[x + 1][y].set_name("top_bottom_left_road")
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x + 1][y].name == "top_right_bottom_road":  # a verifier
                                                self.buildings[x + 1][y].set_name("all_directions_road")
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x + 1][y].name == "left_right_road":
                                                ent.set_name("left_right_road")
                                            # a verifier pour les courbures
                                            elif self.buildings[x + 1][y].name == "bottom_to_right_road":
                                                self.buildings[x + 1][y].set_name("top_right_left_road")
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x + 1][y].name == "top_to_left_road":
                                                self.buildings[x + 1][y].set_name("right_bottom_left_road")
                                                ent.set_name("left_right_road")

                                        # # une route en haut (marche)
                                        if road[2]:
                                            if self.buildings[x][y - 1].name == "left_right_road":
                                                if self.buildings[x + 1][y - 1] is None:
                                                    self.buildings[x][y - 1].set_name("top_to_right_road")
                                                elif self.buildings[x - 1][y - 1] is None:
                                                    self.buildings[x][y - 1].set_name("top_to_left_road")
                                                else:
                                                    self.buildings[x][y - 1].set_name("right_bottom_left_road")
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y - 1].name == "top_right_left_road":
                                                self.buildings[x][y - 1].set_name("all_directions_road")
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y - 1].name == "top_bottom_road":
                                                ent.set_name("top_bottom_road")
                                            # a verifier
                                            elif self.buildings[x][y - 1].name == "bottom_to_left_road":
                                                self.buildings[x][y - 1].set_name("top_bottom_left_road")  # a verifier
                                                ent.set_name("top_bottom_road")
                                            elif self.buildings[x][y - 1].name == "bottom_to_right_road":
                                                self.buildings[x][y - 1].set_name("top_right_bottom_road")  # a verifier
                                                ent.set_name("top_bottom_road")

                                        # # # une route à droite
                                        if road[3]:
                                            if self.buildings[x - 1][y].name == "top_bottom_road":
                                                if self.buildings[x - 1][y - 1] is None:
                                                    self.buildings[x - 1][y].set_name("top_to_left_road")
                                                elif self.buildings[x - 1][y + 1] is None:
                                                    self.buildings[x - 1][y].set_name("bottom_to_right_road")
                                                else:
                                                    self.buildings[x - 1][y].set_name(
                                                        "top_right_bottom_road")  # a verifier
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x - 1][y].name == "top_bottom_left_road":
                                                self.buildings[x - 1][y].set_name("all_directions_road")
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x - 1][y].name == "left_right_road":
                                                ent.set_name("left_right_road")
                                            # a verifier pour les courbures
                                            elif self.buildings[x - 1][y].name == "bottom_to_left_road":
                                                self.buildings[x - 1][y].set_name("top_right_left_road")
                                                ent.set_name("left_right_road")
                                            elif self.buildings[x - 1][y].name == "top_to_right_road":
                                                self.buildings[x - 1][y].set_name("top_right_left_road")
                                                ent.set_name("left_right_road")
                                    ############################
                                    ent.resource_manager.apply_cost_to_resource("road")  # calculate cost of Road
                                    # self.entities.append(ent) desactivation car probleme lors du entities.remove
                                    self.buildings[start_x][start_y] = ent
                                    self.world[start_x][start_y]["road"] = True
                                # select house button in HUD
                                elif self.hud.selected_tile["name"] == "house":
                                    ent = House(start_x, start_y, render_pos, self.resource_manager, self.buildings,
                                                self.entities, self.world)  # create object House
                                    self.entities.append(ent)  # append object in list of entities placed on map
                                    self.buildings[start_x][start_y] = ent
                                    # creation of workers
                                    road = self.roadsAround(start_x, start_y)
                                    if any(road):
                                        x, y = start_x, start_y  # road position
                                        for index, isRoad in enumerate(road):
                                            if isRoad:
                                                if index % 2 == 0:
                                                    y += 1 - index
                                                    break
                                                elif index % 2 != 0:
                                                    x += 2 - index
                                                    break
                                        ent = Migrant(x, y, self.world, self.buildings, self.workers)
                                        ent.valid_tiles = self.roadsAround(x, y)
                                        # We add him only if the house is connected to the road
                                        if ent.path:
                                            self.entities.append(ent)
                                            self.buildings[start_x][start_y].worker = ent
                                elif self.hud.selected_tile["name"] == "well":
                                    ent = Well(render_pos, self.resource_manager)  # create object Well
                                    self.entities.append(ent)  # append object in list of entities placed on map
                                    self.buildings[start_x][start_y] = ent
                                elif self.hud.selected_tile["name"] == "barber":
                                    ent = Barber(render_pos, self.resource_manager)  # create object Well
                                    self.entities.append(ent)  # append object in list of entities placed on map
                                    self.buildings[start_x][start_y] = ent

                                elif self.hud.selected_tile["name"] == Prefecture.name:
                                    ent = Prefecture(start_x, start_y, render_pos, self.resource_manager,
                                                     self.buildings, self.entities,
                                                     self.world)  # create object Prefecture
                                    self.entities.append(ent)  # append object in list of entities placed on map
                                    self.buildings[start_x][start_y] = ent
                                    # creation of workers
                                    road = self.roadsAround(start_x, start_y)
                                    if any(road):
                                        x, y = start_x, start_y  # road position
                                        for index, isRoad in enumerate(road):
                                            if isRoad:
                                                if index % 2 == 0:
                                                    y += 1 - index
                                                    break
                                                elif index % 2 != 0:
                                                    x += 2 - index
                                                    break
                                        ent = Prefet(x, y, self.world, self.buildings, self.workers)
                                        ent.valid_tiles = self.roadsAround(x, y)
                                        self.entities.append(ent)
                                        self.buildings[start_x][start_y].worker = ent
                                if self.buildings[start_x][start_y] is not None:
                                    self.world[start_x][start_y]["collision"] = True  # set collision to True

                            # select shovel button in HUD
                            if self.hud.selected_tile["name"] == "shovel":
                                # Delete terrain element
                                if (self.world[start_x][start_y]["tile"] == "tree") or (
                                        self.world[start_x][start_y]["tile"] == "rock"):
                                    self.resource_manager.apply_cost_to_resource("shovel")
                                    self.world[start_x][start_y]["tile"] = ""
                                    self.world[start_x][start_y]["collision"] = False  # set collision to False
                                # Forbid the clear of the main road
                                elif self.world[start_x][start_y]["tile"] != "water" or self.world[start_x][start_y][
                                    "tile"] != "panel_start":
                                    # if building in list of entities placed on map
                                    if self.buildings[start_x][start_y] in self.entities:
                                        # delete the worker
                                        if self.buildings[start_x][start_y].worker is not None:
                                            obj = self.buildings[start_x][start_y].worker
                                            # Allow to erase a migrant only if it has not reach his house
                                            if self.buildings[start_x][start_y].name == "housePanel" or str(
                                                    self.buildings[start_x][start_y]) != "house":
                                                self.workers[obj.pos_x][obj.pos_y].remove(obj)
                                            self.entities.remove(obj)
                                            print("L'objet", obj, "a été supprimé")
                                        self.entities.remove(
                                            self.buildings[start_x][start_y])  # remove building in list of entities
                                        print("L'objet", self.buildings[start_x][start_y], "a été supprimé")
                                        self.resource_manager.apply_cost_to_resource("shovel")
                                    self.buildings[start_x][start_y] = None
                                    self.world[start_x][start_y]["collision"] = False  # set collision to False
                            start_y += 1
                        start_x += 1
                        start_y = min(self.start_pos[1], self.end_pos[1])
                    # self.hud.selected_tile = None
                    self.start_pos = None
        self.miniMap.update(self.buildings, camera)

    """
    ------------------------
    | mouse_to_grid Method |
    ------------------------

       This function transforms the mouse coordinates (x, y) into grid coordinates. It uses the camera scroll 
       value "scroll" and the tile dimensions "TILE_SIZE". 
             
    """

    def mouse_to_grid(self, x, y, scroll):
        # The function first transforms the mouse coordinates (x, y) into world coordinates by removing the camera
        # scroll and an offset of "self.grass_tiles.get_width() / 2".
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # It then transforms these world coordinates into Cartesian coordinates using inverse formulas to those used
        # in the "cart_to_iso" function.
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # Finally, the function transforms the Cartesian coordinates into grid coordinates by dividing each of them
        # by the tile size "TILE_SIZE" and taking the integer part of the result. It returns the grid coordinates as
        # a pair (grid_x, grid_y)
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    """
    ---------------
    | draw Method |
    ---------------

       This function loads and returns images from files. It uses the pg library to load images and convert 
       their pixels with transparency. 

    """

    def draw(self, screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                # draw world tiles
                tile = self.world[x][y]["tile"]
                if tile == "pannel_start" or tile == "pannel_exit":
                    texture = get_texture(tile)
                    screen.blit(texture,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (texture.get_height() - TILE_SIZE) + camera.scroll.y))
                if tile != "":
                    texture = get_texture(tile, self.world[x][y]["texture_id"])
                    screen.blit(texture,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (texture.get_height() - TILE_SIZE) + camera.scroll.y))

                # draw buildings
                building = self.buildings[x][y]

                # Hide building if key "o" is pressed and display the fire's levels
                if self.keyOPressed and str(building) != "road":
                    if building and building.name != "housePanel":
                        image = get_texture("level_fire_floor")
                        screen.blit(image,
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                        if building.burn_stage > 0:
                            image = get_texture("level_fire_base")
                            screen.blit(image,
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                         render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                            # increase height of fire
                            if building.burn_stage > 1:
                                dy = -20  # 20
                                dx = -4
                                roof = get_texture("level_fire_roof")
                                wall = get_texture("level_fire_wall")

                                for i in range(building.burn_stage - 2):
                                    screen.blit(wall,
                                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + 8,
                                                 render_pos[1] - (
                                                             wall.get_height() - TILE_SIZE) + camera.scroll.y + dy))
                                    dy -= 10

                                screen.blit(roof,
                                            (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + dx,
                                             render_pos[1] - (roof.get_height() - TILE_SIZE) + camera.scroll.y + dy))

                else:
                    if building:
                        image = get_texture(building.name)
                        if building.burning:
                            image = get_texture("house_fire")
                        screen.blit(image,
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                        if self.examine_tile:
                            if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                                mask = pg.mask.from_surface(image).outline()
                                mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                         y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                        for x, y in mask]
                                pg.draw.polygon(screen, (255, 255, 255), mask, 3)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 4)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 4)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )
        self.miniMap.show(screen, pos=(self.width * 0.8210888, self.height * 0.08781))

    def draw_worker(self, screen, camera):
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                # draw workers
                for worker in self.workers[x][y]:
                    # if worker is not None:
                    image = get_texture(worker.name + str(worker.current_direction.value) + str(worker.current_frame))
                    # on déplace le walker d'1/12 de case
                    dx, dy = worker.mini_move()
                    dx, dy = self._cart_to_iso(dx, dy)
                    screen.blit(image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + 15 + dx * (
                                        TILE_SIZE / 12),
                                 render_pos[1] - (
                                         image.get_height() - TILE_SIZE) + camera.scroll.y + dy * (
                                         TILE_SIZE / 12)))

    """
    -------------------------
    | can_place_tile Method |
    -------------------------

        This function check if a tile can be placed at a given grid position. It takes a grid position as an input, 
        which is a tuple (grid_x, grid_y) of integers. 
        
    """

    def can_place_tile(self, grid_pos):
        # The function checks if the mouse cursor is currently hovering over any of the rectangles in the list [
        # elf.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]. If the mouse is hovering over any of
        # these rectangles, the function sets "mouse_on_panel" to True.
        mouse_on_panel = False
        # The function also checks if the grid position is within the bounds of the world grid, which are defined as 0
        # <= grid_x <= self.grid_length_x and 0 <= grid_y <= self.grid_length_x. If the grid position is within these
        # bounds, the function sets "world_bounds" to True.
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)
        # If both "world_bounds" and "mouse_on_panel" are True, the function returns False. Otherwise, it returns True.
        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

    """
    -----------------------
    | get_building Method |
    -----------------------

        This function returning the type of building at location x, y
        """

    # function returning the type of building at location x, y
    def get_building(self, x, y):
        return self.buildings[x][y]

    # return if nearby tiles are road or not
    def roadsAround(self, pos_x, pos_y):
        nearby_road = []  # array of nearby_road
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # directions = [(UP),(RIGHT),(DOWN),(LEFT)]
        # loop for check the different road nearby and append True or False in the array

        list_of_road = ["left_right_road", "top_bottom_road", "top_to_left_road", "top_to_right_road",
                        "bottom_to_right_road", "bottom_to_left_road", "right_bottom_left_road", "top_bottom_left_road",
                        "top_right_bottom_road", "top_right_left_road", "all_directions_road"]
        for dx, dy in directions:
            # manage out of range
            if pos_x + dx > self.grid_length_x - 1:
                nearby_road.append(False)
            elif pos_y + dy > self.grid_length_y - 1:
                nearby_road.append(False)
            elif (self.buildings[pos_x + dx][pos_y + dy] is not None) and (
                    self.buildings[pos_x + dx][pos_y + dy].name in list_of_road):
                nearby_road.append(True)
            else:
                nearby_road.append(False)
        return nearby_road


class MiniMap:
    rect_dragging = False

    def __init__(self, width, height, buildings, grid_length_x, grid_length_y, world):
        self.camera_pos = None
        self.camera = None
        self.grid_length_y = grid_length_y
        self.grid_length_x = grid_length_x
        self.width = width
        self.height = height
        self.buildings = buildings
        self.world = world
        self.rect_pos = [0, 0]
        self.is_changed = False
        self.full_map_surface = pg.Surface((self.width, self.height))

    def show(self, screen, pos):


        grass_color = (78, 106, 27)

        mini_size = int(self.height / (60*math.sqrt(2)))

        surface = pg.Surface((60 * mini_size, 60 * mini_size))
        center_point = (30 * mini_size, 30 * mini_size)
        if self.rect_pos[0] == 0:
            self.rect_pos = [(self.width-60*mini_size*math.sqrt(2))/2, (self.height-60*mini_size*math.sqrt(2))/2+self.height*0.14]

        # mini tree
        tree_color = (59, 81, 6)
        rock_color = (184, 166, 135)
        # mini_road
        road_color = (173, 151, 129)
        # mini_water
        water_color = (51, 65, 123)
        house_color = (195, 95, 75)
        prefecture_color = (166, 93, 70)
        engineers_Post_color = (54, 55, 52)

        for i in range(self.grid_length_x):
            for j in range(self.grid_length_y):
                pos_x = center_point[0] - (30 - i) * mini_size
                pos_y = center_point[1] - (30 - j) * mini_size
                rect = pg.Rect(pos_x, pos_y, mini_size, mini_size)
                pg.draw.rect(surface, grass_color, rect)

                tile = self.world[i][j]["tile"]
                if tile == "water":
                    pg.draw.rect(surface, water_color, rect)
                if tile == "tree":
                    pg.draw.rect(surface, tree_color, rect)
                if tile == "rock":
                    pg.draw.rect(surface, rock_color, rect)

        for i in range(len(self.buildings)):
            for j in range(len(self.buildings[i])):
                pos_x = center_point[0] - (30 - i) * mini_size
                pos_y = center_point[1] - (30 - j) * mini_size
                match self.buildings[i][j]:
                    case Road():
                        pg.draw.rect(surface, road_color, pg.Rect(pos_x, pos_y, mini_size, mini_size))
                    case Prefecture():
                        pg.draw.rect(surface, prefecture_color, pg.Rect(pos_x, pos_y, mini_size, mini_size))
                    case House():
                        pg.draw.rect(surface, house_color, pg.Rect(pos_x, pos_y, mini_size, mini_size))
                    case Engineers_Post():
                        pg.draw.rect(surface, engineers_Post_color, pg.Rect(pos_x, pos_y, mini_size, mini_size))

        surface = pg.transform.rotate(surface, -45)
        rotated_surface_rect = surface.get_rect()
        rotated_surface_rect.center = center_point
        self.full_map_surface.blit(surface, ((self.width - 60 * mini_size * math.sqrt(2)) / 2, (self.height - 60 * mini_size * math.sqrt(2)) / 2))
        self.draw_rectangle(screen, pos)
        screen.blit(self.full_map_surface, pos)

    def draw_rectangle(self, screen, pos):
        # Draw scrolling rectangle
        rect_color = (255, 255, 5)
        rect_width = 1
        rect_size = ((1080 / 1728) * (self.width / 2.5), (1080 / 1728) * (self.width / 2.5))
        # print(self.rect_pos)
        rect_x = self.rect_pos[0] - rect_width / 2
        rect_y = self.rect_pos[1] - rect_width / 2

        mini_rec = pg.Rect((rect_x, rect_y), rect_size)
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if ((self.width * 4.871860778 < mouse_pos[0] and mouse_pos[0] < self.width * 5.864741427) and (self.height * 0.9350167159 > mouse_pos[1] and mouse_pos[1] > self.height * 0.427050939)):
                if event.type == pg.MOUSEBUTTONDOWN:

                # print("mous1", mouse_pos[1])
                # print("mous 0", mouse_pos[0])
                    self.rect_dragging = True

                elif event.type == pg.MOUSEBUTTONUP:
                    print("Hello DARK WORLD")
                    self.is_changed = True
                    self.rect_pos[0] = mouse_pos[0] - rect_size[0] / 2 - self.width * 4.871860778
                    self.rect_pos[1] = mouse_pos[1] - rect_size[1] / 2 - self.height * 0.4263082848
                    self.rect_dragging = False

                elif event.type == pg.MOUSEMOTION:

                    if self.rect_dragging:
                        self.rect_pos[0] = mouse_pos[0] - rect_size[0] / 2 - self.width * 4.871860778
                        self.rect_pos[1] = mouse_pos[1] - rect_size[1] / 2 - self.height * 0.4263082848
                        self.is_changed = True
        pg.draw.rect(self.full_map_surface, rect_color, mini_rec, rect_width)

    def update(self, buildings, camera):
        self.buildings = buildings.copy()
        self.full_map_surface = pg.Surface((self.width, self.height))
        self.async_cam_mini(camera=self.camera)
    def async_cam_mini(self, camera):
        A_y = ((1080 / 1728) * (self.width / 2.5) - 60 * int(self.height / (60 * math.sqrt(2))) * math.sqrt(2)) / 750
        B_y = (self.height - 60 * int(self.height / (60 * math.sqrt(2))) * math.sqrt(2)) / 2 - A_y * 30
        A_x = ((1080 / 1728) * (self.width / 2.5) - 60 * int(self.height / (60 * math.sqrt(2))) * math.sqrt(2)) / 1890
        B_x = (self.width - 60 * int(self.height / (60 * math.sqrt(2))) * math.sqrt(2)) / 2 - A_y * 0
        if self.is_changed:
            camera.scroll.x = (self.rect_pos[0]-B_x)/A_x
            camera.scroll.y = (self.rect_pos[1]-B_y)/A_y
            self.is_changed = False
            return
        else:
            # print(camera.scroll.x)
            # print(camera.scroll.y)
            # self.rect_pos[0] -= camera.dx/7
            self.rect_pos[0] = A_x*camera.scroll.x+B_x
            self.rect_pos[1] = A_y*camera.scroll.y+B_y
