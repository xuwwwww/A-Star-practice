import pygame
# import MazeGen_ver_Import as mz
from  MazeGen_ver_Import import  maplist, stepWidth, wallwidth, canvas_x, canvas_y, wallcolor, backgroundColor
l = len(maplist)-2
w = len(maplist[0])-2
path = ()
pygame.init()
screen = pygame.display.set_mode((canvas_x, canvas_y))
pygame.display.set_caption('Maze')
background = pygame.Surface(screen.get_size())
background.convert()
background.fill(wallcolor)
screen.blit(background, (0, 0))
for i in range(1, w+2, 2):
    for j in range(1, l+2, 2):
        xxx = int((i-1)*stepWidth/2 + wallwidth)
        yyy = int((j-1)*stepWidth/2 + wallwidth)
        pygame.draw.rect(screen, backgroundColor, [xxx, yyy,  stepWidth-wallwidth * 2, stepWidth-wallwidth * 2], 0)
for i in range(1, w+2, 1):
    for j in range(1, l+2, 1):
        xxx = int((i - 1) * stepWidth / 2 + wallwidth)
        yyy = int((j - 1) * stepWidth / 2 + wallwidth)
        if maplist[j][i] == 0:
            pygame.draw.rect(screen, backgroundColor, [xxx, yyy, stepWidth - wallwidth * 2, stepWidth - wallwidth * 2], 0)
            # pygame.display.update()
pygame.display.update()

def a_star_search(start, end):
    """
    search road ,if found end return grid,otherwise None
    :param start:
    :param end:
    :return:
    """

    #waiting to be visited
    open_list = []
    #visited
    close_list = []
    #append start into open list
    open_list.append(start)
    #main loop  check current node each loop
    while len(open_list) > 0:
        #search open_list for min f cost for now node
        current_grid = find_min_gird(open_list)
        #delete min f cost node from open list
        open_list.remove(current_grid)
        #add min f cost node into closed list
        close_list.append(current_grid)
        #search every adjacent node of current node
        neighbors = find_neighbors(current_grid, open_list, close_list)
        for grid in neighbors:
            if grid not in open_list:
                #如果当前节点不在open_list中，标记为父节点，并放入open_list中
                grid.init_grid(current_grid, end)
                open_list.append(grid)
            #如果终点在open_list中，直接返回终点格子
            for grid in open_list:
                if (grid.x == end.x) and (grid.y == end.y):
                    return grid
        #search every options in open_list,if can't find , means not end yet, return none
    return None
def find_min_gird(open_list=[]):
    """
    fing min f_cost
    :param open_list:
    :return:
    """
    temp_grid = open_list[0]
    for grid in open_list:
        if grid.f < temp_grid.f:
            temp_grid = grid
    return temp_grid
def find_neighbors(grid,open_list=[],close_list=[]):
    """
    fin adjecent grid
    :param grid:
    :param open_list:
    :param close_list:
    :return:
    """
    grid_list = []
    if is_valid_grid(grid.x, grid.y-1, open_list, close_list):
        grid_list.append(Grid(grid.x, grid.y-1))
    if is_valid_grid(grid.x, grid.y+1, open_list, close_list):
        grid_list.append(Grid(grid.x, grid.y+1))
    if is_valid_grid(grid.x-1, grid.y, open_list, close_list):
        grid_list.append(Grid(grid.x-1,grid.y))
    if is_valid_grid(grid.x+1, grid.y, open_list, close_list):
        grid_list.append(Grid(grid.x+1, grid.y))
    return grid_list
def is_valid_grid(x,y,open_list=[],close_list=[]):
    """
    decide whether overstep
    :param x:
    :param y:
    :param open_list:
    :param close_list:
    :return:
    """
    #over border
    if x < 0 or x >=len(maplist) or y < 0 or y >= len(maplist[0]):
        return False
    #obstacle
    if maplist[x][y] == 1:
        return False
    #if inopen list
    if contain_grid(open_list, x, y):
        return False
    #if in close list
    if contain_grid(close_list, x, y):
        return False
    return True
def contain_grid(grids, x, y):
    for grid in grids:
        if (grid.x == x) and (grid.y == y):
            return True
    return False
class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None

    def init_grid(self, parent, end):
        self.parent = parent
        if parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 1
        self.h = abs(self.x - end.x) + abs(self.y - end.y)
        self.f = self.g + self.h


start_grid = Grid(1, 1)
end_grid = Grid(l, w)

#find end
result_grid = a_star_search(start_grid, end_grid)
#retrace
path = []
road = []
while result_grid is not None:
    path.append(Grid(result_grid.x, result_grid.y))
    result_grid = result_grid.parent

for paths in path:
    road.append((paths.x, paths.y))
road.reverse()

for r in road:
    xxx = int((r[1] - 1) * stepWidth / 2 + stepWidth / 4 + wallwidth)
    yyy = int((r[0] - 1) * stepWidth / 2 + stepWidth/4 + wallwidth)
    pygame.draw.rect(screen, (150, 150, 150), [xxx, yyy, int((stepWidth - wallwidth * 2)/1.6), int((stepWidth - wallwidth * 2)/1.6)], 0)
    pygame.display.update()


xxx = int((start_grid.x-1) * stepWidth / 2 + stepWidth/4 + wallwidth)
yyy = int((start_grid.y-1) * stepWidth / 2 + stepWidth/4 + wallwidth)
pygame.draw.rect(screen, (0, 255, 0), [yyy, xxx, int((stepWidth - wallwidth * 2) / 1.6), int((stepWidth - wallwidth * 2) / 1.6)], 0)
xxx = int((end_grid.x-1) * stepWidth / 2 + stepWidth/4 + wallwidth)
yyy = int((end_grid.y-1) * stepWidth / 2 + stepWidth/4 + wallwidth)
pygame.draw.rect(screen, (255, 0, 0), [yyy, xxx, int((stepWidth - wallwidth * 2) / 1.6), int((stepWidth - wallwidth * 2) / 1.6)], 0)
pygame.display.update()

running = True

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()