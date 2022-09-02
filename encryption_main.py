from sys import exit

# from encryption_setup import *
from encryption_intro import *
# from encryption_instro2 import *
from encryption_welcome import *
from encryption_instructions import *
from encryption_instructions2 import *
from encryption_level import *
from encryption_challenge import *
# from encryption_results import *
from encryption_finish import *
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
    main_instructions2(agentAge)

#    while doGame:
#        level = main_level()
#        gameResults = main_wheel(level)
#        if gameResults < 0:
#            doGame = True
#        else:
#            doGame = False
#
#    if gameResults > 0:
#        print('congratulations on solving the cipher at the ' + gameLevel[gameResults - 1] +
#              ' level!')
#    else:
#        print('incorrect solution of cipher')

    while doGame:
        if int(agentAge) > 0:
            level = get_agent_level(int(agentAge))
        else:
            level = main_level()

        gameResults = main_challenge(level, agentName, agentAge, agentSecret, agentHacked)

        while gameResults == 0:
            print('incorrect solution of challenge - try again')
            # level = get_agent_level(int(agentAge))
            gameResults = main_challenge(level, agentName, agentAge, agentSecret, agentHacked)

        if int(gameResults) > 0:
            doGame = False
        else:
            main_instructions2(agentAge)

    print('congratulations on finishing the authentication challenge!')

    main_finish()

    # test_sub()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    exit()
