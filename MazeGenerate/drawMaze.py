import pygame
import MazeGen0329 as mz
l = len(mz.maplist)-2
w = len(mz.maplist[0])-2
print(l, w)

pygame.init()
screen = pygame.display.set_mode((mz.canvas_x, mz.canvas_y))
pygame.display.set_caption('Maze')
background = pygame.Surface(screen.get_size())
background.convert()
background.fill(mz.wallcolor)
screen.blit(background, (0, 0))
pygame.display.update()



for i in range(1, w+2, 2):
    for j in range(1, l+2, 2):
        xxx = int((i-1)*mz.stepWidth/2 + mz.wallwidth)
        yyy = int((j-1)*mz.stepWidth/2 + mz.wallwidth)
        pygame.draw.rect(screen, mz.backgroundColor, [xxx, yyy,  mz.stepWidth-mz.wallwidth * 2, mz.stepWidth-mz.wallwidth * 2], 0)


for i in range(1, w+2, 1):
    for j in range(1, l+2, 1):
        xxx = int((i - 1) * mz.stepWidth / 2 + mz.wallwidth)
        yyy = int((j - 1) * mz.stepWidth / 2 + mz.wallwidth)
        if mz.maplist[j][i] == 0:
            pygame.draw.rect(screen, mz.backgroundColor, [xxx, yyy, mz.stepWidth - mz.wallwidth * 2, mz.stepWidth - mz.wallwidth * 2], 0)

pygame.display.update()
start = (1, 1)
end = (l, w)
print(start, end)

# pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(int((route[1]-1)*mz.stepWidth//2+mz.stepWidth//4), int((route[0]-1)*mz.stepWidth//2 + mz.stepWidth//4), int((mz.stepWidth / 1.9 - mz.wallwidth)),  int((mz.stepWidth / 1.9 - mz.wallwidth))), 0)
pygame.display.update()


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()