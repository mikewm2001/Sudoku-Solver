# Sudoku solver GUI that instantly provides a Sudoku solution (if possible)
#
# Instructions:
#   Click to select box
#   Enter numbers 1-9 to display potential number to be placed
#                   (Note: program does not allow for incorrect
#                          placements of values)
#   Hit "Enter" to lock in the value to the box
#   Hit "Spacebar" for the program to process a solution for the given board
#
# This GUI also allows a user to solve the board themselves
#                   (Note: Values entered that will result in an
#                          impossible Sudoku board will be deleted)


import pygame
from solver import valid, find_empty, RED, GREEN, BLACK, GRAY, WHITE, WIDTH, HEIGHT
pygame.font.init()
FONT = pygame.font.SysFont("stylus", 60)


class Grid:
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and self.solveable():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0:  # and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (BLACK), (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(self.win, (BLACK), (i * gap, 0),
                             (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def solveable(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solveable():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.update_model()

                if self.solve_gui():
                    self.cubes[row][col].draw_change(self.win, True)
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # Draw the sketch
        if self.temp != 0 and self.value == 0:
            text = FONT.render(str(self.temp), 1, (GRAY))
            win.blit(text, (x+5, y+5))

        # Draw the entered value
        elif self.value != 0:
            text = FONT.render(str(self.value), 1, (BLACK))
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                     y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (RED), (x, y, gap, gap), 3)

    def draw_change(self, win, green=True):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (GREEN), (x, y, gap, gap), 0)

        text = FONT.render(str(self.value), 1, (BLACK))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2),
                 y + (gap / 2 - text.get_height() / 2)))

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    board.draw()
                    pygame.display.update()
                    # Display solution for 100 seconds
                    pygame.time.delay(100000)

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        board.place(board.cubes[i][j].temp)
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        win.fill((WHITE))
        board.draw()
        pygame.display.update()


main()
pygame.quit()
