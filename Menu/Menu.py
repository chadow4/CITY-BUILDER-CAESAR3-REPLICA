import sys

import pygame.display

from Menu.Model.Model import *
from game.utils import *


############################
# class which stock information about player when a new game begin
class Player:
    def __init__(self, name, creatingDay, save):
        self.name = name
        self.creatingDay = creatingDay
        self.save = save

    def get_name(self):
        print(self.name)


pygame.init()
text_color = (255, 150, 255)


# Main menu function

def viewMainMenu():
    screen.blit(menuBackGround, (0, 0))
    screen.blit(newGameTitre, (ABSCISSA_BUTTON, ORDINATE_NEWGAME))
    screen.blit(loadGameTitre, (ABSCISSA_BUTTON, SCREEN_HEIGHT / 2 - 7 * titreHeight / 6 - 150 * SCREEN_HEIGHT / 1080))
    screen.blit(cityConstructionKitTitre,
                (ABSCISSA_BUTTON, SCREEN_HEIGHT / 2 + titreHeight / 6 - 150 * SCREEN_HEIGHT / 1080))
    screen.blit(exitTitre, (ABSCISSA_BUTTON, SCREEN_HEIGHT / 2 + 3 * titreHeight / 2 - 150 * SCREEN_HEIGHT / 1080))


# New game function
def viewNewGameMenu():
    placeholder = TextLabel("The new governor", text_font, (255, 255, 255))
    shadowPlaceholder = TextLabel("The new governor", text_font, (0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(inputBox, (SCREEN_WIDTH / 2 - boxNewGames_width / 2, SCREEN_HEIGHT / 2 - boxNewGame_height / 2))
    screen.blit(textMenu.surface, (SCREEN_WIDTH / 2 - 360, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))
    events = pygame.event.get()
    textMenu.update(events)
    if textMenu.value == "":
        shadowPlaceholder.drawText(coor(SCREEN_WIDTH / 2 - 358 * SCREEN_WIDTH / 1728,
                                        SCREEN_HEIGHT / 2 - FONT_SIZE / 2 + 2 * SCREEN_HEIGHT / 1080))
        placeholder.drawText(coor(SCREEN_WIDTH / 2 - 360 * SCREEN_WIDTH / 1728, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))


# Load saved function

def viewLoadGameMenu():
    screen.blit(background, (0, 0))
    screen.blit(loadGameBox, (SCREEN_WIDTH / 2 - BOX_WIDTH / 2, SCREEN_HEIGHT / 2 - BOX_HEIGHT / 2))
    shadowText = TextLabel(textField.value, text_font, (0, 0, 0))
    shadowText.drawText(
        coor(SCREEN_WIDTH / 2 - 313 * SCREEN_WIDTH / 1728, SCREEN_HEIGHT / 2 - 240 * SCREEN_HEIGHT / 1080))
    screen.blit(textField.surface,
                (SCREEN_WIDTH / 2 - 315 * SCREEN_WIDTH / 1728, SCREEN_HEIGHT / 2 - 242 * SCREEN_HEIGHT / 1080))
    x, y = abscissaBackup, ordinateBackup
    for i in range(countNumberSaves("./saves")):
        if i > 4:
            break
        textBackup_surface = textBackup.render(listSaves()[i], True, (80, 80, 80))
        screen.blit(buttonBackup, (x, y))
        screen.blit(textBackup_surface, (x+6, y+13))
        y += 28 + buttonBackup.get_height()  # display of different saves

def scrollSave(numberScroll):
    screen.blit(loadGameBox, (SCREEN_WIDTH / 2 - BOX_WIDTH / 2, SCREEN_HEIGHT / 2 - BOX_HEIGHT / 2))
    shadowText = TextLabel(textField.value, text_font, (0, 0, 0))
    shadowText.drawText(
        coor(SCREEN_WIDTH / 2 - 313 * SCREEN_WIDTH / 1728, SCREEN_HEIGHT / 2 - 240 * SCREEN_HEIGHT / 1080))
    screen.blit(textField.surface,
                (SCREEN_WIDTH / 2 - 315 * SCREEN_WIDTH / 1728, SCREEN_HEIGHT / 2 - 242 * SCREEN_HEIGHT / 1080))

    x, y = abscissaBackup, ordinateBackup
    for i in range(numberScroll*5, countNumberSaves("./saves")):
        if i > 4+numberScroll*5:
            break
        textBackup_surface = textBackup.render(listSaves()[i], True, (80, 80, 80))
        screen.blit(buttonBackup, (x, y))
        screen.blit(textBackup_surface, (x + 6, y + 13))
        y += 28 + buttonBackup.get_height()  # display of different saves
# Game information label

# Quit label

# definition of menu's loops
def menuLoop():
    inMenu = True
    save = None
    highlight = False
    while inMenu:
        for event in pygame.event.get():
            if highlight and not is_on_button(x, y):
                viewMainMenu()
                highlight = False
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # highlight of StartNewGame button
            if (ABSCISSA_BUTTON < x < ABSCISSA_BUTTON + titreWidth and (
                    ORDINATE_NEWGAME) < y <
                    ORDINATE_NEWGAME + titreHeight):
                highlight_button(newGameTitre, ABSCISSA_BUTTON, ORDINATE_NEWGAME)
                highlight = True
            # highlight of LoadGame button
            if (ABSCISSA_BUTTON <= x <= ABSCISSA_BUTTON + titreWidth and
                    ORDINATE_LOADGAME <= y <= ORDINATE_LOADGAME + titreHeight):
                highlight_button(loadGameTitre, ABSCISSA_BUTTON, ORDINATE_LOADGAME)
                highlight = True
                # highlight of Exit button
            if (ABSCISSA_BUTTON <= x <= ABSCISSA_BUTTON + titreWidth and
                    ORDINATE_EXIT <= y <= ORDINATE_EXIT + titreHeight):
                highlight_button(exitTitre, ABSCISSA_BUTTON, ORDINATE_EXIT)
                highlight = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if button "START NEW GAME" is pressed
                if (ABSCISSA_BUTTON <= x <= ABSCISSA_BUTTON + titreWidth and (
                        ORDINATE_NEWGAME) <= y <= (
                        ORDINATE_NEWGAME + titreHeight)):
                    viewNewGameMenu()
                    inMenu = newMenuloop()
                # if button "LOAD GAME" is pressed
                if (ABSCISSA_BUTTON <= x <= ABSCISSA_BUTTON + titreWidth and (
                        ORDINATE_LOADGAME) <= y <= (
                        ORDINATE_LOADGAME + titreHeight)):
                    viewLoadGameMenu()
                    inMenu = loadMenuLoop()
                    save = inMenu
                    if save is not None and save is not True:
                        return save
                # if ((SCREEN_WIDTH/2 - titreWidth/2) <= x <= (SCREEN_WIDTH/2 + titreWidth/2) and (SCREEN_HEIGHT/2 + titreHeight/6 - 150*SCREEN_HEIGHT/1080) <= y <= (SCREEN_HEIGHT/2 + 7*titreHeight/6 - 150*SCREEN_HEIGHT/1080)):
                #     in4View.InformationView(True).viewDidLoad()
                # if button "EXIT" is pressed
                if ABSCISSA_BUTTON <= x <= ABSCISSA_BUTTON + titreWidth and (
                        ORDINATE_EXIT) <= y <= (ORDINATE_EXIT + titreHeight):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def newMenuloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        viewMainMenu()
                        return True
                if event.key == pygame.K_RETURN:
                    if (textMenu.value == ""):
                        textMenu.value = "The new governor"
                    # player = Player(textField.value, datetime.now(), configuration())
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if ((SCREEN_WIDTH / 2 + 361 * SCREEN_WIDTH / 1728) <= x <= (
                        SCREEN_WIDTH / 2 + 423 * SCREEN_WIDTH / 1728) and (
                        SCREEN_HEIGHT / 2 + 68 * SCREEN_HEIGHT / 1080) <= y <= (
                        SCREEN_HEIGHT / 2 + 124 * SCREEN_HEIGHT / 1080)):
                    if textMenu.value == "":
                        textMenu.value = "The new governor"
                    # player = Player(textMenu.value, datetime.now(), configuration())
                    return False
        pygame.display.update()


def loadMenuLoop():
    mylist = listSaves()  # print list of differents saves
    print(mylist)
    ####################
    NumberOfscroll = 0
    numberSave = None
    while True:
        events = pygame.event.get()
        textField.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        viewMainMenu()
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Button proceed
                if ((SCREEN_WIDTH / 2 + 49 * SCREEN_WIDTH / 1728) <= x <= (
                        SCREEN_WIDTH / 2 + 125 * SCREEN_WIDTH / 1728) and (
                        SCREEN_HEIGHT / 2 + 257 * SCREEN_HEIGHT / 1080) <= y <= (
                        SCREEN_HEIGHT / 2 + 305 * SCREEN_HEIGHT / 1080)):
                    return loadGame(textField.value)
                # Button return
                if ((SCREEN_WIDTH / 2 + 145 * SCREEN_WIDTH / 1728) <= x <= (
                        SCREEN_WIDTH / 2 + 220 * SCREEN_WIDTH / 1728) and (
                        SCREEN_HEIGHT / 2 + 257 * SCREEN_HEIGHT / 1080) <= y <=
                        SCREEN_HEIGHT / 2 + 305 * SCREEN_HEIGHT / 1080):
                    viewMainMenu()
                    return True
                # Down arrow
                if (1280 <= x <= 1280+84) and (724 <= y <= 724+52):
                    if NumberOfscroll >= countNumberSaves("./saves")//5:
                        pass
                    else:
                        NumberOfscroll += 1
                    scrollSave(NumberOfscroll)
                # Up arrow
                if (1280 <= x <= 1280+84) and (363 <= y <= 363+52):
                    if NumberOfscroll < 1:
                        pass
                    else:
                        NumberOfscroll -= 1
                    scrollSave(NumberOfscroll)
                numberSave = selected_save(x, y)

                # Display of the name of the selected save
                if numberSave is not None:
                    # manage when the button DOWN/UP is pressed
                    numberSave += NumberOfscroll * 5
                    if (NumberOfscroll >= countNumberSaves("./saves") // 5) and (
                    numberSave > countNumberSaves("./saves") - 1):
                        numberSave = None
                    else:
                        print(listSaves()[numberSave])
                        textField.value = listSaves()[numberSave]
                        scrollSave(NumberOfscroll)



        pygame.display.update()


def highlight_button(surface, abscissa, ordinate):
    highlight = pygame.Surface((surface.get_width() + 8, surface.get_height() + 8))
    highlight.fill((200, 200, 200))
    highlight.blit(surface, (4, 4))
    screen.blit(highlight, (abscissa, ordinate))


# Return True if the mouse is on a button in Main Menu
def is_on_button(x, y):
    return ABSCISSA_BUTTON <= x <= (ABSCISSA_BUTTON + titreWidth) and ((
           ORDINATE_NEWGAME) <= y <= (
           # Button Start New game
           ORDINATE_NEWGAME + titreHeight) or (
           ORDINATE_LOADGAME <= y <= ORDINATE_LOADGAME + titreHeight) or (
           # Button Start Load game
            ORDINATE_EXIT <= y <= ORDINATE_EXIT + titreHeight)   # Button Start Exit
                                                            )

def selected_save(x, y):
    for i in range(5):
        if (abscissaBackup <= x <= abscissaBackup+buttonBackup.get_width()) and (
        ordinateBackup+i*(28 + buttonBackup.get_height()) <= y <=
        ordinateBackup+buttonBackup.get_height()+i*(28 + buttonBackup.get_height())):
            return i


