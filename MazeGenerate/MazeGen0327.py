import pygame
import os
import random
import time
pygame.init()
random.seed()

canvas_x = 1800
canvas_y = 1000
backgroundColor = (0, 0, 0)
stepWidth = 10
pos = [(0, 0)]    #記錄走過的路
deadEnd = [(0, 0)]
x, y = 0, 0
start = 0
facing_list = [0, 1, 2, 3]
pos[0] = (x, y)

window = pygame.display.set_mode((canvas_x, canvas_y))
pygame.display.set_caption("Maze Generator")
background = pygame.Surface(window.get_size())
window.fill(backgroundColor)


def drawwall(x, y, long, width=1, color=(150, 150, 150)):
    wall = pygame.Surface((long, long))
    wall.fill(backgroundColor)
    pygame.draw.rect(window, color, [x, y, long, long], width)
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
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(x+1, y+1, stepWidth-2, stepWidth-2), 1000)
def if_touch_wall(mx, my, printt=True):                                                           #傳入移動的步伐  true 是撞牆
    global x, y, canvas_x, canvas_y, pos, deadEnd
    if x+mx < 0 or x+mx >= canvas_x:
        if printt == True:
            print('touched wall\nunmovable')
        return True
    if y+my < 0 or y+my >= canvas_y:
        if printt == True:
            print('touched wall\nunmovable')
        return True
    try:
        if_visitedb = pos.index((x+mx/2, y+my/2))
        if printt == True:
            print('touched walked route')
    except:                                                                         #如果數值未存在則返回-1 也就是可以往那邊走
        if_visitedb = -1

    try:
        if_visitedb2 = pos.index((x+mx, y+my))
        if printt == True:
            print('touched walked route')
    except:                                                                         #如果數值未存在則返回-1 也就是可以往那邊走
        if_visitedb2 = -1

    try:
        if_visitedd = deadEnd.index((x + mx, y + my))
        if printt == True:
            print('touched dead end')
    except:
        if_visitedd = -1

    if printt == True:
        print('visited', if_visitedd, if_visitedb, if_visitedb2)
    if if_visitedd ==-1 and if_visitedb == -1 and if_visitedb2 == -1:
        unmovable = False       #if touched wall = false
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
def maze_maker(startMakingX= 0, startMakingY= 0):
    global x, y, stepWidth, pos, deadEnd, start
    premove_num = 0                                                             #先設定一個數接收預定要往哪邊走
    for face in range(4):
        premove_num = non_repeat_random()
        fx, fy = facing(premove_num)
        # print('from', int(x), int(y), 'move', int(fx), int(fy), 'towards', int(x+fx), int(y+fy), '   Touched wall==>{} '.format(if_touch_wall(fx, fy, False)))
        # os.system("pause")
        if if_touch_wall(fx, fy, False) == False:                              #沒有撞牆   先試著走一次看看
            pos.append((x, y))                                    #紀錄半步和一步
            x += fx/2
            y += fy/2
            drawpath()
            pos.append((x, y))
            x += fx / 2
            y += fy / 2
            drawpath()
            non_repeat_random(True)                                             #跳出尋找上下左右的迴圈
            # print('successfully moved to %d %d\n'%(x, y))
            break
        else:                                                                   #撞牆了
            # print('bumped wall %d times\nreturning.......\n' % (face+1))
            if face == 3:                                                       #都走過了
                # print('all visited')
                # print('dead ends ===>', deadEnd)
                #
                # print('positions ===>', pos)
                # os.system('pause')
                # pygame.quit()
                # print('now x y=', x, y)
                deadEnd.append((x, y))
                x, y = pos.pop()
                # print('now x y=', x, y)

                x, y = pos.pop()

                # print('now x y=', x, y)
                # print(deadEnd)
                # print(len(pos))
                re_pos = pos[:]
                re_pos.reverse()
                # print(re_pos)
                re_pos.clear()
                # time.sleep(10)
                non_repeat_random(True)
                if start == 1 and pos[0] == (x, y):
                    time.sleep(1000)

    return



clock = pygame.time.Clock()
run = True
pygame.draw.rect(window, (0, 0, 0), pygame.Rect(x+1, y+1, stepWidth - 2, stepWidth - 2), 1000)
drawloop(stepWidth)
while run:
    # clock.tick(5000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    maze_maker()
    start =1
    pygame.display.update()
pygame.quit()