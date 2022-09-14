import pygame
import os
import random
import numpy as np
import time
import sys
np.set_printoptions(threshold=sys.maxsize)
startt = time.time()
pygame.init()
random.seed()

canvas_x = 1000
canvas_y = 1000
backgroundColor = (60, 80, 130)
wallwidth = 2
wallcolor = (0, 0, 0)
stepWidth = 10
# x, y = 0, 0

maplist = [[1 for i in range(int(canvas_x//stepWidth)*2+1)] for j in range(int((canvas_y//stepWidth)*2+1))]
maplist2 = np.ones(((canvas_y//stepWidth)*2+1, (canvas_x//stepWidth)*2+1), dtype=int)
for i in range(1, int(canvas_x / stepWidth) * 2 + 1, 2):
    for j in range(1, int((canvas_y / stepWidth) * 2 + 1), 2):
        maplist[j][i] = 0
        maplist2[j][i] = 0

x = random.randint(0, canvas_x//stepWidth) * stepWidth
y = random.randint(0, canvas_y//stepWidth) * stepWidth
pos = [(0, 0)]    #記錄走過的路
deadEnd = []
start = 0
facing_list = [0, 1, 2, 3]
finishMaking = 0
pos[0] = (x, y)

window = pygame.display.set_mode((canvas_x, canvas_y))
pygame.display.set_caption("Maze")
# background = pygame.Surface(window.get_size())
window.fill(backgroundColor)

def drawwall(x, y, long):
    global wallwidth, wallcolor
    wall = pygame.Surface((long, long))
    wall.fill(backgroundColor)
    pygame.draw.rect(window, wallcolor, [x, y, long, long], wallwidth)
def drawloop(width):
    jumpW = canvas_x//width
    jumpH = canvas_y//width
    nowx, nowy = 0, 0
    for i in range(0, jumpW):
        nowx=i*width
        for j in range(0, jumpH):
            nowy= j*width
            drawwall(nowx, nowy, width)
def drawpath():
    global stepWidth, backgroundColor, wallwidth
    pygame.draw.rect(window, backgroundColor, pygame.Rect(x+wallwidth, y+wallwidth, stepWidth-wallwidth*2, stepWidth-wallwidth*2), stepWidth)
def if_touch_wall(mx, my, printt=True):                                                           #傳入移動的步伐  true 是撞牆
    global x, y, canvas_x, canvas_y, pos, deadEnd
    if x + mx < 0 or x + mx >= canvas_x:
        if printt == True:
            print('touched wall\nunmovable')
        return True
    if y + my < 0 or y + my >= canvas_y:
        if printt == True:
            print('touched wall\nunmovable')
        return True
    if_visitedb = if_visitedd = True
    if not (x + mx, y + my) in pos:
        if_visitedb = False
    if not (x + mx, y + my) in deadEnd:
        if_visitedd = False
    if printt == True:
        print('visited', if_visitedd, if_visitedb)

    if if_visitedd == False and if_visitedb == False:
        unmovable = False  # if touched wall = false
        if printt == True:
            print('movable')
    else:
        unmovable = True
        if printt == True:
            print('unmovable')
    return unmovable
def non_repeat_random(refresh = False):
    global facing_list
    pop_up_num = 0
    if refresh == True:
        facing_list.clear()
        # print('random refreshing')
        for j in range(4):
            facing_list.append(j)
    else:
        random.shuffle(facing_list)
        pop_up_num = facing_list.pop(0)
    return pop_up_num
def facing(ranNum):                                                     # 上下左右 1234   回傳應該移動的值
    if ranNum == 0:
        return [0, stepWidth]
    elif ranNum == 1:
        return [0, -stepWidth]
    elif ranNum == 2:
        return [-stepWidth, 0]
    elif ranNum == 3:
        return [stepWidth, 0]
    else:
        print("error")
        os.system("pause")
        return -1                                                  #
def maze_maker():
    global x, y, stepWidth, pos, deadEnd, start, finishMaking
    premove_num = 0                                                             #先設定一個數接收預定要往哪邊走
    for face in range(4):
        premove_num = non_repeat_random()
        fx, fy = facing(premove_num)
        # print('from', int(x), int(y), 'move', int(fx), int(fy), 'towards', int(x+fx), int(y+fy), '   Touched wall==>{} '.format(if_touch_wall(fx, fy, False)))
        # os.system("pause")
        if if_touch_wall(fx, fy, False) == False:
            pos.append((x, y))
            x += fx/2
            y += fy/2
            drawpath()
            pos.append((x, y))
            maplist[int(y/(stepWidth/2) + 1)][int(x/(stepWidth/2) + 1)] = 0
            maplist2[int(y/(stepWidth/2) + 1)][int(x/(stepWidth/2) + 1)] = 0

            x += fx / 2
            y += fy / 2
            drawpath()
            non_repeat_random(True)
            break
        else:
            if face == 3:
                deadEnd.append((x, y))
                pos.pop()
                x, y = pos.pop()
                non_repeat_random(True)
                if start == 1 and pos[0] == (x, y):
                    finishMaking = True
    return

clock = pygame.time.Clock()
run = True
drawloop(stepWidth)
while run:
    # clock.tick(0.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if finishMaking == 0:
        maze_maker()
    elif finishMaking == 1:
        pygame.display.update()
        print('finish with time %.2f' % (time.time()-startt))
        # print(maplist2)
        finishMaking = 2
        # run = False
    else:
        pass

    start = 1
pygame.quit()