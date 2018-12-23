#!/usr/bin/env python
from isolation import Board, game_as_text
from random import randint


# This file is your main submission that will be graded against. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.
class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


class OpenMoveEvalFn:
    def score(self, game, maximizing_player_turn=True):
        """Score the current game state

        Evaluation function that outputs a score equal to how many
        moves are open for AI player on the board minus how many moves
        are open for Opponent's player on the board.
        Note:
            exercise1. Be very careful while doing opponent's moves. You might end up
               reducing your own moves.
            3. If you think of better evaluation function, do it in CustomEvalFn below.

            Args
                param1 (Board): The board and game state.
                param2 (bool): True if maximizing player is active.

            Returns:
                float: The current state's score. MyMoves-OppMoves.

            """
        if maximizing_player_turn == True:
            # if current player lose
            if len(game.get_legal_moves()) == 0:
                return float(-1e9)
            # if opponent player loser
            if len(game.get_opponent_moves()) == 0:
                return float(1e9)

            player_moves = len(game.get_legal_moves())
            opponent_moves = len(game.get_opponent_moves())
        # if Opponent Player
        else:
            if len(game.get_opponent_moves()) == 0:
                return float(-1e9)
            if len(game.get_legal_moves()) == 0:
                return float(1e9)
            opponent_moves = len(game.get_legal_moves())
            player_moves = len(game.get_opponent_moves())
        return float(player_moves - opponent_moves)


class CustomEvalFn:
    def __init__(self):
        pass

    def get_sum_jumping_runs(self, game, player_y_pos, player_x_pos, moves):
        """This function measures the longest run of jumping moves that can be performed inside the 3x3 squares
        defined by a starting position and each of its legal moves left. The longest run one can hope to reach is 7.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        player_y_pos, player_x_pos : int, int
            The player's position to evaluate based on its longest jumping run.
        moves : `list` of legal moves for 'player'
            List` of legal moves for 'player'
        Returns
        -------
        int
            The longest run found.
        """
        sum_jumping_runs = 0
        for move_y, move_x, dummy in moves:
            if move_y == player_y_pos + 1 and move_x == player_x_pos + 2:  # Pos exercise1
                # Start the run going East-South

                if not game.move_is_legal(player_y_pos - 1, player_x_pos + 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 2):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos + 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos + 2):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos - 1 and move_x == player_x_pos + 2:  # Pos exercise1
                # Start the run going East-North

                if not game.move_is_legal(player_y_pos + 1, player_x_pos + 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 2):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos + 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos + 2):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos - 2 and move_x == player_x_pos + 1:  # Pos exercise1
                # Start the run going North-East

                if not game.move_is_legal(player_y_pos, player_x_pos + 2):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 2, player_x_pos + 2):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 1):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 2, player_x_pos):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos + 2):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos - 2 and move_x == player_x_pos - 1:  # Pos exercise1

                if not game.move_is_legal(player_y_pos - 1, player_x_pos + 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos - 1):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 2, player_x_pos):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 1):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos - 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 2, player_x_pos + 1):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos - 1 and move_x == player_x_pos - 2:  # Pos exercise1
                # Start the run going West-North

                if not game.move_is_legal(player_y_pos + 1, player_x_pos - 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos - 2):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos - 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos - 2):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos + 1 and move_x == player_x_pos - 2:  # Pos exercise1
                # Start the run going West-South

                if not game.move_is_legal(player_y_pos - 1, player_x_pos - 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos - 2):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos - 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos - 1, player_x_pos - 2):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos + 2 and move_x == player_x_pos - 1:  # Pos exercise1
                # Start the run going South-West

                if not game.move_is_legal(player_y_pos + 1, player_x_pos + 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos - 1):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 2, player_x_pos):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 1):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos - 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 2, player_x_pos + 1):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

            if move_y == player_y_pos + 2 and move_x == player_x_pos + 1:  # Pos exercise1
                # Start the run going South-East

                if not game.move_is_legal(player_y_pos + 1, player_x_pos - 1):  # Pos 2
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos + 1):  # Pos 3
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 2, player_x_pos):  # Pos 4
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos, player_x_pos - 1):  # Pos 5
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 1, player_x_pos + 1):  # Pos 6
                    continue
                else:
                    sum_jumping_runs += 1
                if not game.move_is_legal(player_y_pos + 2, player_x_pos - 1):  # Pos 7
                    continue
                else:
                    sum_jumping_runs += 1
                    continue

        return sum_jumping_runs

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state

        Custom evaluation function that acts however you think it should. This
        is not required but highly encouraged if you want to build the best
        AI possible.

        Args
            game (Board): The board and game state.
            maximizing_player_turn (bool): True if maximizing player is active.

        Returns:
            float: The current state's score, based on your own heuristic.

        """

        # Return a score depend on intersection between Player legal move and opponent legal move
        urr_moves = game.get_legal_moves()

        if maximizing_player_turn:
            opp_moves = len(game.get_opponent_moves())
            # opp_prev_moves = len(self.prevGame.get_legal_moves())
            plyr_moves = len(game.get_legal_moves())

            # plyr_prev_moves = len(self.prevGame.get_opponent_moves())
        else:
            opp_moves = len(game.get_legal_moves())
            plyr_moves = len(game.get_opponent_moves())
            # opp_prev_moves = len(self.prevGame.get_legal_moves())

        if game.move_count <= 2:
            return plyr_moves
            # this is the first move, any player can go anywhere
        elif plyr_moves == 0 and not opp_moves == 0:
            # no moves for me, idx lose
            return -1e9
        elif opp_moves == 0 and not plyr_moves == 0:
            # no moves for opp, idx root
            return 1e9
        elif opp_moves == plyr_moves and plyr_moves == 0:
            # this is a tie
            return -5
        else:
            return plyr_moves - opp_moves * .5


class CustomPlayer:
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, search_depth=2, eval_fn=CustomEvalFn()):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent

            Note:
                exercise1. Do NOT change the user_name of this 'move' function. We are going to call
                the this function directly.
                2. Change the user_name of minimax function to alphabeta function when
                required. Here we are talking about 'minimax' function call,
                NOT 'move' function user_name.
                Args:
                game (Board): The board and game state.
                legal_moves (list): List of legal moves
                time_left (function): Used to determine time left before timeout

            Returns:
                tuple: best_move
            """

        # Choice between Minimax and alphabeta as u like
        # best_move, utility = self.minimax(game, time_left, depth=self.search_depth)
        best_move, utility = self.alphabeta(game, time_left, depth=self.search_depth)
        return best_move

    def utility(self, game, maximizing_player):
        """Can be updated if desired. Not compulsory. """
        return self.eval_fn.score(game)

    def minimax(self, game, time_left, depth, maximizing_player=True):
        """Implementation of the minimax algorithm

        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, val
        """

        path = []
        best_val, best_move = self.minimax_max_value(game, depth, path, time_left)

        # return the first node of the path
        return best_move[0], best_val

    def minimax_max_value(self, game, depth, path, time_left, maximizing_player=True):
        # base case end of depth
        if depth == 0:
            return self.eval_fn.score(game, maximizing_player), path

        # Get moves
        legal_moves = game.get_legal_moves()
        #  Best answer variable ( score,move)
        ans = (float(-1e9), [(-1, -1)])

        for move in legal_moves:
            # Try each move
            tried_game = game.forecast_move(move)[0]

            # Try the move and get the score and path
            move_score = self.minimax_min_value(tried_game, depth - 1, path, time_left, not maximizing_player)[0]

            # if it's a better
            if move_score > ans[0]:
                ans = (move_score, path + [move])

        return ans

    def minimax_min_value(self, game, depth, path, time_left, maximizing_player=True):
        if depth == 0:
            return self.eval_fn.score(game, maximizing_player), path

        # Get moves
        legal_moves = game.get_legal_moves()
        #  Best answer variable ( score,move)
        ans = (float(1e9), [(-1, -1)])

        for move in legal_moves:
            # Try each move
            tried_game = game.forecast_move(move)[0]
            # Try the move and get the score and path
            move_score = self.minimax_max_value(tried_game, depth - 1, path, time_left, not maximizing_player)[0]

            # if it's a better
            if move_score < ans[0]:
                ans = (move_score, path + [move])

        return ans

    def alphabeta(self, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implementation of the alphabeta algorithm

        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, val
        """
        path = []
        val, path = self.alphabeta_max_value(game, time_left, depth, path, alpha, beta, maximizing_player)
        if len(path) == 0:
            return (-1, -1), float(-1e9)
        best_move = path[0]
        return best_move, val

    def alphabeta_max_value(self, game, time_left, depth, path, alpha, beta, maximizing_player):
        if depth == 0:
            return self.eval_fn.score(game, maximizing_player), path

        # Get moves
        legal_moves = game.get_legal_moves()
        #  Best answer variable ( score,move)
        ans = (float(-1e9), [(-1, -1)])
        for move in legal_moves:
            # Try each move
            tried_game = game.forecast_move(move)[0]
            # Try the move and get the score and path
            move_score = \
                self.alphabeta_min_value(tried_game, time_left, depth - 1, path, alpha, beta, not maximizing_player)[0]
            # if it's a better
            if move_score > ans[0]:
                ans = (move_score, path + [move])

            # Make Pruning
            if move_score >= beta:
                return (move_score, path + [move])

            alpha = max(alpha, move_score)
        return ans

    def alphabeta_min_value(self, game, time_left, depth, path, alpha, beta, maximizing_player):
        if depth == 0:
            return self.eval_fn.score(game, maximizing_player), path

        # Get moves
        legal_moves = game.get_legal_moves()
        #  Best answer variable ( score,move)
        ans = (float(1e9), [(-1, -1)])
        for move in legal_moves:
            # Try each move
            tried_game = game.forecast_move(move)[0]
            # Try the move and get the score and path
            move_score = \
                self.alphabeta_max_value(tried_game, time_left, depth - 1, path, alpha, beta, not maximizing_player)[0]
            # if it's a better
            if move_score < ans[0]:
                ans = (move_score, move)

            # Make Pruning
            if move_score <= alpha:
                return move_score, path + [move]

            beta = min(beta, move_score)
        return ans
