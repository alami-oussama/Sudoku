# Solve the sudoku board
def solve(board):
    position = blank_cell(board)

    if position == None:
        return True

    row, column = position
    for number in range(1, 10):
        if is_valid(board, position, number) == True:
            board[row][column] = number

            if not solve(board):
                board[row][column] = 0
                continue

            return True

    return False

# Chack if the number is valid in the cell
def is_valid(board, position, number):
    row, column = position

    # Check row
    for i in range(9):
        if board[i][column] == number:
            return False
    
    # Check column
    for j in range(9):
        if board[row][j] == number:
            return False

    # Check box
    box_row, box_column = row // 3, column // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_column * 3, box_column * 3 + 3):
            if board[i][j] == number:
                return False

    return True

# Return a blank cell
def blank_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None