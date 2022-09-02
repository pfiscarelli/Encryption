import pygame

from pygame.locals import *
from encryption_setup import *

pygame.init()

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 200

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)
gameFont = pygame.font.SysFont('fonts/consolas.ttf', 16, True)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


def do_intro(xPos, yPos):
    lineCount = 0
    introFile = open('txt/intro1.txt', "r")
    for line in introFile:
        text = line.rstrip('\n')
        backColor = DARK_GREY
        textSize = 48
        yBuffer = 4
        if lineCount == 0:
            backColor = LIGHT_GREY
            textSize = 64
            yBuffer = 32
        fontTitle = pygame.font.Font("fonts/consolas.ttf", textSize)
        textTitle = fontTitle.render(text, True, LIME_GREEN, backColor)
        textTitleRect = textTitle.get_rect()
        textTitleRect.center = (xPos, yPos)
        gameSurface.blit(textTitle, textTitleRect)
        yPos += (textSize + yBuffer)
        lineCount += 1
    introFile.close()


def main_intro():
    pygame.display.set_caption('Encryption Challenge - Insert Floppy Disk')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    floppyDriveX = xCenter
    floppyDriveY = yCenter + 75
    # floppyLEDX = floppyDriveX - 94
    # floppyLEDY = floppyDriveY + 70

    floppyDrive = pygame.image.load('gfx/floppy_drive_green_led.png')
    floppyDriveRect = floppyDrive.get_rect()
    floppyDriveRect.center = (floppyDriveX, floppyDriveY)

    gameSurface.fill(DARK_GREY)
    # gameSurface.blit(resultsBox, resultsBoxRect)
    gameSurface.blit(floppyDrive, floppyDriveRect)
    # gameSurface.blit(floppyLED, floppyLEDRect)

    do_intro(WINDOW_WIDTH/2, 100)

    startButton = pygame.image.load('gfx/start_button.png')
    startHoverButton = pygame.image.load('gfx/start_button_hover.png')
    startClickButton = pygame.image.load('gfx/start_button_click.png')
    startButtonRect = startButton.get_rect()
    startButtonRect.center = (xCenter, yCenter + 550)

    clock = pygame.time.Clock()

    startButt = startButton
    doneIntro = False
    buttonDown = False

    while not doneIntro:
        events = pygame.event.get()
        for event in events:
            # x = 0
            if event.type == MOUSEMOTION:
                if startButtonRect.collidepoint(event.pos):
                    if buttonDown:
                        startButt = startClickButton
                        # print('mouse over button down' + str(event.pos))
                    else:
                        startButt = startHoverButton
                        # print('mouse over button' + str(event.pos))
                else:
                    startButt = startButton
                    buttonDown = False
            elif event.type == MOUSEBUTTONDOWN:
                if startButtonRect.collidepoint(event.pos):
                    startButt = startClickButton
                    # print('mouse click button' + str(event.pos))
                    buttonDown = True
                    mouseClick.play()
                else:
                    startButt = startButton
            elif event.type == MOUSEBUTTONUP:
                if startButtonRect.collidepoint(event.pos):
                    startButt = startHoverButton
                    # print('mouse over button' + str(event.pos))
                    doneIntro = True
                else:
                    startButt = startButton
            elif event.type == QUIT:
                doneIntro = True

        pygame.draw.rect(gameSurface, DARK_GREY, startButtonRect)
        gameSurface.blit(startButt, startButtonRect)

        pygame.display.flip()
    clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_intro()
    pygame.quit()
