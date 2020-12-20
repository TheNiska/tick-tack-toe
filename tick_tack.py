import pygame, os
import numpy as np

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win_size  = (661, 661)
pygame.display.set_caption('Tick-tack-toe')
win = pygame.display.set_mode(win_size)

COLORS = {'bg_color':      ((92,219,149), (153,115,142),(202,250,254),(22, 22, 22),(25,0,97), (26,26,29), (39,39,39) ),
          'cells_color':   ((237,245,225),(47,47,162),  (151,202,239),(145,113,99),(36,0,145), (78,78,80),(20,167,108) ),
          'outline_color': ((5,56,107),   (85,61,103),  (85,188,201),(142,228,175), (53,0,211), (111,34,50), (255,101,47)),
          'sign_color':    ((55,150,131), (246,76,114), (240,108,149),(237,245,225),(170,170,210), (195,7,63), (255,228,0) )
           }


def isInRect(x, y, rect):
    rx0 = rect[0]
    ry0 = rect[1]
    rx1 = rx0 + rect[2]
    ry1 = ry0 + rect[2]

    if (x > rx0) and (x < rx1) and (y > ry0) and (y < ry1):
        return True
    return False


class Cell():
    def __init__(self, subfield_size, subfield_x0, subfield_y0, n_row, n_col):
        self.cell_size = subfield_size // 3
        self.x0 = subfield_x0 + self.cell_size * n_col
        self.y0 = subfield_y0 + self.cell_size * n_row
        self.isDrawn = False
        self.isCircle = False


class Subfield():
    def __init__(self, win_size, n_row, n_col):
        self.cell_size = (win_size[0] - 40) // 3
        self.x0 = 20 + self.cell_size * n_col
        self.y0 = 20 + self.cell_size * n_row
        self.n_row = n_row
        self.n_col = n_col
        self.isWon = False
        self.isWonByCircle = False
        self.cells = []
        self.wonCount = 0

        for i in range(3): # 3 x 3 matrics
            row = []
            for j in range(3):
                row.append(Cell(self.cell_size-1, self.x0-1, self.y0, i, j))
            self.cells.append(row)


    def isSubfieldWon(self):
        matrix = np.zeros((3,3), dtype=int)
        for i in range(3):
            for j in range(3):
                if self.cells[i][j].isDrawn:
                    if self.cells[i][j].isCircle:
                        matrix[i,j] = 0
                    else:
                        matrix[i,j] = 1
                else:
                    matrix[i,j] = -1

        for i in range(3):
            if np.max(matrix[:,i]) == np.min(matrix[:,i]):
                if matrix[0,i] == 0:
                    self.isWon = True
                    self.isWonByCircle = True
                    field.main_matrix[self.n_row, self.n_col] = 0
                elif matrix[0,i] == 1:
                    self.isWon = True
                    self.isWonByCircle = False
                    field.main_matrix[self.n_row, self.n_col] = 1

            if np.max(matrix[i,:]) == np.min(matrix[i,:]):
                if matrix[i,0] == 0:
                    self.isWon = True
                    self.isWonByCircle = True
                    field.main_matrix[self.n_row, self.n_col] = 0
                elif matrix[i,0] == 1:
                    self.isWon = True
                    self.isWonByCircle = False
                    field.main_matrix[self.n_row, self.n_col] = 1

        diag1 = np.diag(matrix)
        diag2 = np.diag(np.flip(matrix, axis=0))
        diags = (diag1, diag2)

        for i in range(2):
            if (diags[i] == diags[i][0]).all():
                if diags[i][0] == 0:
                    self.isWon = True
                    self.isWonByCircle = True
                    field.main_matrix[self.n_row, self.n_col] = 0
                elif diags[i][0] == 1:
                    self.isWon = True
                    self.isWonByCIrcle = False
                    field.main_matrix[self.n_row, self.n_col] = 1

        # print(field.main_matrix)


class Field():
    def __init__(self, win_size, colorScheme):
        self.clr = colorScheme
        self.x0 = 20
        self.y0 = 20
        self.width = win_size[0] - 40

        self.main_cells = [] # 3 x 3 matrics

        for i in range(3):
            row = []
            for j in range(3):
                row.append(Subfield(win_size, i, j))
            self.main_cells.append(row)

        self.main_matrix = np.array([[-1, -1, -1],
                                     [-1, -1, -1],
                                     [-1, -1, -1]])


    def isGameOver(self):
        for i in range(3):
            if (np.max(self.main_matrix[i,:]) == np.min(self.main_matrix[i,:])) and (self.main_matrix[i,0] != -1):
                if self.main_matrix[i,0] == 0:
                    return 0
                else:
                    return 1
            elif (np.max(self.main_matrix[:,i]) == np.min(self.main_matrix[:,i])) and (self.main_matrix[0,i] != -1):
                if self.main_matrix[0,i] == 0:
                    return 0
                else:
                    return 1
        diag1 = np.diag(self.main_matrix)
        diag2 = np.diag(np.flip(self.main_matrix, axis=0))
        if np.max(diag1) == np.min(diag1) and diag1[0] != -1:
            if diag1[0] == 0:
                return 0
            else:
                return 1
        elif np.max(diag2) == np.min(diag2) and diag2[0] != -1:
            if diag2[0] == 0:
                return 0
            else:
                return 1

        return -1


isCircle = True
clock = pygame.time.Clock()
run = True
pos = -1

field = Field(win_size, 3)

while run:
    clock.tick(22)
    for event in pygame.event.get(): # в список сохряняет все события
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                temp_color = field.clr
                pos = -1
                del field

                if temp_color < 6:
                    temp_color +=1
                else:
                    temp_color = 0
                field = Field(win_size, temp_color)

    win.fill(COLORS['bg_color'][field.clr])

    cell_size = (win_size[0] - 40) // 9
    if field.isGameOver() == -1:
        for i in range(3):
            for j in range(3):
                if not field.main_cells[i][j].isWon:
                    for m in range(3):
                        for n in range(3):
                            mini_x = field.main_cells[i][j].cells[m][n].x0
                            mini_y = field.main_cells[i][j].cells[m][n].y0
                            c_size = field.main_cells[i][j].cells[m][n].cell_size
                            rect = (mini_x, mini_y, c_size)
                            pygame.draw.rect(win, COLORS['cells_color'][field.clr], (mini_x, mini_y, c_size, c_size), 2)

                            if pos != -1 and isInRect(pos[0], pos[1], rect):
                                if not field.main_cells[i][j].cells[m][n].isDrawn:
                                    field.main_cells[i][j].cells[m][n].isDrawn = True
                                    isCircle = not isCircle
                                    field.main_cells[i][j].cells[m][n].isCircle = isCircle
                                    field.main_cells[i][j].isSubfieldWon() # check if area is won


                            if field.main_cells[i][j].cells[m][n].isDrawn:
                                if field.main_cells[i][j].cells[m][n].isCircle:
                                    pygame.draw.circle(win, COLORS['sign_color'][field.clr], (mini_x + c_size//2, mini_y+c_size//2), c_size//2-5, 3)
                                else:
                                    pygame.draw.line(win, COLORS['sign_color'][field.clr], (mini_x+10, mini_y+10), (mini_x+c_size-10, mini_y+c_size-10), 4)
                                    pygame.draw.line(win, COLORS['sign_color'][field.clr], (mini_x + c_size-10, mini_y+10), (mini_x+10, mini_y+c_size-10), 4)


                else:
                    if field.main_cells[i][j].isWonByCircle:
                        pygame.draw.circle(win, COLORS['sign_color'][field.clr], (field.main_cells[i][j].x0 + field.main_cells[i][j].cell_size//2, field.main_cells[i][j].y0 + field.main_cells[i][j].cell_size//2), field.main_cells[i][j].cell_size//2-12, 3)
                    else:
                        pygame.draw.line(win, COLORS['sign_color'][field.clr], (field.main_cells[i][j].x0+24, field.main_cells[i][j].y0+24), (field.main_cells[i][j].x0+field.main_cells[i][j].cell_size-24, field.main_cells[i][j].y0+field.main_cells[i][j].cell_size-24), 4)
                        pygame.draw.line(win, COLORS['sign_color'][field.clr], (field.main_cells[i][j].x0 + field.main_cells[i][j].cell_size-24, field.main_cells[i][j].y0+24), (field.main_cells[i][j].x0+24, field.main_cells[i][j].y0+field.main_cells[i][j].cell_size-24), 4) 

        for i in range(3):
            for j in range(3):
                pygame.draw.rect(win, COLORS['outline_color'][field.clr], (18 + cell_size*j*3, 19 + cell_size*i*3, cell_size*3, cell_size*3), 3)

    else:
        if field.isGameOver() == 0:
            pygame.draw.circle(win, COLORS['sign_color'][field.clr], (win_size[0]//2, win_size[1]//2), win_size[0]//2-25, 6)
        else:
            pygame.draw.line(win, COLORS['sign_color'][field.clr], (40, 40), (win_size[0] - 40, win_size[1] - 40), 7)
            pygame.draw.line(win, COLORS['sign_color'][field.clr], (40, win_size[1] - 40), (win_size[0] - 40, 40), 7)

    
    pygame.display.update()