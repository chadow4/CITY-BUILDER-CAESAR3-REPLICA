from Menu.Menu import *
from game.game import Game
from game.world import World
pg.init()

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)


def startGame():
    running = True
    playing = True

    pg.mixer.init()

    clock = pg.time.Clock()
    # implement menus
    viewMainMenu()
    # implement game
    game = Game(screen, clock)

    while running:

        # start menu goes here
        save = menuLoop()
        if save is not None:
            game.resource_manager = save[3]
            game.entities = save[4]
            game.world = World(game.resource_manager, game.entities, game.hud, 60, 60, game.width, game.height)
            game.world.world = save[0]
            game.world.buildings = save[1]
            game.world.workers = save[2]
            game.world.miniMap.camera = game.camera

        while playing:
            # game loop here
            playSong()
            game.run()


def playSong():
    sound = pygame.mixer.Sound("assets/sound/Rome3.mp3")
    sound.play(-1, 0, 0)
    sound.set_volume(0.2)
