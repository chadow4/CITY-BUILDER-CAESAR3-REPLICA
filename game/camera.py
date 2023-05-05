import pygame as pg

"""
    CAMERA CLASS 
"""


class Camera:

    def __init__(self, width, height):

        self.width = width  # width of the map
        self.height = height  # height of the map
        self.scroll = pg.Vector2(0, 0)
        self.dx = 0  # initialize default movement coordinate x
        self.dy = 0  # initialize default movement coordinate y
        self.speed = 10  # initialize speed of movement

    """
     Update Camera Function 
    """

    def update(self):

        mouse_pos = pg.mouse.get_pos()  # get mouse Position
        keys = pg.key.get_pressed()  # get keys Pressed

        """
        x Movement Action
        """
        # with mouse
        if mouse_pos[0] > self.width * 0.97:  # right
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:  # left
            self.dx = self.speed
        else:
            self.dx = 0
        # with keyboard
        if keys[pg.K_LEFT]:  # left
            self.dx = self.speed
        if keys[pg.K_RIGHT]:  # right
            self.dx = -self.speed

        """
        y movement
        """
        # with mouse
        if mouse_pos[1] > self.height * 0.97:  # up
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.0 + 1:  # down
            self.dy = self.speed
        else:
            self.dy = 0
        # with keyboard
        if keys[pg.K_UP]:  # up
            self.dy = self.speed
        if keys[pg.K_DOWN]:  # down
            self.dy = -self.speed

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy

        if keys[pg.K_SPACE]:
            self.scroll.x = 0
            self.scroll.y = 0
