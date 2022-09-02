import random
import pygame
from pygame.locals import *
from encryption_setup import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 200

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)


def main_results():
    pygame.display.set_caption('Caesar Cipher Challenge - Instructions')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    floppyDriveX = xCenter
    floppyDriveY = yCenter + 310
    floppyLEDX = floppyDriveX - 94
    floppyLEDY = floppyDriveY + 70

    floppyDrive = pygame.image.load('gfx/floppy_drive.png')
    floppyDriveRect = floppyDrive.get_rect()
    floppyDriveRect.center = (floppyDriveX, floppyDriveY)

    resultsBox = pygame.image.load('gfx/writing_results_floppy.png')
    resultsBoxRect = resultsBox.get_rect()
    resultsBoxRect.center = (xCenter, yCenter)

    floppyDarkLED = pygame.image.load('gfx/floppy_dark_led.png')
    floppyBrightLED = pygame.image.load('gfx/floppy_bright_led.png')
    floppyLEDRect = floppyBrightLED.get_rect()
    floppyLEDRect.center = (floppyLEDX, floppyLEDY)
    floppyLED = floppyBrightLED

    gameSurface.fill(DARK_GREY)
    gameSurface.blit(resultsBox, resultsBoxRect)
    gameSurface.blit(floppyDrive, floppyDriveRect)
    gameSurface.blit(floppyLED, floppyLEDRect)

    clock = pygame.time.Clock()

    LEDTime = 0
    doneResults = False

    while not doneResults:
        gameSurface.blit(floppyLED, floppyLEDRect)

        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEMOTION:
                print(event.pos)
            elif event.type == QUIT:
                doneResults = True

        #pygame.draw.rect(gameSurface, DARK_GREY, nextButtonRect)
        #pygame.draw.rect(gameSurface, DARK_GREY, backButtonRect)
        #gameSurface.blit(nextButt, nextButtonRect)
        #gameSurface.blit(backButt, backButtonRect)

        '''
        LEDTime += 1

        if LEDTime >= (FPS/2):
            LEDTime = 0
            if floppyLED == floppyBrightLED:
                floppyLED = floppyDarkLED
            else:
                floppyLED = floppyBrightLED
        '''

        if random.randrange(1, 3) == 1:
            floppyLED = floppyDarkLED
        else:
            floppyLED = floppyBrightLED

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_results()
    pygame.quit()
