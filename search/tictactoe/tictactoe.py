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
                empty_squares.add((i, j))

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
    win_pattern_length = len(board)

    for row in board:
        if row.count(X) == win_pattern_length:
            return X
        elif row.count(O) == win_pattern_length:
            return O

    for column in zip(*board):
        if column.count(X) == win_pattern_length:
            return X
        elif column.count(O) == win_pattern_length:
            return O

    diagonals = [
        [board[i][i] for i in range(win_pattern_length)],
        [board[i][j] for i, j in zip(range(win_pattern_length), range(win_pattern_length)[::-1])]
    ]
    for diagonal in diagonals:
        if diagonal.count(X) == win_pattern_length:
            return X
        if diagonal.count(O) == win_pattern_length:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for column in row:
            if column == EMPTY:
                return False

    return True


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

    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]


def max_value(board):
    if terminal(board):
        return utility(board), None

    max_eval = float('-inf')
    max_action = None
    for action in actions(board):
        eval = min_value(result(board, action))
        if eval[0] > max_eval:
            max_eval = eval[0]
            max_action = action

    return max_eval, max_action


def min_value(board):
    if terminal(board):
        return utility(board), None

    min_eval = float('+inf')
    min_action = None
    for action in actions(board):
        eval = max_value(result(board, action))
        if eval[0] < min_eval:
            min_eval = eval[0]
            min_action = action

    return min_eval, min_action
