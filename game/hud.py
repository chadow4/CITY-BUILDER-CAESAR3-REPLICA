import pygame as pg

from .utils import draw_text
from .graphic_scheduler import get_texture
from .buildings import *
from .Building.health_related import *
from .Building.religious_structure import *
from .Building.water_strcuture import *
from .Building.road import *
from .Building.house import *
from .Building.prefecture import *

class Hud:

    def __init__(self, resource_manager, width, height):
        self.resource_manager = resource_manager
        self.width = width
        self.height = height
        self.backgroundPanelRessource = pg.image.load("assets/graphics/Hud/paneling_00001.png").convert_alpha()
        self.backgroundPanelRessource2 = pg.image.load("assets/graphics/Hud/paneling_00015.png").convert_alpha()

        self.backgroundPanelObject = pg.image.load("assets/graphics/Hud/paneling_00017.png").convert_alpha()
        self.backgroundPanelObject2 = pg.image.load("assets/graphics/Hud/paneling_00019.png").convert_alpha()
        self.backgroundPanelObject3 = pg.image.load("assets/graphics/Hud/paneling_00018.png").convert_alpha()
        self.backgroundPanelObject4 = pg.image.load("assets/graphics/Hud/paneling_00097.png").convert_alpha()
        self.backgroundPanelObject5 = pg.image.load("assets/graphics/Hud/paneling_00080.png").convert_alpha()
        self.backgroundPanelObject6 = pg.image.load("assets/graphics/Hud/paneling_00082.png").convert_alpha()
        self.backgroundPanelObject7 = pg.image.load("assets/graphics/Hud/paneling_00085.png").convert_alpha()
        self.backgroundPanelObject8 = pg.image.load("assets/graphics/Hud/paneling_00088.png").convert_alpha()
        self.backgroundPanelObject9 = pg.image.load("assets/graphics/Hud/paneling_00091.png").convert_alpha()
        self.backgroundPanelObject10 = pg.image.load("assets/graphics/Hud/paneling_00094.png").convert_alpha()
        self.hud_colour = (198, 155, 93, 175)
        self.buttons = Buttons()

        # resouces hud
        self.resouces_surface = pg.Surface((width, height * 0.1), pg.SRCALPHA)
        self.resources_rect = self.resouces_surface.get_rect(topleft=(0, 0))
        count = 0
        ranged = self.width // 24
        #print(ranged)
        for i in range(ranged):
            self.resouces_surface.blit(self.backgroundPanelRessource, (count, 0))
            count += 24

        # building hud
        self.build_surface = pg.Surface((width * 0.2, height), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

    def create_build_hud(self):

        render_pos = [self.width * 0.827546, self.height * 0.537963]

        object_width = self.width * 0.043402778
        distance_height = self.height * 0.0669245
        tiles = []
        count = 0
        for image_name, image in self.images.items():
            pos = render_pos.copy()

            # Some specific custom for prefecture cuz we have not complete all of button
            if image_name == "prefecture":
                pos = [self.width*85/96, self.height*0.737037]

            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )
            count += 1
            render_pos[0] += 0.057716 * self.width
            if count == 3:
                render_pos[0] -= 3 * 0.057716 * self.width
                render_pos[1] += distance_height



        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        #if mouse_action[0]: print("Mouse pos: ", mouse_pos[0], mouse_pos[1], sep=" ")
        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        # resouce hud
        screen.blit(self.resouces_surface, (0, 0))

        # build hud
        IngameMenu().show(screen)
        # select hud
        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img = get_texture(self.examined_tile.name).copy()
            img_scale = self.scale_image(img, h=h * 0.7)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), self.select_rect.topleft)

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)

        # resources
        pos = self.width - 400
        txt = "Dn     " + str(self.resource_manager.resources)
        draw_text(screen, txt, 23, (255, 255, 255), (pos, 5))
        pos += 100
        self.resouces_surface.blit(self.backgroundPanelRessource2, (1285, 0))  # background for pop
        self.resouces_surface.blit(self.backgroundPanelRessource2, (self.width - 413, 0))  # background for Deniers
        self.resouces_surface.blit(self.backgroundPanelRessource2, (1775, 0))  # background for FPS

        self.buttons.screen = screen
        self.buttons.update()

    def load_images(self):

        # read images
        shovel = pg.image.load("assets/graphics/Hud/paneling_00131.png").convert_alpha()

        images = {
            Road.name: pg.image.load("assets/graphics/Hud/paneling_00135.png").convert_alpha(),
            House.name: pg.image.load("assets/graphics/buildings/house/house_lv0.png"),
            "shovel": shovel,
            Well.name: Well.image,
            Barber.name: Barber.image,
            Ceres.name: Ceres.image,
            Prefecture.name: pg.image.load("assets/graphics/buildings/prefecture.png").convert_alpha()
        }

        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image


class IngameMenu:
    def __init__(self):
        self.backgroundPanelObject = [
            pg.image.load("assets/graphics/Hud/paneling_00017.png").convert_alpha(),  # [0]
            pg.image.load("assets/graphics/Hud/paneling_00234.png").convert_alpha(),  # [1] overlay background
            pg.image.load("assets/graphics/Hud/paneling_00097.png").convert_alpha(),  # [2] arrow symbol
            pg.image.load("assets/graphics/Hud/paneling_00080.png").convert_alpha(),  # [3]
            pg.image.load("assets/graphics/Hud/paneling_00082.png").convert_alpha(),  # [4]
            pg.image.load("assets/graphics/Hud/paneling_00085.png").convert_alpha(),  # [5]
            pg.image.load("assets/graphics/Hud/paneling_00088.png").convert_alpha(),  # [6]
            pg.image.load("assets/graphics/Hud/paneling_00091.png").convert_alpha(),  # [7]
            pg.image.load("assets/graphics/Hud/paneling_00094.png").convert_alpha(),  # [8]
            pg.image.load("assets/graphics/Hud/panelwindows_00013.png").convert_alpha(),  # [9]
            pg.image.load("assets/graphics/Hud/paneling_00135.png").convert_alpha(),  # 10]
            pg.image.load("assets/graphics/Hud/paneling_00123.png").convert_alpha(),  # [11]
            pg.image.load("assets/graphics/Hud/paneling_00131.png").convert_alpha(),  # [12]
            pg.image.load("assets/graphics/Hud/paneling_00127.png").convert_alpha(),  # [13]
            pg.image.load("assets/graphics/Hud/paneling_00163.png").convert_alpha(),  # [14]
            pg.image.load("assets/graphics/Hud/paneling_00151.png").convert_alpha(),  # [15]
            pg.image.load("assets/graphics/Hud/paneling_00147.png").convert_alpha(),  # [16]
            pg.image.load("assets/graphics/Hud/paneling_00143.png").convert_alpha(),  # [17]
            pg.image.load("assets/graphics/Hud/paneling_00139.png").convert_alpha(),  # [18]
            pg.image.load("assets/graphics/Hud/paneling_00167.png").convert_alpha(),  # [19]
            pg.image.load("assets/graphics/Hud/paneling_00159.png").convert_alpha(),  # [20]
            pg.image.load("assets/graphics/Hud/paneling_00155.png").convert_alpha(),  # [21]
            pg.image.load("assets/graphics/Hud/paneling_00174.png").convert_alpha(),  # [22]
            pg.image.load("assets/graphics/Hud/paneling_00118.png").convert_alpha(),  # [23]
            pg.image.load("assets/graphics/Hud/paneling_00122.png").convert_alpha(),  # [24]
            pg.image.load("assets/graphics/Hud/paneling_00018.png").convert_alpha()  # [25]
        ]

    def show(self, screen):
        for i in range(len(self.backgroundPanelObject) - 1):
            self.backgroundPanelObject[i] = self._scale_img(self.backgroundPanelObject[i])

        width = pg.display.get_surface().get_width()
        height = pg.display.get_surface().get_height()
        menu_width = width * 0.188
        menu_height = height * 0.977
        surface = pg.Surface((menu_width, menu_height), pg.SRCALPHA)
        surface.blit(self.backgroundPanelObject[0], (0, 0))  # Menu de droite

        # element statiques du menu
        surface.blit(self.backgroundPanelObject[1], (menu_width * 0.027, menu_height * 0.0065))  # overlay background
        surface.blit(self.backgroundPanelObject[2],
                     (menu_width * 0.783, menu_height * 0.01))  # 2eme boutton ==> 1ere ligne de bouton
        surface.blit(self.backgroundPanelObject[3],
                     (menu_width * 0.045, menu_height * 0.2945))  # 1er boutton ==> 2eme ligne de bouton
        surface.blit(self.backgroundPanelObject[4],
                     (menu_width * 0.520, menu_height * 0.2945))  # 2eme bouton ==> 2eme ligne de bouton
        surface.blit(self.backgroundPanelObject[5],
                     (menu_width * 0.045, menu_height * 0.349))  # 1er bouton ==> 3eme ligne de bouton
        surface.blit(self.backgroundPanelObject[6],
                     (menu_width * 0.285, menu_height * 0.349))  # 2eme bouton ==> 3eme ligne de bouton
        surface.blit(self.backgroundPanelObject[7],
                     (menu_width * 0.520, menu_height * 0.349))  # 3eme bouton ==> 3eme ligne de bouton
        surface.blit(self.backgroundPanelObject[8],
                     (menu_width * 0.760, menu_height * 0.349))  # 4eme bouton ==> 4eme ligne de bouton
        surface.blit(self.backgroundPanelObject[9], (menu_width * 0.045, menu_height * 0.407))
        surface.blit(self.backgroundPanelObject[10], (menu_width * 0.083, menu_height * 0.5255))  # Road button
        surface.blit(self.backgroundPanelObject[11], (menu_width * 0.390, menu_height * 0.5255))  # Housing button
        surface.blit(self.backgroundPanelObject[12],
                     (menu_width * 0.698, menu_height * 0.5255))  # Delete terrain button
        surface.blit(self.backgroundPanelObject[13],
                     (menu_width * 0.083, menu_height * 0.5935))  # Water structure button
        surface.blit(self.backgroundPanelObject[14],
                     (menu_width * 0.390, menu_height * 0.5935))  # Health-related structure button
        surface.blit(self.backgroundPanelObject[15],
                     (menu_width * 0.698, menu_height * 0.5935))  # Religion structure button
        surface.blit(self.backgroundPanelObject[16],
                     (menu_width * 0.083, menu_height * 0.6620))  # Education structure button
        surface.blit(self.backgroundPanelObject[17],
                     (menu_width * 0.390, menu_height * 0.6620))  # Entertainment structure button
        surface.blit(self.backgroundPanelObject[18],
                     (menu_width * 0.698, menu_height * 0.6620))  # Religion structure button
        surface.blit(self.backgroundPanelObject[19], (menu_width * 0.083, menu_height * 0.7305))
        surface.blit(self.backgroundPanelObject[20], (menu_width * 0.390, menu_height * 0.7305))
        surface.blit(self.backgroundPanelObject[21], (menu_width * 0.698, menu_height * 0.7305))
        surface.blit(self.backgroundPanelObject[22], (menu_width * 0.083, menu_height * 0.7990))
        surface.blit(self.backgroundPanelObject[23], (menu_width * 0.390, menu_height * 0.7990))
        surface.blit(self.backgroundPanelObject[24], (menu_width * 0.698, menu_height * 0.7990))

        self.backgroundPanelObject[25] = pg.transform.scale(self.backgroundPanelObject[25], (menu_width, (
                    menu_width / self.backgroundPanelObject[25].get_width()) * self.backgroundPanelObject[
                                                                                                 25].get_height()))
        surface.blit(self.backgroundPanelObject[25],
                     (0, self.backgroundPanelObject[0].get_height()))  # Religion structure button
        screen.blit(surface, (width - menu_width, height - menu_height))

    def _scale_img(self, img):
        witdh, height = img.get_width(), img.get_height()
        return pg.transform.scale(img, (witdh * 2 * pg.display.get_surface().get_width() / 1728,
                                        height * 2 * pg.display.get_surface().get_height() / 1080))


class Buttons:
    def __init__(self, screen=None):
        self.screen = screen
        self.backgroundPanelObject = []
        self.load_images()
        self.chosenButton = None
        self.isChosen = False

    def load_images(self):
        self.backgroundPanelObject.append(pg.image.load("assets/graphics/Hud/file.png").convert_alpha())
        self.backgroundPanelObject.append(pg.image.load("assets/graphics/Hud/option.png").convert_alpha())
        self.backgroundPanelObject.append(pg.image.load("assets/graphics/Hud/help.png").convert_alpha())
        self.backgroundPanelObject.append(pg.image.load("assets/graphics/Hud/advisor.png").convert_alpha())
        for i in range(len(self.backgroundPanelObject)):
            original_width = self.backgroundPanelObject[i].get_width()
            original_height = self.backgroundPanelObject[i].get_height()
            self.backgroundPanelObject[i] = pg.transform.scale(self.backgroundPanelObject[i],
                                                               (original_width / 3, original_height / 3))

        """
        images = {
            "file": file,
            "option": option,
            "help": help,
            "advisor": advisor
        }

        return images
        """

    def draw(self):
        button_surface = pg.Surface((self.backgroundPanelObject[self.chosenButton].get_width(),
                                     self.backgroundPanelObject[self.chosenButton].get_height()))
        button_surface.blit(self.backgroundPanelObject[self.chosenButton], (0, 0))
        if self.chosenButton == 0:
            self.screen.blit(button_surface, (0, 24))
        elif self.chosenButton == 1:
            self.screen.blit(button_surface, (110, 24))
        elif self.chosenButton == 2:
            self.screen.blit(button_surface, (226, 24))
        else:
            self.screen.blit(button_surface, (314, 24))

    def update(self)    :

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        height = pg.display.get_surface().get_height()

        button_height = 24 * height / 1080
        button = [
            pg.Rect(0, 0, 110, button_height),
            pg.Rect(110, 0, 116, button_height),
            pg.Rect(226, 0, 88, button_height),
            pg.Rect(314, 0, 115, button_height),
        ]

        if mouse_action[2]:
            self.isChosen = False
        for i in range(len(button)):
            if button[i].collidepoint(mouse_pos[0], mouse_pos[1]):
                if (mouse_action[0]):
                    self.chosenButton = i
                    self.isChosen = True
                    break

        if self.isChosen: self.draw()






