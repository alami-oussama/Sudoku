import pygame
import os
from generator import generate_board
from solver import is_valid, solve

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
DARK_BLUE = (25, 73, 114)
LIGHT_BLUE = (24, 108, 179)
CYAN = (204, 229, 255)
LIGHT_RED = (240, 128, 128)

FPS = 60

class Board:
    def __init__(self, board):
        self.board = board
        self.INITIAL_BOARD = [[self.board[i][j] for j in range(9)] for i in range(9)]

    CELL_SIZE = 75
    PADDING = 20

    def board_background(self):
        GRID_BACKGROUND = pygame.Rect(self.PADDING, self.PADDING, 9 * self.CELL_SIZE, 9 * self.CELL_SIZE)
        pygame.draw.rect(SCREEN, WHITE, GRID_BACKGROUND)

    def draw_grid(self):
        for x in range(self.PADDING, 9 * self.CELL_SIZE, self.CELL_SIZE):
            for y in range(self.PADDING, 9 * self.CELL_SIZE, self.CELL_SIZE):
                rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(SCREEN, GREY, rect, 1)

        for x in range(self.PADDING, 10 * self.CELL_SIZE, self.CELL_SIZE): 
            if (x // self.CELL_SIZE) % 3 == 0:
                    pygame.draw.line(SCREEN, BLACK, (x, self.PADDING), (x, 9 * self.CELL_SIZE + self.PADDING), 3)

        for y in range(self.PADDING, 10 * self.CELL_SIZE, self.CELL_SIZE):
            if (y // self.CELL_SIZE) % 3 == 0:
                pygame.draw.line(SCREEN, BLACK, (self.PADDING, y), (9 * self.CELL_SIZE + self.PADDING, y), 3)

    def board_init(self):
        self.CELL_SIZE = 75
        self.PADDING = 20
        FONT = pygame.font.SysFont('comicsans', 50)
        for i in range(9):
            for j in range(9):
                if self.INITIAL_BOARD[i][j] != 0:
                    number = FONT.render(str(self.INITIAL_BOARD[i][j]), 1, LIGHT_BLUE)
                    x = i * self.CELL_SIZE + self.PADDING + self.CELL_SIZE // 2 - number.get_width() // 2
                    y = j * self.CELL_SIZE + self.PADDING + self.CELL_SIZE // 2 - number.get_height() // 2
                    SCREEN.blit(number, (x, y))

    def darw_numbers(self):
        self.CELL_SIZE = 75
        self.PADDING = 20
        FONT = pygame.font.SysFont('comicsans', 45)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 and self.INITIAL_BOARD[i][j] == 0:
                    number = FONT.render(str(self.board[i][j]), 1, BLACK)
                    x = i * self.CELL_SIZE + self.PADDING + (self.CELL_SIZE - number.get_width()) // 2
                    y = j * self.CELL_SIZE + self.PADDING + (self.CELL_SIZE - number.get_height()) // 2
                    SCREEN.blit(number, (x, y))
        self.board_init()

    def select_cell(self, position, invalid_cell):
        if position == None:
            return False
        row, column = map(lambda x: (x - self.PADDING) // self.CELL_SIZE, position)
        if row < 0 or row > 8 or column < 0 or column > 8:
            return False
        if position == invalid_cell:
            color = LIGHT_RED
        else:
            color = CYAN
        row, column = map(lambda x: ((x - self.PADDING) // self.CELL_SIZE) * self.CELL_SIZE, position)
        rect = pygame.Rect(row + self.PADDING, column + self.PADDING, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(SCREEN, color, rect)

    invalid_cell = None
    def update_board(self, position, number):
        if number == -1 or position == None:
            return False
        row, column = map(lambda x: (x - self.PADDING) // self.CELL_SIZE, position)
        if row < 0 or row > 8 or column < 0 or column > 8:
            return False
        if self.INITIAL_BOARD[row][column] == 0:
            if is_valid(self.board, (row, column), number) or number == 0:
                self.board[row][column] = number
                self.invalid_cell = None
            else:
                self.invalid_cell = position

    def clear_changes(self):
        self.board = [[self.INITIAL_BOARD[i][j] for j in range(9)] for i in range(9)]

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0
                self.INITIAL_BOARD[i][j] = 0

    def generate_board(self):
        board = generate_board()
        for i in range(9):
            for j in range(9):
                self.board[i][j] = board[i][j]
                self.INITIAL_BOARD[i][j] = board[i][j]
    
    def solve(self):
        solve(self.board)
    
    def draw(self, position, number):
        self.update_board(position, number)
        self.board_background()
        self.select_cell(position, self.invalid_cell)
        self.draw_grid()
        self.darw_numbers()

class Button:
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    color = WHITE

    def button_clicked(self, click_position, event):
        if click_position == None:
            return False
        x, y = click_position
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            event()

    def draw_button(self):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, self.color, rect)
        outline = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(SCREEN, BLACK, outline, 3)
        FONT = pygame.font.SysFont('comicsans', 45)
        text = FONT.render(self.text, 1, BLACK)
        position = (self.x + (self.w  - text.get_width()) // 2, self.y + (self.h - text.get_height()) // 2)
        SCREEN.blit(text, position)

    def hover(self, hover_position):
        if hover_position == None:
            return False
        x, y = hover_position
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            self.color = GREY
        else:
            self.color = WHITE

    def draw(self, hover_position, click_position, event):
        self.draw_button()
        self.hover(hover_position)
        self.button_clicked(click_position, event)

class Menu(Board):
    def __init__(self):
        pass

    # Creat menu
    PADDING = 20
    W = 540
    H = HEIGHT - PADDING * 2
    X, Y = WIDTH - W - PADDING, PADDING

    def draw_menu(self):
        rect = pygame.Rect(self.X, self.Y, self.W, self.H)
        pygame.draw.rect(SCREEN, BLACK, rect, 3)
    # Creat menu buttons
    create_board_button = Button(840, 120, 300, 100, "New Board")
    empty_board_button = Button(840, 240, 300, 100, "Empty Board")
    clear_board_button = Button(840, 360, 300, 100, "Clear")
    solve_board_button = Button(840, 480, 300, 100, "Solve")

    def draw_buttons(self, hover_position, click_position):
        self.create_board_button.draw(hover_position, click_position, board.generate_board)
        self.empty_board_button.draw(hover_position, click_position, board.clear_board)
        self.clear_board_button.draw(hover_position, click_position, board.clear_changes)
        self.solve_board_button.draw(hover_position, click_position, board.solve)

    def draw(self, hover_position, click_position):
        self.draw_menu()
        self.draw_buttons(hover_position, click_position)

def draw(position, number, hover_position, click_position):
    SCREEN.fill(DARK_BLUE)
    board.draw(position, number)
    menu.draw(hover_position, click_position)
    pygame.display.update()

def main():
    position = None
    clock = pygame.time.Clock()
    quit = False
    while not quit:
        number = -1
        click_position = None
        hover_position = None
        clock.tick(FPS)
        for event in pygame.event.get():
            hover_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                click_position = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    number = 1
                if event.key == pygame.K_2:
                    number = 2
                if event.key == pygame.K_3:
                    number = 3
                if event.key == pygame.K_4:
                    number = 4
                if event.key == pygame.K_5:
                    number = 5
                if event.key == pygame.K_6:
                    number = 6
                if event.key == pygame.K_7:
                    number = 7
                if event.key == pygame.K_8:
                    number = 8
                if event.key == pygame.K_9:
                    number = 9
                if event.key == pygame.K_BACKSPACE:
                    number = 0

        draw(position, number, hover_position, click_position)

    pygame.quit()

if __name__ == "__main__":
    board = Board(generate_board())
    menu = Menu()
    main()