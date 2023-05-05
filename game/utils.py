import os
import pickle

import pygame as pg


def draw_text(screen, text, size, colour, pos):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


# function counting the number of saves
def countNumberSaves(dir):
    return len([item for item in os.listdir(dir) if os.path.isfile(os.path.join(dir, item))])


def listSaves():
    file_list = [name[:len(name)-5] for name in os.listdir("./saves")]
    file_list.sort()
    return file_list


# function
def saveGame(world):
    numberOfSave = countNumberSaves("./saves") + 1
    dirOfSave = "./saves/save" + str(numberOfSave) + ".cae3"
    with open(dirOfSave, "wb") as f:
        pickle.dump((world.world, world.buildings, world.workers, world.resource_manager, world.entities), f)
        print("World saved")


def loadGame(nameSave):
    if nameSave != "My Rome":
        print('./saves/'+nameSave+'.cae3')
        with open('./saves/'+nameSave+'.cae3', 'rb') as f:
            return pickle.load(f)
    else:
        return True