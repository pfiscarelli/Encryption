import random
# import pygame
from pygame.locals import *
# from encryption_setup import *
from ui_utils import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 200

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


def main_finish():
    pygame.display.set_caption('Encryption Challenge - Finish')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    floppyDriveX = xCenter
    floppyDriveY = yCenter + 310
    floppyLEDX = floppyDriveX - 94
    floppyLEDY = floppyDriveY + 70

    floppyDrive = pygame.image.load('gfx/floppy_drive_green_led.png')
    floppyDriveRect = floppyDrive.get_rect()
    floppyDriveRect.center = (floppyDriveX, floppyDriveY)

    resultsBox = pygame.image.load('gfx/writing_results_floppy.png')
    resultsBoxRect = resultsBox.get_rect()
    resultsBoxRect.center = (xCenter, yCenter)

    floppyDarkLED = pygame.image.load('gfx/floppy_dark_green_led.png')
    floppyBrightLED = pygame.image.load('gfx/floppy_bright_green_led.png')
    floppyLEDRect = floppyBrightLED.get_rect()
    floppyLEDRect.center = (floppyLEDX, floppyLEDY)
    floppyLED = floppyBrightLED

    finishButton = pygame.image.load('gfx/finish_button.png')
    finishHoverButton = pygame.image.load('gfx/finish_button_hover.png')
    finishClickButton = pygame.image.load('gfx/finish_button_click.png')
    finishButtonRect = finishButton.get_rect()
    finishButtonRect.center = (xCenter, yCenter + 550)

    gameSurface.fill(DARK_GREY)
    gameSurface.blit(resultsBox, resultsBoxRect)
    gameSurface.blit(floppyDrive, floppyDriveRect)
    gameSurface.blit(floppyLED, floppyLEDRect)

    clock = pygame.time.Clock()

    time = 0
    finishButt = finishButton
    buttonDown = False
    doneFinish = False

    while not doneFinish:
        gameSurface.blit(floppyLED, floppyLEDRect)
        pygame.draw.rect(gameSurface, DARK_GREY, finishButtonRect)
        gameSurface.blit(finishButt, finishButtonRect)

        events = pygame.event.get()
        for event in events:
            # x = 0
            if event.type == MOUSEMOTION:
                if finishButtonRect.collidepoint(event.pos):
                    if buttonDown:
                        finishButt = finishClickButton
                        # print('mouse over button down' + str(event.pos))
                    else:
                        finishButt = finishHoverButton
                        # print('mouse over button' + str(event.pos))
                else:
                    finishButt = finishButton
                    buttonDown = False
            elif event.type == MOUSEBUTTONDOWN:
                if finishButtonRect.collidepoint(event.pos):
                    finishButt = finishClickButton
                    # print('mouse click button' + str(event.pos))
                    buttonDown = True
                    mouseClick.play()
                else:
                    finishButt = finishButton
            elif event.type == MOUSEBUTTONUP:
                if finishButtonRect.collidepoint(event.pos):
                    finishButt = finishHoverButton
                    # print('mouse over button' + str(event.pos))
                    doneFinish = True
                else:
                    finishButt = finishButton
            elif event.type == QUIT:
                doneFinish = True

        if time < 240:
            time += 1
            if random.randrange(1, 5) == 1:
                floppyLED = floppyDarkLED
            else:
                floppyLED = floppyBrightLED
        else:
            floppyLED = floppyDarkLED

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_finish()
    pygame.quit()
