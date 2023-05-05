from game.videoplayer import Video
import pygame, sys
import startGame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def play_vid4():
    vid4 = Video("assets/videos/vid4.mp4")
    vid4.set_size((1950, 1150))

    while True:
        vid4.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid4.close()
                startGame.startGame()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def play_vid3():
    vid3 = Video("assets/videos/vid3.mp4")
    vid3.set_size((1950, 1150))

    while True:
        vid3.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid3.close()
                play_vid4()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def play_vid2():
    vid2 = Video("assets/videos/vid2.mp4")
    vid2.set_size((1950, 1150))
    while True:
        vid2.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid2.close()
                play_vid3()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def play_vid1():
    vid1 = Video("assets/videos/vid1.mp4")
    vid1.set_size((1950, 1150))

    while True:
        vid1.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid1.close()
                play_vid2()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
