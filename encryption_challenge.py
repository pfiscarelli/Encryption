import math
import random
import pygame
from pygame.locals import *
from encryption_setup import *

SPACE_REF = 32
A_REF = 65
Z_REF = 90

WHEEL_LEFT = 1
WHEEL_RIGHT = -1

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 100

clock = pygame.time.Clock()
CLEAR_TEXT = 'WE HOPE YOU ENJOY YOUR VISIT TO LINCOLN LABORATORY'
CLEAR_TEXT_NOVICE = 'WE HOPE YOU ENJOY YOUR VISIT TO LINCOLN LABORATORY'
CLEAR_TEXT_INTERMEDIATE = 'WELCOME TO LINCOLN LABORATORY'
CLEAR_TEXT_EXPERT = 'WELCOME TO LINCOLN LABORATORY'

gameLevel = 0


def getMouseAngle(position):
    x, y = position
    xPos = 1 - (xCenter - x)
    yPos = yCenter - y
    angle = math.atan2(yPos, xPos) * (360.0 / (2 * math.pi))
    if angle < 0:
        angle += 360.0
    # print('angle is: ' + str(angle))
    return angle


def getCipherText(message, seed):
    cipher = ''
    for c in message:
        ascValue = ord(c)
        if ascValue != SPACE_REF:
            ascValue += seed
            if ascValue > Z_REF:
                ascValue = A_REF + (ascValue - Z_REF) - 1
        cipher += chr(ascValue)
        # print(str(seed) + ':' + c + ':' + str(ord(c)) + ":" + str(ascValue))
    # print('cipher text: ' + cipher)
    return cipher


def getWheelPosition(angle):
    if angle >= 360.0:
        angle -= 360.0
    elif angle < 0:
        angle += 360.0
    angleOffset = int(angle / (360.0 / 26.0) + 0.5) - 1
    if angleOffset < 0:
        angleOffset = 25
    position = 25 - angleOffset
    return position


def getKeyIn(inputKey):
    # print('keyIn: ' + str(inputKey))
    if inputKey == SPACE_REF:
        return ' '
    elif inputKey == 8:
        return 'BS'
    elif (inputKey >= 97) and (inputKey <= 122):
        return chr(inputKey - 32)
    elif (inputKey >= A_REF) and (inputKey <= Z_REF):
        return chr(inputKey)
    else:
        return ''


def getCursorPosition(inputText):
    newCursorPosition = len(inputText)
    if newCursorPosition >= len(CLEAR_TEXT):
        newCursorPosition -= 1
    elif newCursorPosition < 1:
        newCursorPosition = 0
    return newCursorPosition


def checkResults(inString, inlevel):
    if inString == CLEAR_TEXT:
        return inlevel
    else:
        return 0


def main_wheel(levelSelect):
    print('gameLevel: ' + str(levelSelect))
    fontSize = 48

    # get random seed from 1-to-25 (omit A=0)
    cipherSeed = random.randrange(1, 25)
    print('cipherSeed value: ' + str(cipherSeed) + " : " + chr(A_REF) + "=" + chr(A_REF + cipherSeed))

    # clock = pygame.time.Clock()

    gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_caption('Caesar Cipher Challenge - Decryption')
    pygame.display.set_icon(lockIcon)

    # Load images
    outerWheel = pygame.image.load('gfx/cipher_wheel_outer.png').convert_alpha()
    rotatedOuter = pygame.transform.rotate(outerWheel, 0.0)
    rotatedOuterRect = rotatedOuter.get_rect()
    rotatedOuterRect.center = (xCenter, yCenter)

    innerWheel = pygame.image.load('gfx/cipher_wheel_inner.png').convert_alpha()
    innerRect = innerWheel.get_rect()
    innerRect.center = (xCenter, yCenter)
    
    backButton = pygame.image.load('gfx/back_button.png')
    backHoverButton = pygame.image.load('gfx/back_button_hover.png')
    backClickButton = pygame.image.load('gfx/back_button_click.png')
    backButtonRect = backButton.get_rect()
    backButtonRect.center = (xCenter-700, yCenter + 550)
    
    finishButton = pygame.image.load('gfx/finish_button.png')
    finishHoverButton = pygame.image.load('gfx/finish_button_hover.png')
    finishClickButton = pygame.image.load('gfx/finish_button_click.png')
    finishButtonRect = finishButton.get_rect()
    finishButtonRect.center = (xCenter+700, yCenter + 550)

    # Set fonts
    gameFont = pygame.font.Font('fonts/consolas.ttf', 16)
    codeFont = pygame.font.Font('fonts/consolasb.ttf', 80)
    cipherFont = pygame.font.Font('fonts/consolasb.ttf', fontSize)

    cipherText = getCipherText(CLEAR_TEXT, cipherSeed)
    cipherSurf = cipherFont.render(cipherText, True, LIME_GREEN, LIGHT_GREY)
    cipherRect = cipherSurf.get_rect()
    cipherRect.center = (xCenter, WINDOW_HEIGHT - 200)
    gameSurface.blit(cipherSurf, cipherRect)
    print('cipherText: ' + cipherText)

    codeText = 'A=A'
    codeSurf = codeFont.render(codeText, True, BLACK)
    codeRect = codeSurf.get_rect()
    codeRect.center = (xCenter, yCenter + 125)
    gameSurface.blit(codeSurf, codeRect)

    inputText = len(CLEAR_TEXT) * chr(32)
    inputSurf = cipherFont.render(inputText, True, LIME_GREEN)
    inputRect = inputSurf.get_rect()
    inputRect.center = (xCenter, WINDOW_HEIGHT - 140)
    pygame.draw.rect(gameSurface, BLACK, inputRect)
    gameSurface.blit(inputSurf, inputRect)

    pygame.mixer.init(48000, -16, 1, 1024)
    mouseClick = pygame.mixer.Sound('snd/click.mp3')

    cursorX = inputRect.x + 2
    cursorY = inputRect.y + fontSize - 8
    cursorSizeX = fontSize / 2
    cursorSizeY = 5
    cursorMoveX = (fontSize / 2) + 2

    cursorPosition = (cursorX, cursorY)
    cursorLocation = 0
    cursorRect = Rect(cursorPosition, (cursorSizeX, cursorSizeY))

    rotationAngle = 0.0
    angleDiff = 0.0
    wheelDirection = WHEEL_RIGHT
    mouseDownRotation = 0.0
    # wheelPosition = 0
    mouseButtonDown = False
    keyRotate = False
    doRotate = False
    doneGame = False

    cursorTime = 0
    currentTime = 0
    gameTimer = 0
    gameClock = 100
    cursorColor = BLUE

    finishButt = finishButton
    backButt = backButton

    inputString = ''

    while not doneGame:
        gameSurface.fill(DARK_GREY)
        gameSurface.blit(rotatedOuter, rotatedOuterRect)
        gameSurface.blit(innerWheel, innerRect)
        gameSurface.blit(codeSurf, codeRect)
        gameSurface.blit(cipherSurf, cipherRect)
        gameSurface.blit(finishButt, finishButtonRect)
        gameSurface.blit(backButt, backButtonRect)

        if levelSelect > 1:
            pygame.draw.rect(gameSurface, BLACK, inputRect)
            gameSurface.blit(inputSurf, inputRect)
            pygame.draw.rect(gameSurface, cursorColor, cursorRect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keyRotate = True
                    wheelDirection = WHEEL_LEFT
                elif event.key == pygame.K_RIGHT:
                    keyRotate = True
                    wheelDirection = WHEEL_RIGHT
                else:
                    if levelSelect > 1:
                        keyIn = getKeyIn(event.key)
                        if keyIn == 'BS':
                            inputString = inputString[:-1]
                        else:
                            if len(inputString) < len(CLEAR_TEXT):
                                inputString += keyIn
                                pygame.draw.rect(gameSurface, BLACK, cursorRect)
                            else:
                                tempString = inputString[:-1] + keyIn
                                inputString = tempString
                        cursorLocation = getCursorPosition(inputString)
                        cursorPosition = (cursorX + (cursorLocation * cursorMoveX), cursorY)
                        cursorRect = Rect(cursorPosition, (cursorSizeX, cursorSizeY))
                        inputSurf = cipherFont.render(inputString, True, LIME_GREEN)
            elif event.type == MOUSEMOTION:
                if event.pos[1] > 900:
                    if finishButtonRect.collidepoint(event.pos):
                        finishButt = finishHoverButton
                    elif backButtonRect.collidepoint(event.pos):
                        backButt = backHoverButton
                    else:
                        finishButt = finishButton
                        backButt = backButton
                else:
                    # print(event.pos)
                    if mouseButtonDown:
                        angleDiff = rotationAngle + getMouseAngle(event.pos) - mouseDownRotation
                        doRotate = True
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[1] > 900:
                    if finishButtonRect.collidepoint(event.pos):
                        finishButt = finishClickButton
                        mouseClick.play()
                    elif backButtonRect.collidepoint(event.pos):
                        backButt = backClickButton
                        mouseClick.play()
                    else:
                        finishButt = finishButton
                        backButt = backButton
                else:
                    mouseButtonDown = True
                    mouseDownRotation = getMouseAngle(event.pos)
            elif event.type == MOUSEBUTTONUP:
                if event.pos[1] > 900:
                    if finishButtonRect.collidepoint(event.pos):
                        # finishButt = finishHoverButton
                        return checkResults(inputString, levelSelect)
                    elif backButtonRect.collidepoint(event.pos):
                        # backButt = backHoverButton
                        return -1
                    else:
                        finishButt = finishButton
                        backButt = backButton
                else:
                    mouseButtonDown = False
                    rotationAngle += getMouseAngle(event.pos) - mouseDownRotation
            elif event.type == QUIT:
                doneGame = True

        if rotationAngle >= 360.0:
            rotationAngle -= 360.0
        elif rotationAngle < 0:
            rotationAngle += 360.0

        if keyRotate:
            rotationAngle += (360.0 / 52.0) * wheelDirection
            angleDiff = math.trunc(rotationAngle / (360.0 / 52.0) + (0.01 * wheelDirection)) * (360.0 / 52.0)
            # print('rotation Angle: ' + str(rotationAngle) + " : " + " angleDiff: " + str(angleDiff))
            doRotate = True
            keyRotate = False

        if doRotate:
            rotatedOuter = pygame.transform.rotozoom(outerWheel, angleDiff, 1.0)
            rotatedOuterRect = rotatedOuter.get_rect()
            rotatedOuterRect.center = (xCenter, yCenter)
            wheelPosition = getWheelPosition(angleDiff)
            # print('wheelPosition: ' + str(wheelPosition) + " : " + 'rotationAngle: ' + str(rotationAngle) + " : " +
            #      'angleDiff: ' + str(angleDiff) + " : " + str(xCenter) + " " + str(yCenter))
            cipherText = getCipherText(CLEAR_TEXT, abs(wheelPosition - cipherSeed))
            if levelSelect <= 1:
                cipherSurf = cipherFont.render(cipherText, True, LIME_GREEN, LIGHT_GREY)
                inputString = cipherText
            # print('wheelPosition: ' + wheelPosition)
            codeText = 'A=' + chr(A_REF + wheelPosition)
            codeSurf = codeFont.render(codeText, True, BLACK)
            doRotate = False

        cursorTime += 1
        currentTime += 1

        if currentTime >= FPS:
            gameTimer += 1
            gameClock -= 1
            currentTime = 0
            # print('gameClock: ' + str(gameClock))

        if cursorTime >= (FPS/2):
            cursorTime = 0
            if len(inputString) != len(CLEAR_TEXT):
                if cursorColor == BLUE:
                    cursorColor = BLACK
                else:
                    cursorColor = BLUE
            else:
                cursorColor = BLACK

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main_wheel(gameLevel)
    pygame.quit()
    # sys.exit()
