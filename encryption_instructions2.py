# import pygame
from pygame.locals import *
# from encryption_setup import *
from ui_utils import *


xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 100

novice_question = 'txt/novice_question.txt'
intermediate_question = 'txt/intermediate_question.txt'
expert_question = 'txt/expert_question.txt'

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


def get_intro_text(age):
    level = get_agent_level(int(age))
    if level == 1:
        file = novice_question
    elif level == 2:
        file = intermediate_question
    else:
        file = expert_question

    question = ''
    introFile = open(file, "r")
    for line in introFile:
        text = parse_agent_content(line, '', '', '')
        question += text + "\n"
    introFile.close()
    return question


def show_intro_text(age):
    question_text = get_intro_text(age)
    print(question_text)
    print_intro_text(100, 150, question_text)


def print_intro_text(xPos, yPos, text):
    lines = text.split('\n')

    backColor = DARK_GREY
    textSize = 40
    yBuffer = 16

    fontTitle = pygame.font.Font("fonts/consolas.ttf", textSize)

    for line in lines:
        line = line.rstrip('\n')
        textTitle = fontTitle.render(line, True, LIME_GREEN, backColor)
        textTitleRect = textTitle.get_rect()
        if xPos < 0:
            textTitleRect.center = (WINDOW_WIDTH/2, yPos)
        else:
            textTitleRect.topleft = (xPos, yPos)
        gameSurface.blit(textTitle, textTitleRect)
        yPos += (textSize + yBuffer)


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


def main_instructions2(agentAge):
    pygame.display.set_caption('Encryption Challenge - Instructions (part 2)')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    gameSurface.fill(DARK_GREY)
    clock = pygame.time.Clock()

    x = 100
    y = 100

    show_intro_text(agentAge)

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
    main_instructions2()
    pygame.quit()
