import pygame
from pygame.locals import *
# from encryption_setup import *
from ui_utils import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 100

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


# def parse_content(inText, name, age):
#    stripText = inText.rstrip('\n')
#    tempText = stripText.replace("<agent_name>", name)
#    outText = tempText.replace("<age>", age)
#    return outText


def do_intro(xPos, yPos, name, age):
    lineCount = 0
    introFile = open('txt/welcome.txt', "r")
    for line in introFile:
        # text = line.rstrip('\n')
        text = parse_agent_content(line, name, age, '')
        backColor = DARK_GREY
        textSize = 40
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


def main_welcome(doneIntro, agentName, agentAge):
    pygame.display.set_caption('Authentication Challenge - Introduction')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    gameSurface.fill(DARK_GREY)
    clock = pygame.time.Clock()

    # x = 100
    # y = 100

    do_intro(xCenter, 100, agentName, agentAge)

    nextButton = pygame.image.load('gfx/next_button.png')
    nextHoverButton = pygame.image.load('gfx/next_button_hover.png')
    nextClickButton = pygame.image.load('gfx/next_button_click.png')
    nextButtonRect = nextButton.get_rect()
    nextButtonRect.center = (xCenter+400, yCenter + 550)
    # gameSurface.blit(nextButt, nextButtonRect)

    nextButt = nextButton
    buttonDown = False
    # doneIntro = False
    while not doneIntro:

        events = pygame.event.get()
        for event in events:
            # x = 0
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
                    buttonDown = True
                    mouseClick.play()
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
        gameSurface.blit(nextButt, nextButtonRect)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_welcome(False, agentName='', agentAge='')
    pygame.quit()
