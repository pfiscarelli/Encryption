import pygame
from pygame.locals import *
from encryption_setup import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 100

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


def do_intro1(xPos, yPos):
    # this is a test comment
    instruct1File = open('txt/instruct1.txt', "r")
    for line in instruct1File:
        text = line.rstrip('\n')
        textSize = 32
        yBuffer = 0
        if yPos == 100:
            textSize = 64
            yBuffer = 32
        fontTitle = pygame.font.Font("fonts/consolas.ttf", textSize)
        textTitle = fontTitle.render(text, True, LIME_GREEN)
        textTitleRect = textTitle.get_rect()
        textTitleRect.center = (xCenter, yPos)
        gameSurface.blit(textTitle, textTitleRect)
        yPos += (32 + yBuffer)
    instruct1File.close()


def do_intro2(xPos, yPos):
    instruct2File = open('txt/instruct2.txt', "r")
    for line in instruct2File:
        text = line.rstrip('\n')
        textSize = 32
        yBuffer = 0
        fontTitle = pygame.font.Font("fonts/consolas.ttf", textSize)
        textTitle = fontTitle.render(text, True, LIME_GREEN)
        textTitleRect = textTitle.get_rect()
        textTitleRect.center = (xCenter, yPos + 60)
        gameSurface.blit(textTitle, textTitleRect)
        yPos += (32 + yBuffer)
    instruct2File.close()


def main_instructions():
    pygame.display.set_caption('Encryption Challenge - Instructions')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    gameSurface.fill(DARK_GREY)
    clock = pygame.time.Clock()

    x = 100
    y = 100

    do_intro1(x, y)
    do_intro2(x, y+500)

    cipherAlpha = pygame.image.load('gfx/cipher_shift3.png')
    cipherAlphaRect = cipherAlpha.get_rect()
    cipherAlphaRect.center = (xCenter, yCenter + 110)
    gameSurface.blit(cipherAlpha, cipherAlphaRect)

    cipherApple = pygame.image.load('gfx/cipher_apple.png')
    cipherAppleRect = cipherApple.get_rect()
    cipherAppleRect.center = (xCenter, yCenter + 320)
    gameSurface.blit(cipherApple, cipherAppleRect)

    nextButton = pygame.image.load('gfx/next_button.png')
    nextHoverButton = pygame.image.load('gfx/next_button_hover.png')
    nextClickButton = pygame.image.load('gfx/next_button_click.png')
    nextButtonRect = nextButton.get_rect()
    nextButtonRect.center = (xCenter+400, yCenter + 550)
    # gameSurface.blit(nextButt, nextButtonRect)

    # backButton = pygame.image.load('gfx/back_button.png')
    # backHoverButton = pygame.image.load('gfx/back_button_hover.png')
    # backClickButton = pygame.image.load('gfx/back_button_click.png')
    # backButtonRect = backButton.get_rect()
    # backButtonRect.center = (xCenter-400, yCenter + 550)

    nextButt = nextButton
    # backButt = backButton
    buttonDown = False
    doneIntro = False

    while not doneIntro:
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEMOTION:
                if nextButtonRect.collidepoint(event.pos):
                    if buttonDown:
                        nextButt = nextClickButton
                        # print('mouse over button down' + str(event.pos))
                    else:
                        nextButt = nextHoverButton
                        # print('mouse over button' + str(event.pos))
                else:
                    nextButt = nextButton
                    buttonDown = False
            elif event.type == MOUSEBUTTONDOWN:
                if nextButtonRect.collidepoint(event.pos):
                    nextButt = nextClickButton
                    # print('mouse click button' + str(event.pos))
                    mouseClick.play()
                    buttonDown = True
                else:
                    nextButt = nextButton
            elif event.type == MOUSEBUTTONUP:
                if nextButtonRect.collidepoint(event.pos):
                    nextButt = nextHoverButton
                    # print('mouse over button' + str(event.pos))
                    doneIntro = True
                else:
                    nextButt = nextButton
            elif event.type == QUIT:
                doneIntro = True

        pygame.draw.rect(gameSurface, DARK_GREY, nextButtonRect)
        # pygame.draw.rect(gameSurface, DARK_GREY, backButtonRect)
        gameSurface.blit(nextButt, nextButtonRect)
        # gameSurface.blit(backButt, backButtonRect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_instructions()
    pygame.quit()
