import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win_size  = (660, 660)
pygame.display.set_caption('Tick-tack-toe')
win = pygame.display.set_mode(win_size)

def isInRect(x, y, rect):
    rx0 = rect[0]
    ry0 = rect[1]
    rx1 = rx0 + rect[2]
    ry1 = ry0 + rect[2]

    if (x > rx0) and (x < rx1) and (y > ry0) and (y < ry1):
        return True
    return False

isClicked = [[False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False]]

isCircle = False
clock = pygame.time.Clock()
run = True
pos = -1
while run:
    clock.tick(30)
    for event in pygame.event.get(): # в список сохряняет все события
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    win.fill((92,219,149))

    area_size = win_size[0] - 40
    cell_size = area_size // 9
    for i in range(9):
        for j in range(9):
            rect = (20+cell_size*j, 20 + cell_size*i, cell_size)

            if pos != -1 or isClicked[i][j]:
                draw = isInRect(pos[0], pos[1], rect)
                if draw or isClicked[i][j]:
                    if isCircle:
                        pygame.draw.circle(win, (55,150,131), (rect[0]+cell_size//2, rect[1]+cell_size//2), cell_size//2-5, 2)
                        if not isClicked[i][j]: isCircle = False
                    else:
                        pygame.draw.line(win, (55,150,131), (rect[0]+10, rect[1]+10), (rect[0]+rect[2]-10, rect[1]+rect[2]-10), 3)
                        pygame.draw.line(win, (55,150,131), (rect[0] + rect[2]-10, rect[1]+10), (rect[0]+10, rect[1]+rect[2]-10), 3)
                        if not isClicked[i][j]: isCircle = True
                    isClicked[i][j] = True
        


            pygame.draw.rect(win, (237,245,225), (20 + cell_size*j, 20 + cell_size*i, cell_size, cell_size), 1)


    for i in range(3):
        for j in range(3):
            pygame.draw.rect(win, (5,56,107), (20 + cell_size*j*3, 20 + cell_size*i*3, cell_size*3, cell_size*3), 2)

    pygame.display.update()
