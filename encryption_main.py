from sys import exit

# from encryption_setup import *
from encryption_intro import *
from encryption_welcome import *
from encryption_instructions import *
from encryption_level import *
from encryption_challenge import *
from encryption_results import *
from ui_utils import *


gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)
gameFont = pygame.font.Font('fonts/consolas.ttf', 16)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')

gameLevel = ('novice', 'intermediate', 'expert')


def main():
    pygame.display.set_caption('Caesar Cipher Challenge')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    doGame = True
    gameResults = 0

    main_intro()

    agentName, agentAge, agentSecret, agentHacked = get_agent_file(AGENT_FILE)

    main_welcome(False, agentName, agentAge)
    main_instructions()

    while doGame:
        level = main_level()
        gameResults = main_wheel(level)
        if gameResults < 0:
            doGame = True
        else:
            doGame = False

    if gameResults > 0:
        print('congratulations on solving the cipher at the ' + gameLevel[gameResults - 1] +
              ' level!')
    else:
        print('incorrect solution of cipher')

    main_results()

    # test_sub()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    exit()
