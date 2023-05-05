import sys

from .camera import Camera
from .hud import Hud
from .resource_manager import ResourceManager
from .utils import *
from .world import World
from .worker import BasicWorker

"""
Class Game
"""


class Game:

    # Constructor Game Method
    def __init__(self, screen, clock):
        self.playing = None
        self.screen = screen
        self.clock = clock
        self.resource_manager = ResourceManager()
        self.entities = []
        self.width, self.height = self.screen.get_size()
        self.hud = Hud(self.resource_manager, self.width, self.height)
        self.camera = Camera(self.width, self.height)
        self.world = World(self.resource_manager, self.entities, self.hud, 60, 60, self.width, self.height)
        self.world.miniMap.camera = self.camera
        self.is_paused = False

    # Public Run Game Method
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(120)
            self._events()
            if 1-self.is_paused: self._update()
            self._draw()

    # Private Events Game Method
    def _events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # for i in self.world.workers:
                    #     for j in i:
                    #         if j is not None:
                    #             print (j.__dict__)
                    saveGame(self.world)  # sauvegarde de la partie en cour
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_p:
                    self.is_paused = 1-self.is_paused
            self.is_paused = self.hud.buttons.isChosen or self.is_paused

    # Private Update Game Method
    def _update(self):
        self.camera.update()
        for e in self.entities: e.update()  # building and walker
        self.hud.update()
        self.world.update(self.camera)

    # Private Draw Game Method
    def _draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen, self.camera)
        self.world.draw_worker(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(
            self.screen,
            'FPS : {}'.format(round(self.clock.get_fps())),
            23,
            (255, 255, 255),
            (1800, 5)
        )

        ListOfButton = ["File", "Option", "Help", "Advisor"]
        pos = 50
        for i in range(len(ListOfButton)):
            draw_text(self.screen, ListOfButton[i], 23, (0, 0, 0), (pos, 5))
            pos += 100
        countPop = 0

        for item in self.entities:
            if isinstance(item, BasicWorker):
                countPop += 1
        draw_text(self.screen, "Pop   " + str(countPop), 23, (255, 255, 255), (1300, 5))

        pg.display.flip()
