# author : Penggun

import pygame as pg
import random
from time import sleep

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pad_width = 1600
pad_height = 900

background_width = 1600

aircraft_width = 450
aircraft_height = 200

bat_width = 199
bat_height = 168

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

'''
def changeBullet():
    global bullet
    bullet = pg.image.load('Bullet-Bill-icon.png')
'''

def saveHigh_score(high_score):
    fo = open("score.txt", 'w')
    fo.write(high_score)
    fo.close()

def drawPass(count, score, high_score):
    global gamepad

    font = pg.font.SysFont('comicsansms', 25)
    text = font.render('Chicken Passed ' + str(count) + '                                                          Score ' + str(score) + '                                        high_score ' + high_score, True, WHITE)
    gamepad.blit(text, (0, 0))


def gameOver():
    global gamepad
    dispMessage('GAMEOVER')


def drawScore(count):
    global gamepad

    font = pg.font.SysFont('comicsansms', 25)
    text = font.render('Score ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))


def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()


def dispMessage(text):
    global gamepad

    largeText = pg.font.Font('DEAD.TTF', 155)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width / 2), (pad_height / 2))
    gamepad.blit(TextSurf, TextRect)
    pg.display.update()
    sleep(2)
    runGame()


def crash():
    global gamepad, explosion_sound
    pg.mixer.Sound.play(explosion_sound)
    dispMessage("Crashed")


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def runGame():
    global gamepad, clock, aircraft, background1, background2, shot_sound
    global bat, fires, bullet, boom, high_score

    isShotBat = False
    boom_count = 0

    score = 0

    bat_passed = 0

    bullet_xy = []

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    bat_x = pad_width
    bat_y = random.randrange(100, pad_height-100)

    fire_x = pad_width
    fire_y = random.randrange(100, pad_height-100)
    random.shuffle(fires)
    fire = fires[0]

    af = False

    crashed = False
    while not crashed:

        score += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    y_change = -15
                elif event.key == pg.K_DOWN:
                    y_change = 15

                elif event.key == pg.K_LCTRL:
                    pg.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height / 2
                    bullet_xy.append([bullet_x, bullet_y])

                elif event.key == pg.K_z:
                    af = True
                elif event.key == pg.K_x:
                    af = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    y_change = 0

        gamepad.fill(WHITE)

        # autofire
        if af == True:
            pg.mixer.Sound.play(shot_sound)
            bullet_x = x + aircraft_width
            bullet_y = y + aircraft_height / 2
            bullet_xy.append([bullet_x, bullet_y])

        background1_x -= 10
        background2_x -= 10

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        drawPass(bat_passed, score, high_score)

        # Check the number of Bat passed
        if bat_passed > 9:
            if int(high_score) < score:
                high_score = str(score)
                saveHigh_score(high_score)

            score = 0
            gameOver()

        # Aircraft Position
        y += y_change
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height

        # Bat Position
        bat_x -= 30
        if bat_x <= 0:
            bat_passed += 1
            bat_x = pad_width
            bat_y = random.randrange(0, pad_height)

        # Fireball Position
        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 10

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # Bullets Position
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                # Check if bullet strike Bat
                if bxy[0] >= bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        isShotBat = True

                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        # -------------------충돌---------------#
        if x + aircraft_width > bat_x:
            if (y > bat_y and y < bat_y + bat_height) or \
                    (y + aircraft_height > bat_y and y + aircraft_height < bat_y + bat_height):
                if int(high_score) < score:
                    high_score = str(score)
                    saveHigh_score(high_score)
                score = 0
                crash()
        # -------------------충돌---------------#

        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height
            ''''
            if x + aircraft_width > fire_x:
                if (y > fire_y and y < fire_y + fireball_height) or \
                        (y + aircraft_height > fire_y and y + aircraft_height < fire_y + fireball_height):
                    changeBullet()
            '''
        drawObject(aircraft, x, y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotBat:
            drawObject(bat, bat_x, bat_y)
        else:
            drawObject(boom, bat_x - 200, bat_y - 100)
            boom_count += 1
            if boom_count > 3:
                boom_count = 0
                bat_x = pad_width
                bat_y = random.randrange(0, pad_height - bat_height)
                isShotBat = False

        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)

        pg.display.update()
        clock.tick(60)

    pg.quit()


def initGame():
    global gamepad, clock, aircraft, background1, background2, bat, fires, bullet, boom, shot_sound, explosion_sound, high_score, bullet
    fires = []

    pg.init()
    gamepad = pg.display.set_mode((pad_width, pad_height))
    pg.display.set_caption('PyFlying')
    aircraft = pg.image.load('plane.jpg')
    background1 = pg.image.load('minimalism-plane-ot-1600x900.jpg')
    background2 = background1.copy()
    bat = pg.image.load('bird_256.png')
    fires.append((0, pg.image.load('unnamed.png')))
    fires.append((1, pg.image.load('Cat.png')))
    boom = pg.image.load('boom.png')
    shot_sound = pg.mixer.Sound('shot.wav')
    explosion_sound = pg.mixer.Sound('explosion.wav')

    for i in range(10):
        fires.append((i + 2, None))

    bullet = pg.image.load('bullet.png')

    fi = open("score.txt", 'r')
    high_score = fi.readline()
    fi.close()


    pg.mixer.music.load('bgm.wav')
    pg.mixer.music.play(-1)

    clock = pg.time.Clock()
    runGame()


if __name__ == '__main__':
    initGame()
