# import pygame

from pygame.locals import *
# from authentication_setup import *
from ui_utils import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 200

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')

novice_correct = 'txt/novice_correct.txt'
novice_incorrect = 'txt/novice_incorrect.txt'
intermediate_correct = 'txt/intermediate_correct.txt'
intermediate_incorrect = 'txt/intermediate_incorrect.txt'
expert_correct = 'txt/expert_correct.txt'
expert_incorrect = 'txt/expert_incorrect.txt'


def get_answer_file(level, score):
    if level == 1:
        if score > 0:
            summary = novice_correct
        else:
            summary = novice_incorrect
    elif level == 2:
        if score > 0:
            summary = intermediate_correct
        else:
            summary = intermediate_incorrect
    else:
        if score > 0:
            summary = expert_correct
        else:
            summary = expert_incorrect
    return summary


def get_answer_text(file, name, password):
    summaryText = ''
    introFile = open(file, "r")
    for line in introFile:
        text = parse_agent_content(line, name, "0", password)
        summaryText += text + "\n"
    introFile.close()
    return summaryText


def show_summary(level, name, score, password):
    summary_file = get_answer_file(level, score)
    summary_text = get_answer_text(summary_file, name, password)
    print(summary_text)
    print_summary_text(100, 150, summary_text)


def print_summary_text(xPos, yPos, text):
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


def main_results(levelSelect, agentName, agentAge, agentSecret, agentHacked, agentScore, agentPassword):
    pygame.display.set_caption('Encryption Challenge - Results')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    backButton = pygame.image.load('gfx/back_button.png')
    backHoverButton = pygame.image.load('gfx/back_button_hover.png')
    backClickButton = pygame.image.load('gfx/back_button_click.png')
    backButtonRect = backButton.get_rect()
    backButtonRect.center = (xCenter - 700, yCenter + 550)

    nextButton = pygame.image.load('gfx/next_button.png')
    nextHoverButton = pygame.image.load('gfx/next_button_hover.png')
    nextClickButton = pygame.image.load('gfx/next_button_click.png')
    nextButtonRect = nextButton.get_rect()
    nextButtonRect.center = (xCenter + 700, yCenter + 550)

    gameSurface.fill(DARK_GREY)
    clock = pygame.time.Clock()

    show_summary(levelSelect, agentName, agentScore, agentPassword)

    nextButt = nextButton
    backButt = backButton
    doneResults = False

    index = 0

    while not doneResults:
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEMOTION:
                if nextButtonRect.collidepoint(event.pos):
                    nextButt = nextHoverButton
                elif backButtonRect.collidepoint(event.pos):
                    backButt = backHoverButton
                else:
                    nextButt = nextButton
                    backButt = backButton
            elif event.type == MOUSEBUTTONDOWN:
                if nextButtonRect.collidepoint(event.pos):
                    nextButt = nextClickButton
                    mouseClick.play()
                elif backButtonRect.collidepoint(event.pos):
                    backButt = backClickButton
                    mouseClick.play()
                else:
                    nextButt = nextButton
                    backButt = backButton
            elif event.type == MOUSEBUTTONUP:
                if nextButtonRect.collidepoint(event.pos):
                    nextButt = nextHoverButton
                    doneResults = True
                    if agentScore == 0:
                        index = ENCRYPTION
                elif backButtonRect.collidepoint(event.pos):
                    return 0
                else:
                    nextButt = nextButton
            elif event.type == QUIT:
                doneResults = True

        pygame.draw.rect(gameSurface, DARK_GREY, nextButtonRect)
        gameSurface.blit(nextButt, nextButtonRect)

        # if levelSelect == 3 and not bool(get_password_score(agentScore)):
        #    pygame.draw.rect(gameSurface, DARK_GREY, backButtonRect)
        #    gameSurface.blit(backButt, backButtonRect)

        pygame.display.flip()
        clock.tick(FPS)

        write_agent_file(AGENT_FILE, agentName, agentAge, agentSecret, agentHacked, index)

    return 1


if __name__ == '__main__':
    pygame.init()
    main_results(levelSelect=0, agentName='', agentAge='', agentSecret='', agentHacked='',
                 agentScore=0, agentPassword='')
    pygame.quit()
