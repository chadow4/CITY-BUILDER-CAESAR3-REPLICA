import pygame.display
from pygame_textinput import pygame_textinput

# from Menu.Model.Model import TextLabel

pygame.init()

# stockage de l'écran et de ses dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# paramètre de la police du menu
FONT_SIZE = int(40 * SCREEN_HEIGHT / 1080)
TEXT_COLOR = (255, 255, 255)
text_font = pygame.font.SysFont("Times", FONT_SIZE)

manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 20)
textField = pygame_textinput.TextInputVisualizer(manager=manager, font_object=text_font, font_color=(255, 255, 255))
textField.cursor_width = 3
textField.cursor_color = (255, 255, 255)

# chargement de l'images des boutons du menu
titreWidth = 256 * 3 * SCREEN_WIDTH / 1728
titreHeight = 25 * 3 * SCREEN_HEIGHT / 1080

ABSCISSA_BUTTON = SCREEN_WIDTH / 2 - titreWidth / 2
ORDINATE_NEWGAME = SCREEN_HEIGHT / 2 - 5 * titreHeight / 2 - 150 * SCREEN_HEIGHT / 1080
ORDINATE_LOADGAME = SCREEN_HEIGHT / 2 - 7 * titreHeight / 6 - 150 * SCREEN_HEIGHT / 1080
ORDINATE_EXIT = SCREEN_HEIGHT / 2 + 3 * titreHeight / 2 - 150 * SCREEN_HEIGHT / 1080

menuBackGround = pygame.image.load("assets/graphics/Menu/background.png")
menuBackGround = pygame.transform.scale(menuBackGround, (SCREEN_WIDTH, SCREEN_HEIGHT))

newGameTitre = pygame.image.load("assets/graphics/Menu/startNewGameTitre.png")
newGameTitre = pygame.transform.scale(newGameTitre, (titreWidth, titreHeight))

loadGameTitre = pygame.image.load("assets/graphics/Menu/loadGameTitre.png")
loadGameTitre = pygame.transform.scale(loadGameTitre, (titreWidth, titreHeight))

cityConstructionKitTitre = pygame.image.load("assets/graphics/Menu/cityConstructionKitTitre.png")
cityConstructionKitTitre = pygame.transform.scale(cityConstructionKitTitre, (titreWidth, titreHeight))

exitTitre = pygame.image.load("assets/graphics/Menu/exitTitre.png")
exitTitre = pygame.transform.scale(exitTitre, (titreWidth, titreHeight))

# Loading pictures of newMenu

manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 20)
textMenu = pygame_textinput.TextInputVisualizer(manager=manager, font_object=text_font, font_color=(255, 255, 255))
textMenu.cursor_width = 3
textMenu.cursor_color = (255, 255, 255)

# Draw background

background = pygame.image.load("assets/graphics/Menu/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

boxNewGames_width = 384 * 2.5 * SCREEN_WIDTH / 1728
boxNewGame_height = 128 * 2.5 * SCREEN_HEIGHT / 1080
inputBox = pygame.image.load("assets/graphics/Menu/inputNewNameBox.png")
inputBox = pygame.transform.scale(inputBox, (boxNewGames_width, boxNewGame_height))

# Loading pictures of loadMenu

BOX_WIDTH = 384 * 2 * SCREEN_WIDTH / 1728
BOX_HEIGHT = 336 * 2 * SCREEN_HEIGHT / 1080
loadGameBox = pygame.image.load("assets/graphics/Menu/loadGameBox.png")
loadGameBox = pygame.transform.scale(loadGameBox, (BOX_WIDTH, BOX_HEIGHT))
buttonBackup = pygame.Surface((650, 50))
buttonBackup.fill((200, 200, 200))
abscissaBackup = SCREEN_WIDTH / 2 - buttonBackup.get_width() / 2 - 38
ordinateBackup = SCREEN_HEIGHT / 2 - BOX_HEIGHT / 2 + 180

manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 20)
textField = pygame_textinput.TextInputVisualizer(manager=manager, font_object=text_font, font_color=(255, 255, 255))
textField.cursor_width = 3
textField.cursor_color = (255, 255, 255)
textField.value = "My Rome"
manager.cursor_pos = len(textField.value)
# Text for display the save's name
textBackup = pygame.font.Font(None, 36)
#textBackup = textBackup.render("Hello, World!", True, (80, 80, 80))
