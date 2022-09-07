import math
import random
# import pygame
# from pygame.locals import *
# from encryption_setup import *
from encryption_results import *

SPACE_REF = 32
BACKSPACE_REF = 8
RETURN_REF = 13

A_REF = 65
Z_REF = 90

WHEEL_LEFT = 1
WHEEL_RIGHT = -1

pygame.mixer.init(48000, -16, 1, 1024)
mouseClick = pygame.mixer.Sound('snd/click.mp3')

xCenter = int(WINDOW_WIDTH / 2)
yCenter = int(WINDOW_HEIGHT / 2) - 100

clock = pygame.time.Clock()

# CLEAR_TEXT = 'WE HOPE YOU ENJOY YOUR VISIT TO LINCOLN LABORATORY'
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


def get_clear_text(level):
    if level == 1:
        text = CLEAR_TEXT_NOVICE
    elif level == 2:
        text = CLEAR_TEXT_INTERMEDIATE
    else:
        text = CLEAR_TEXT_EXPERT
    return text


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
    elif inputKey == BACKSPACE_REF:
        return 'BS'
    elif inputKey == RETURN_REF:
        return 'CR'
    elif (inputKey >= 97) and (inputKey <= 122):
        return chr(inputKey - 32)
    elif (inputKey >= A_REF) and (inputKey <= Z_REF):
        return chr(inputKey)
    else:
        return ''


def getCursorPosition(inputText, clearText):
    newCursorPosition = len(inputText)
    if newCursorPosition >= len(clearText):
        newCursorPosition -= 1
    elif newCursorPosition < 1:
        newCursorPosition = 0
    return newCursorPosition


def show_secret_key(key, level):
    return 0


def checkResults(inString, clearText):
    print('clear text is: ' + str(clearText))
    print('submitted text is: ' + str(inString))
    if inString == clearText:
        return 1
    else:
        return 0


def main_challenge(levelSelect, agentName, agentAge, agentSecret, agentHacked):
    print('gameLevel: ' + str(levelSelect))
    fontSize = 48

    clearText = get_clear_text(levelSelect)

    # get random seed from 1-to-25 (omit A=0)
    cipherSeed = random.randrange(1, 25)
    print('cipherSeed value: ' + str(cipherSeed) + " : " + chr(A_REF) + "=" + chr(A_REF + cipherSeed))

    # clock = pygame.time.Clock()

    gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF)
    lockIcon = pygame.image.load('gfx/lock.ico')
    pygame.display.set_caption('Encryption Challenge - Decryption')
    pygame.display.set_icon(lockIcon)

    # Load images
    outerWheel = pygame.image.load('gfx/cipher_wheel_outer.png').convert_alpha()
    rotatedOuter = pygame.transform.rotate(outerWheel, 0.0)
    rotatedOuterRect = rotatedOuter.get_rect()
    rotatedOuterRect.center = (xCenter, yCenter - 50)

    innerWheel = pygame.image.load('gfx/cipher_wheel_inner_new.png').convert_alpha()
    innerRect = innerWheel.get_rect()
    innerRect.center = (xCenter, yCenter - 50)
    
    backButton = pygame.image.load('gfx/back_button.png')
    backHoverButton = pygame.image.load('gfx/back_button_hover.png')
    backClickButton = pygame.image.load('gfx/back_button_click.png')
    backButtonRect = backButton.get_rect()
    backButtonRect.center = (xCenter-700, yCenter + 550)
    
    submitButton = pygame.image.load('gfx/submit_button.png')
    submitHoverButton = pygame.image.load('gfx/submit_button_hover.png')
    submitClickButton = pygame.image.load('gfx/submit_button_click.png')
    submitButtonRect = submitButton.get_rect()
    submitButtonRect.center = (xCenter+700, yCenter + 550)

    # Set fonts
    keyFont = pygame.font.Font('fonts/consolasb.ttf', 48)
    codeFont = pygame.font.Font('fonts/consolasb.ttf', 64)
    cipherFont = pygame.font.Font('fonts/consolasb.ttf', fontSize)

    cipherText = getCipherText(clearText, cipherSeed)
    cipherSurf = cipherFont.render(cipherText, True, LIME_GREEN, LIGHT_GREY)
    cipherRect = cipherSurf.get_rect()
    cipherRect.center = (xCenter, WINDOW_HEIGHT - 250)
    gameSurface.blit(cipherSurf, cipherRect)
    print('cipherText: ' + cipherText)

    keyText = 'A=' + chr(A_REF + cipherSeed)
    keySurf = keyFont.render(keyText, True, RED)
    keyRect = keySurf.get_rect()
    keyRect.center = (xCenter, yCenter + 100)
    gameSurface.blit(keySurf, keyRect)

    secretKeyText = "Secret Key"
    secretKeySurf = keyFont.render(secretKeyText, True, RED)
    secretKeyRect = secretKeySurf.get_rect()
    secretKeyRect.center = (xCenter, yCenter + 50)
    gameSurface.blit(secretKeySurf, secretKeyRect)

    codeText = 'A=A'
    codeSurf = codeFont.render(codeText, True, BLACK)
    codeRect = codeSurf.get_rect()
    codeRect.center = (xCenter, yCenter - 150)
    gameSurface.blit(codeSurf, codeRect)

    inputText = len(clearText) * chr(32)
    inputSurf = cipherFont.render(inputText, True, LIME_GREEN)
    inputRect = inputSurf.get_rect()
    inputRect.center = (xCenter, WINDOW_HEIGHT - 190)
    pygame.draw.rect(gameSurface, BLACK, inputRect)
    gameSurface.blit(inputSurf, inputRect)

    cursorX = inputRect.x + 2
    cursorY = inputRect.y + fontSize - 8
    cursorSizeX = fontSize / 2
    cursorSizeY = 5
    cursorMoveX = (fontSize / 2) + 2

    cursorPosition = (cursorX, cursorY)
    # cursorLocation = 0
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

    submitButt = submitButton
    backButt = backButton

    showHint = False

    inputString = ''

    while not doneGame:
        gameSurface.fill(DARK_GREY)
        gameSurface.blit(rotatedOuter, rotatedOuterRect)
        gameSurface.blit(innerWheel, innerRect)
        gameSurface.blit(codeSurf, codeRect)
        gameSurface.blit(cipherSurf, cipherRect)
        gameSurface.blit(submitButt, submitButtonRect)
        gameSurface.blit(backButt, backButtonRect)

        if levelSelect == 2 or showHint:
            gameSurface.blit(keySurf, keyRect)
            gameSurface.blit(secretKeySurf, secretKeyRect)

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
                elif event.key == pygame.K_h and pygame.KMOD_CTRL:
                    showHint = True
                    print("CTRL+H is pressed")
                else:
                    if levelSelect > 1:
                        keyIn = getKeyIn(event.key)
                        if keyIn == 'BS':
                            inputString = inputString[:-1]
                        elif keyIn != 'CR':
                            if len(inputString) < len(clearText):
                                inputString += keyIn
                                pygame.draw.rect(gameSurface, BLACK, cursorRect)
                            else:
                                tempString = inputString[:-1] + keyIn
                                inputString = tempString
                        cursorLocation = getCursorPosition(inputString, clearText)
                        cursorPosition = (cursorX + (cursorLocation * cursorMoveX), cursorY)
                        cursorRect = Rect(cursorPosition, (cursorSizeX, cursorSizeY))
                        inputSurf = cipherFont.render(inputString, True, LIME_GREEN)
            elif event.type == MOUSEMOTION:
                if event.pos[1] > 900:
                    if submitButtonRect.collidepoint(event.pos):
                        submitButt = submitHoverButton
                    elif backButtonRect.collidepoint(event.pos):
                        backButt = backHoverButton
                    else:
                        submitButt = submitButton
                        backButt = backButton
                else:
                    # print(event.pos)
                    if mouseButtonDown:
                        angleDiff = rotationAngle + getMouseAngle(event.pos) - mouseDownRotation
                        doRotate = True
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[1] > 900:
                    if submitButtonRect.collidepoint(event.pos):
                        submitButt = submitClickButton
                        mouseClick.play()
                    elif backButtonRect.collidepoint(event.pos):
                        backButt = backClickButton
                        mouseClick.play()
                    else:
                        submitButt = submitButton
                        backButt = backButton
                else:
                    mouseButtonDown = True
                    mouseDownRotation = getMouseAngle(event.pos)
            elif event.type == MOUSEBUTTONUP:
                if event.pos[1] > 900:
                    if submitButtonRect.collidepoint(event.pos):
                        # submitButt = submitHoverButton
                        # return checkResults(inputString, levelSelect)
                        score = checkResults(inputString, clearText)
                        retryAttempt = main_results(levelSelect, agentName, agentAge, agentSecret,
                                                    agentHacked, score, inputString)
                        return retryAttempt
                    elif backButtonRect.collidepoint(event.pos):
                        # backButt = backHoverButton
                        return -1
                    else:
                        submitButt = submitButton
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
            rotatedOuterRect.center = (xCenter, yCenter - 50)
            wheelPosition = getWheelPosition(angleDiff)
            # print('wheelPosition: ' + str(wheelPosition) + " : " + 'rotationAngle: ' + str(rotationAngle) + " : " +
            #      'angleDiff: ' + str(angleDiff) + " : " + str(xCenter) + " " + str(yCenter))
            cipherText = getCipherText(clearText, abs(wheelPosition - cipherSeed))
            if levelSelect <= 1:
                cipherSurf = cipherFont.render(cipherText, True, LIME_GREEN, LIGHT_GREY)
                inputString = cipherText
            # print('wheelPosition: ' + wheelPosition)
            codeText = 'A=' + chr(A_REF + wheelPosition)
            codeSurf = codeFont.render(codeText, True, BLACK)
            if gameLevel == 2:
                keySurf = keyFont.render(keyText, True, RED)
                secretKeySurf = keyFont.render(secretKeyText, True, RED)
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
            if len(inputString) != len(clearText):
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
    main_challenge(gameLevel, agentName='', agentAge='', agentSecret='', agentHacked='')
    pygame.quit()
    # sys.exit()
