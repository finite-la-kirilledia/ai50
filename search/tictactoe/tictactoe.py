"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_square_count = 0
    for row in board:
        for column in row:
            if column == EMPTY:
                empty_square_count += 1

    return X if empty_square_count % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    row_count = len(board)
    column_count = len(board[0])
    empty_squares = set()

    for i in range(row_count):
        for j in range(column_count):
            if board[i][j] == EMPTY:
                empty_squares.add(
                    (i, j)
                )

    return empty_squares


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    i = action[0]
    j = action[1]

    if board_copy[i][j] is not EMPTY:
        raise ValueError(f'Illegal move {action}')

    board_copy[i][j] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    side_length = len(board)

    for row in board:
        if row.count(X) == side_length:
            return X
        elif row.count(O) == side_length:
            return O

    for column in zip(*board):
        if column.count(X) == side_length:
            return X
        elif column.count(O) == side_length:
            return O

    diagonals = [
        [board[i][i] for i in range(side_length)],
        [board[0][2], board[1][1], board[2][0]]
    ]
    for diagonal in diagonals:
        if diagonal.count(X) == side_length:
            return X
        if diagonal.count(O) == side_length:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        for column in row:
            if column == EMPTY:
                return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_player = winner(board)
    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if (player(board)) == X:
        return max_value_move(board)[1]
    else:
        return min_value_move(board)[1]


def max_value_move(board):
    if terminal(board):
        return utility(board), None

    max_value = float('-inf')
    max_move = None
    for action in actions(board):
        enemy_min_value_move = min_value_move(result(board, action))
        enemy_min_value = enemy_min_value_move[0]
        #   enemy_min_move = enemy_min_value_move[1]
        if enemy_min_value > max_value:
            max_value = enemy_min_value
            max_move = action

    return max_value, max_move


def min_value_move(board):
    if terminal(board):
        return utility(board), None

    min_value = float('inf')
    min_move = None
    for action in actions(board):
        enemy_max_value_move = max_value_move(result(board, action))
        enemy_max_value = enemy_max_value_move[0]
        #   enemy_max_move = enemy_max_value_move[1]
        if enemy_max_value < min_value:
            min_value = enemy_max_value
            min_move = action

    return min_value, min_move
