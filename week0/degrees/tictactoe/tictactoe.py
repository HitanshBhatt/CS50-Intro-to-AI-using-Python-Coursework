"""
Tic Tac Toe Player
"""

import math

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
    num_of_X, num_of_O = 0, 0

    for row in board:
        num_of_X += row.count(X)
        num_of_O += row.count(O)

    return O if num_of_X > num_of_O else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_slots = set()

    for i, row in enumerate(board):
        for j, player_move in enumerate(row):
            if player_move == EMPTY:
                action_slots.add((i, j))

    return action_slots



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)
    board_dup = [row[:] for row in board]  # Make a deep copy of the board
    i, j = action

    if board_dup[i][j] is not EMPTY:
        raise Exception('Invalid move')

    board_dup[i][j] = player_move
    return board_dup



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player_turn in (X, O):

        # Check vertical columns
        for j in range(3):
            if all(board[i][j] == player_turn for i in range(3)):
                return player_turn

        # Check horizontal rows
        for i in range(3):
            if all(board[i][j] == player_turn for j in range(3)):
                return player_turn

        # Check diagonals
        if all(board[i][i] == player_turn for i in range(3)):
            return player_turn
        elif all(board[i][2-i] == player_turn for i in range(3)):
            return player_turn

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If the game is won by any player
    if winner(board) is not None:
        return True

    # If empty spaces still exist in the game board, return False
    for row in board:
        if EMPTY in row:
            return False

    # No moves are possible
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

#AI Code: Will find the best move to play
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    """
    Max value will be represented by X
    Min value will be represented by O
    """

    # Define the maximum_value function that searches for the best move for the maximizing player (X).
    def maximum_value(board):
        optimal_move = ()

        # If the board is in a terminal state, return the utility value and the optimal move.
        if terminal(board):
            return utility(board), optimal_move
        else:
            # Initialize the minimum threshold to a very low value.
            min_threshold = float('-inf')

            # For each possible action on the board, calculate the minimum value that the minimizing player (O) can get.
            for action in actions(board):
                minimum_val = minimum_value(result(board, action))[0]
                # If the current minimum value is greater than the minimum threshold, update the threshold and optimal move.
                if minimum_val > min_threshold:
                    min_threshold = minimum_val
                    optimal_move = action

            # Return the minimum threshold and the optimal move.
            return min_threshold, optimal_move

    # Define the minimum_value function that searches for the best move for the minimizing player (O).
    def minimum_value(board):
        optimal_move = ()

        # If the board is in a terminal state, return the utility value and the optimal move.
        if terminal(board):
            return utility(board), optimal_move
        else:
            # Initialize the maximum threshold to a very high value.
            max_threshold = float('inf')

            # For each possible action on the board, calculate the maximum value that the maximizing player (X) can get.
            for action in actions(board):
                maximum_val = maximum_value(result(board, action))[0]
                # If the current maximum value is less than the maximum threshold, update the threshold and optimal move.
                if maximum_val < max_threshold:
                    max_threshold = maximum_val
                    optimal_move = action

            # Return the maximum threshold and the optimal move.
            return max_threshold, optimal_move
    
    # Get the current player on the board.
    curr_player = player(board)

    # If the board is in a terminal state, return None.
    if terminal(board):
        return None
    
    # If the current player is the minimizing player (O), return the optimal move calculated by the minimum_value function.
    if curr_player == O:
        return minimum_value(board)[1]
    # If the current player is the maximizing player (X), return the optimal move calculated by the maximum_value function.
    else:
        return maximum_value(board)[1]

