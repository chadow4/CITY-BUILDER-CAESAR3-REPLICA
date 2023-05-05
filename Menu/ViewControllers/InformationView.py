# from Model.Model import *
# from Model.Constant import *
# import pygame
# import sys
#
# from ViewControllers.MainMenuView import *
#
# pygame.init()
#
# NORMAL_FONT_SIZE = 30
#
#
#
#
#
# class InformationView:
#     def __init__(self, isInInformationView):
#         self.isInInformationView = isInInformationView
#
#     img = pygame.image.load("/Users/duy/Desktop/Game_main_menu/assets/back_arrow.png")
#     img = pygame.transform.scale(img, (100, 100))
#     normalFont = pygame.font.SysFont("arialblack", NORMAL_FONT_SIZE)
#
#     text_font = pygame.font.SysFont("arialblack", FONT_SIZE)
#
#     def viewDidLoad(self):
#         while self.isInInformationView:
#             screen.fill((50, 50, 50))
#             draw("Hello", self.text_font, TEXT_COLOR, coor(300, 300))
#             draw("This is a game from my team", self.normalFont, TEXT_COLOR, coor(300, 400))
#             screen.blit(self.img, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.isInInformationView = False
#                     sys.exit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     x, y = pygame.mouse.get_pos()
#                     if ((SCREEN_WIDTH - 100)<x<SCREEN_WIDTH and (SCREEN_HEIGHT - 100)<y<SCREEN_HEIGHT):
#                         self.isInInformationView = False
#             pygame.display.update()
#
