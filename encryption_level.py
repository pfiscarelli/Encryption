import pygame
from pygame.locals import *
from encryption_setup import *

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2)

greetingText = "Select Level"

pygame.init()
gameFont = pygame.font.SysFont('consolas', 104, True)

greetingSurf = gameFont.render(greetingText, True, LIME_GREEN)
greetingRect = greetingSurf.get_rect()
greetingRect.center = (xCenter, 128)

gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)

levelNovice = pygame.image.load('gfx/level_novice_button.png')
levelNoviceHover = pygame.image.load('gfx/level_novice_button_hover.png')
levelNoviceClick = pygame.image.load('gfx/level_novice_button_click.png')
levelNoviceRect = levelNovice.get_rect()
levelNoviceRect.center = (xCenter, yCenter - 250)

levelIntermediate = pygame.image.load('gfx/level_intermediate_button.png')
levelIntermediateHover = pygame.image.load('gfx/level_intermediate_button_hover.png')
levelIntermediateClick = pygame.image.load('gfx/level_intermediate_button_click.png')
levelIntermediateRect = levelIntermediate.get_rect()
levelIntermediateRect.center = (xCenter, yCenter - 75)

levelExpert = pygame.image.load('gfx/level_expert_button.png')
levelExpertHover = pygame.image.load('gfx/level_expert_button_hover.png')
levelExpertClick = pygame.image.load('gfx/level_expert_button_click.png')
levelExpertRect = levelExpert.get_rect()
levelExpertRect.center = (xCenter, yCenter + 100)

levelBlankText = pygame.image.load('gfx/blank_level_description.png')
levelNoviceText = pygame.image.load('gfx/novice_level_description.png')
levelIntermediateText = pygame.image.load('gfx/intermediate_level_description.png')
levelExpertText = pygame.image.load('gfx/expert_level_description.png')
levelTextRect = levelBlankText.get_rect()
levelTextRect.center = (xCenter, yCenter + 350)

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')


def main_level():
    pygame.display.set_caption('Caesar Cipher Challenge - Select Level')
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_icon(lockIcon)

    buttonNovice = levelNovice
    buttonIntermediate = levelIntermediate
    buttonExpert = levelExpert
    levelText = levelBlankText

    clock = pygame.time.Clock()
    doneLevel = False

    levelSelect = 0

    while not doneLevel:

        gameSurface.fill(DARK_GREY)
        gameSurface.blit(greetingSurf, greetingRect)
        gameSurface.blit(buttonNovice, levelNoviceRect)
        gameSurface.blit(buttonIntermediate, levelIntermediateRect)
        gameSurface.blit(buttonExpert, levelExpertRect)
        gameSurface.blit(levelText, levelTextRect)

        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEMOTION:
                if levelNoviceRect.collidepoint(event.pos):
                    buttonNovice = levelNoviceHover
                    buttonIntermediate = levelIntermediate
                    buttonExpert = levelExpert
                    levelText = levelNoviceText
                elif levelIntermediateRect.collidepoint(event.pos):
                    buttonIntermediate = levelIntermediateHover
                    buttonNovice = levelNovice
                    buttonExpert = levelExpert
                    levelText = levelIntermediateText
                elif levelExpertRect.collidepoint(event.pos):
                    buttonExpert = levelExpertHover
                    buttonNovice = levelNovice
                    buttonIntermediate = levelIntermediate
                    levelText = levelExpertText
                else:
                    levelText = levelBlankText
                    buttonNovice = levelNovice
                    buttonIntermediate = levelIntermediate
                    buttonExpert = levelExpert
            elif event.type == MOUSEBUTTONDOWN:
                if levelNoviceRect.collidepoint(event.pos):
                    buttonNovice = levelNoviceClick
                    mouseClick.play()
                elif levelIntermediateRect.collidepoint(event.pos):
                    buttonIntermediate = levelIntermediateClick
                    mouseClick.play()
                elif levelExpertRect.collidepoint(event.pos):
                    buttonExpert = levelExpertClick
                    mouseClick.play()
                else:
                    buttonNovice = levelNovice
                    buttonIntermediate = levelIntermediate
                    buttonExpert = levelExpert
            elif event.type == MOUSEBUTTONUP:
                if levelNoviceRect.collidepoint(event.pos):
                    buttonNovice = levelNoviceHover
                    doneLevel = True
                    levelSelect = 1
                elif levelIntermediateRect.collidepoint(event.pos):
                    buttonIntermediate = levelIntermediateHover
                    doneLevel = True
                    levelSelect = 2
                elif levelExpertRect.collidepoint(event.pos):
                    buttonExpert = levelExpertHover
                    doneLevel = True
                    levelSelect = 3
                else:
                    buttonNovice = levelNovice
                    buttonIntermediate = levelIntermediate
                    buttonExpert = levelExpert
            elif event.type == QUIT:
                doneLevel = True

        pygame.display.flip()
        clock.tick(FPS)

    return levelSelect


if __name__ == '__main__':
    pygame.init()
    selectedLevel = main_level()
    print('selected level: ' + str(selectedLevel))
    pygame.quit()
