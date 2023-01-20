import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from digitalio import DigitalInOut,Direction, Pull
from adafruit_bitmap_font import bitmap_font

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=32,height = 16, bit_depth=4,
    rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

display.auto_refresh = False
btnup = DigitalInOut(board.GP20)
btnup.direction = Direction.INPUT
btndown = DigitalInOut(board.GP18)
btndown.direction = Direction.INPUT
btnleft = DigitalInOut(board.GP19)
btnleft.direction = Direction.INPUT
btnright = DigitalInOut(board.GP21)
btnright.direction = Direction.INPUT

#btn.pull = Pull.UP

gamemap = []
playerpos = []
boxpos = []
targetpos = []

levels = 3

def iswin():
    counter = 0
    for a in range(len(targetpos)):
        for b in range(len(boxpos)):
            if targetpos[a][0] == boxpos[b][0] and targetpos[a][1] == boxpos[b][1]:
                counter += 1
    if counter == len(targetpos):
        return True
    return False

def wasittarget(x,y):
    for a in range(len(targetpos)):
        if targetpos[a][0] == x and targetpos[a][1] == y:
            return True
    return False
    
def changeboxpos(xn,yn,xnn,ynn):
    for a in range(len(boxpos)):
        if boxpos[a][0] == xn and boxpos[a][1] == yn:
            boxpos[a][0] = xnn
            boxpos[a][1] = ynn
            return

def openfile(level):
    file = open("levels/level{}.txt".format(level),"r")

    lines = file.readlines()
    for line in lines:
        gamemap.append(list(line)[:-1])

def generatemap():
    for x in range(len(gamemap)):
        for y in range(len(gamemap[0])):
            if gamemap[x][y] == 'P':
                playerpos.append(x)
                playerpos.append(y)
            if gamemap[x][y] == 'B':
                boxpos.append([x, y])
            if gamemap[x][y] == 'C':
                targetpos.append([x, y])
def printmap():
    for x in range(8):
        for y in range(10):
            print(gamemap[x][y],end='')
        print("")

def move(x,y,xn,yn):
    xnn = x + (x - xn) * (-2)
    ynn = y + (y - yn) * (-2)
    if gamemap[xn][yn] == 'B' and (gamemap[xnn][ynn] == 'C' or gamemap[xnn][ynn] == 'O'):
        playerpos[0] = xn
        playerpos[1] = yn
        gamemap[xn][yn] = 'P'
        gamemap[xnn][ynn] = 'B'
        changeboxpos(xn,yn,xnn,ynn)
        if wasittarget(x,y):
            gamemap[x][y] = 'C'
        else:
            gamemap[x][y] = 'O'
        return True

    elif gamemap[xn][yn] == 'O' or gamemap[xn][yn] == 'C':
        if wasittarget(x,y):
            gamemap[x][y] = 'C'
        else:
            gamemap[x][y] = 'O'
        gamemap[xn][yn] = 'P'
        playerpos[0] = xn
        playerpos[1] = yn
        return True
    return False

def play(step):
    steps = 0 + step
    while True:

        if btnup.value:
            if move(playerpos[0], playerpos[1], playerpos[0] - 1, playerpos[1]):
                draw_map(steps)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                print(steps)
                if iswin():
                    return steps
                steps = steps + 1
                time.sleep(0.5)
        elif btndown.value:
            if move(playerpos[0], playerpos[1], playerpos[0] + 1, playerpos[1]):
                draw_map(steps)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                print(steps)
                if iswin():
                    return steps
                steps = steps + 1
                time.sleep(0.5)
        elif btnleft.value:
            if move(playerpos[0], playerpos[1], playerpos[0], playerpos[1] - 1):
                draw_map(steps)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                print(steps)
                if iswin():
                    return steps
                steps = steps + 1
                time.sleep(0.5)
        elif btnright.value:
            if move(playerpos[0], playerpos[1], playerpos[0], playerpos[1] + 1):
                draw_map(steps)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
                print(steps)
                if iswin():
                    return steps
                steps = steps + 1
                time.sleep(0.5)

step = 0




    


target_fps = 10

def draw_map(steps):
    g = displayio.Group()
    
    y = 0
    x = 0
    for xm in range(8):
        x = 0
        for ym in range(10):
            if gamemap[xm][ym] == "#":
                l = Rect(x,y,2,2,fill=0x202020)
            if gamemap[xm][ym] == "P":
                l = Rect(x,y,2,2,fill=0x000045)
            if gamemap[xm][ym] == "B":
                l = Rect(x,y,2,2,fill=0x100a00)
            if gamemap[xm][ym] == "C":
                l = Rect(x,y,2,2,fill=0x004500)
            if gamemap[xm][ym] == "O":
                l = Rect(x,y,2,2,fill=0x000000)
            g.append(l)
            x = x + 2
        y = y + 2
    l = Rect(14,18,2,2,fill=0x202020)
    
    la = Label(text=str(steps), font=terminalio.FONT, color=0xffffff, scale=1)
    la.x = 21
    la.y = 7
    g.append(la)
    g.append(l)
    display.show(g)

    
    
step = 1
openfile(1)
generatemap()
draw_map(0)
display.refresh()
while True:
    

    ##display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)


    for x in range(1,levels+1):
        targetpos.clear()
        boxpos.clear()
        playerpos.clear()
        gamemap.clear()
        openfile(x)
        generatemap()
        g = displayio.Group()
        draw_map(step)
        display.show(g)
        display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
        step = play(step)
    g = displayio.Group()    
    la = Label(text="Win!!", font=terminalio.FONT, color=0xffffff, scale=1)
    la.y = 7
    la.x = 2
    g.append(la)
    display.show(g)
    display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
    display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
    print("You won!")
    time.sleep(1000)