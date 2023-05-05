import pygame

from Menu.Model.Model import *
from .Constant import *

class coor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TextLabel:
    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color
    def drawText(self, coor):
        return draw(self.text, self.font, self.color, coor)





class ViewObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Image(ViewObject):
    def __init__(self, path, x, y, weight, height):
        super(Image, self).__init__(x, y)
        self.weight = weight
        self.height = height
        self.img = pygame.transform.scale(pygame.image.load(path), (weight, height))

class Label(ViewObject):
    def __init__(self, textLabel, x, y):
        super(Label, self).__init__(x, y)
        self.textLabel = textLabel





def draw(text, font, color, coor):
    img = font.render(text, True, color)
    screen.blit(img, (coor.x, coor.y))
    return (pygame.Surface.get_width(img), pygame.Surface.get_height(img))

class Player:
    def __init__(self, name, creatingDay, configuration):
        self.name = name
        self.creatingDay = creatingDay
        self.configurationFile = configuration

    def get_name(self):
        print(self.name)

def save(player):
    pass

class configuration:
    def __init__(self):
        pass

class Player_:
    def __init__(self, player=None):
        self.player = player
        self.next = None

class PlayerList:
    def __init__(self):
        self.head = None

    def append(self, player):
        player.next = self.head
        self.head = player

playerList = PlayerList()