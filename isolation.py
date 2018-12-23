from copy import deepcopy
import time
import platform
import random
# import io
import StringIO
# import resource
if platform.system() != 'Windows':
    import resource

import sys
import os
sys.path[0] = os.getcwd()


class Board:
    BLANK = " "
    BLOCKED = "X"
    NOT_MOVED = (-1, -1, False)

    __player_1__ = None
    __player_2__ = None
    __queen_1__ = None
    __queen_2__ = None

    __active_player__ = None
    __inactive_player__ = None
    __active_players_queen__ = None
    __inactive_players_queen__ = None

    __last_queen_move__ = {}
    __last_queen_symbols__ = {}

    move_count = 0

    def __init__(self, player_1, player_2, width=7, height=7):
        self.width = width
        self.height = height

        self.__player_1__ = player_1
        self.__player_2__ = player_2

        self.__queen_1__ = player_1.__class__.__name__ + " - Q1"
        self.__queen_2__ = player_2.__class__.__name__ + " - Q2"


        self.__board_state__ = [
            [Board.BLANK for i in range(0, width)] for j in range(0, height)]

        self.__last_queen_move__ = {
            self.__queen_1__: Board.NOT_MOVED, self.__queen_2__: Board.NOT_MOVED}

        self.__queen_symbols__ = {
            Board.BLANK: Board.BLANK, self.__queen_1__: "Q1", self.__queen_2__: "Q2"}

        self.__active_player__ = player_1
        self.__inactive_player__ = player_2
        self.__active_players_queen__ = self.__queen_1__
        self.__inactive_players_queen__ = self.__queen_2__

        self.move_count = 0


    def get_state(self):
        return deepcopy(self.__board_state__)

    # Returns True, playername if playername just won
    # Returns False, None if game should continue
    def __apply_move__(self, queen_move):
        row, col, push = queen_move
        my_pos = self.__last_queen_move__[self.__active_players_queen__]
        opponent_pos = self.__last_queen_move__[self.__inactive_players_queen__]

        queen_name = self.__queen_symbols__[self.__active_players_queen__]

        # IF pushing
        if push:
            new_enemy_x, new_enemy_y = calculate_enemy_push_location(my_pos[0], my_pos[1], opponent_pos[0], opponent_pos[1])

            opponent_new_pos = (new_enemy_x, new_enemy_y, False)

            # If opponent was pushed off the board
            if not self.move_is_in_board(opponent_new_pos[0], opponent_new_pos[1]):
                return True, self.__active_players_queen__
            self.__last_queen_move__[self.__inactive_players_queen__] = opponent_new_pos
            self.__board_state__[opponent_new_pos[0]][opponent_new_pos[1]] = \
                self.__queen_symbols__[self.__inactive_players_queen__]

        # apply move of active player
        self.__last_queen_move__[self.__active_players_queen__] = queen_move
        self.__board_state__[row][col] = self.__queen_symbols__[self.__active_players_queen__]

        if self.move_is_in_board(my_pos[0], my_pos[1]):
            self.__board_state__[my_pos[0]][my_pos[1]] = Board.BLOCKED

        # swap the players
        self.__active_player__, self.__inactive_player__ = self.__inactive_player__, self.__active_player__

        # swaping the queens
        self.__active_players_queen__, self.__inactive_players_queen__ = self.__inactive_players_queen__,  self.__active_players_queen__

        # increment move count
        self.move_count = self.move_count + 1

        return False, None

    def copy(self):
        b = Board(self.__player_1__, self.__player_2__,
                  width=self.width, height=self.height)
        for key, value in self.__last_queen_move__.items():
            b.__last_queen_move__[key] = value
        for key, value in self.__queen_symbols__.items():
            b.__queen_symbols__[key] = value
        b.move_count = self.move_count
        b.__active_player__ = self.__active_player__
        b.__inactive_player__ = self.__inactive_player__
        b.__active_players_queen__ = self.__active_players_queen__
        b.__inactive_players_queen__ = self.__inactive_players_queen__
        b.__board_state__ = self.get_state()
        return b

    def forecast_move(self, queen_move):
        new_board = self.copy()
        is_over, winner = new_board.__apply_move__(queen_move)
        return new_board, is_over, winner

    def get_active_player(self):
        return self.__active_player__

    def get_inactive_player(self):
        return self.__inactive_player__

    def get_active_players_queen(self):
        return self.__active_players_queen__

    def get_inactive_players_queen(self):
        return self.__inactive_players_queen__

    def get_opponent_moves(self):
        q_move = self.__last_queen_move__[
            self.__inactive_players_queen__]
        
        return self.__get_moves__(q_move)

    def get_legal_moves(self):
        # List of legal moves. Each move: (row, current_col, is_push)
        q_move = self.__last_queen_move__[
            self.__active_players_queen__]
        
        return self.__get_moves__(q_move)


    def __get_moves__(self, move):

        if move == self.NOT_MOVED:
            return self.get_first_moves()

        r, c, _ = move

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0,  1),
                      (1, -1), (1,  0), (1,  1)]

        moves = []

        for direction in directions:
            for mag in range(1, max(self.height, self.width)):
                row = direction[0] * mag + r
                col = direction[1] * mag + c
                if self.move_is_in_board(row, col):
                    if self.is_spot_open(row, col):
                        moves.append((row, col, False))
                    elif self.is_spot_queen(row, col) and self.does_move_allow_push(row, col, direction):
                        moves.append((row, col, True))
                        break
                    else:
                        break
                else:
                    break

        return moves

    def get_first_moves(self):
        return [(i, j, False) for i in range(0, self.height) for j in range(0, self.width) if self.__board_state__[i][j] == Board.BLANK]

    def move_is_in_board(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def is_spot_open(self, row, col):
        return self.__board_state__[row][col] == Board.BLANK
    def is_spot_queen(self, row, col):
        q1 = self.__queen_symbols__[self.__active_players_queen__]
        q2 = self.__queen_symbols__[self.__inactive_players_queen__]  
        return self.__board_state__[row][col] == q1 or self.__board_state__[row][col] == q2

    def does_move_allow_push(self, row, col, direction):

        if not self.is_spot_queen(row,col):
            return False

        # Where the opponent's queen will be if it can be pushed
        row_next = row + direction[0]
        col_next = col + direction[1]

        if not self.move_is_in_board(row_next, col_next) or self.is_spot_open(row_next, col_next):
            # and IF the square they'd be pushed TO is either off the board or an open space on the board
            return True

        return False

    def move_is_legal(self, row, col):
        return 0 <= row < self.height and \
            0 <= col < self.width and \
            self.__board_state__[row][col] == Board.BLANK

    def print_board(self, legal_moves=[]):

        p1_r, p1_c, push = self.__last_queen_move__[self.__queen_1__]
        p2_r, p2_c, push = self.__last_queen_move__[self.__queen_2__]
        b = self.__board_state__

        out = '  |'
        for i in range(len(b[0])):
            out += str(i)+' |'
        out += '\n\r'

        for i in range(len(b)):
            out += str(i)+' |'
            for j in range(len(b[i])):
                if (i, j) == (p1_r, p1_c):
                    out += self.__queen_symbols__[self.__queen_1__]
                elif (i, j) == (p2_r, p2_c):
                    out += self.__queen_symbols__[self.__queen_2__]
                elif (i, j, True) in legal_moves or (i, j, False) in legal_moves:
                    out += 'o '
                elif b[i][j] == Board.BLANK:
                    out += '  '
                else:
                    out += '><'

                out += '|'
            if i != len(b)-1:
                out += '\n\r'

        return out

    def play_isolation(self, time_limit=10000, print_moves=False):
        move_history = []

        if platform.system() == 'Windows':
            def curr_time_millis():
                return int(round(time.time() * 1000))
        else:
            def curr_time_millis():
                return 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_utime

        while True:

            game_copy = self.copy()
            move_start = curr_time_millis()

            def time_left():
                #print("Limit: "+str(time_limit) +" - "+str(curr_time_millis()-move_start))
                return time_limit - (curr_time_millis() - move_start)

            if print_moves:
                print "\n",self.__active_players_queen__, " Turn"

            #try:
            legal_player_moves = self.get_legal_moves()
            curr_move = self.__active_player__.move(
                game_copy, legal_player_moves, time_left)  # queen added in return
            #except AttributeError as e:
            #    raise e
            #except Exception as e:
            #    print e
            #    pass

            if curr_move is None:
                return self.__inactive_players_queen__, move_history, \
                       (self.__active_players_queen__ +" has no legal moves left.")

            # Append new move to game history
            if self.__active_player__ == self.__player_1__:
                move_history.append([curr_move])
            else:
                move_history[-1].append(curr_move)

            # Handle Timeout
            if time_limit and time_left() <= 0:
                return self.__inactive_players_queen__, move_history, \
                       (self.__active_players_queen__ +" timed out.")

            # Safety Check
            legal_moves = self.get_legal_moves()
            if curr_move not in legal_moves:
                return self.__inactive_players_queen__, move_history, \
                       (self.__active_players_queen__ +" made an illegal move.")


            # Apply move to game.
            is_over, winner = self.__apply_move__(curr_move)

            if print_moves:
                print "move chosen: ", curr_move
                print self.copy().print_board()

            if is_over:
                return self.__active_players_queen__, move_history, \
                       (self.__inactive_players_queen__ + " was forced off the grid.")

    def __apply_move_write__(self, move_queen):
        if move_queen[0] is None or move_queen[1] is None:
            return

        row, col, push = move_queen
        self.__last_queen_move__[self.__active_players_queen__] = move_queen
        self.__board_state__[row][col] = \
            self.__queen_symbols__[self.__active_players_queen__]

        # swap the players
        tmp = self.__active_player__
        self.__active_player__ = self.__inactive_player__
        self.__inactive_player__ = tmp

        # swaping the queens
        tmp = self.__active_players_queen__
        self.__active_players_queen__ = self.__inactive_players_queen__
        self.__inactive_players_queen__ = tmp

        self.move_count = self.move_count + 1


def game_as_text(winner, move_history,  termination="", board=Board(1, 2)):
    ans = StringIO.StringIO()

    board = Board(board.__player_1__, board.__player_2__, board.width, board.height)

    print "Printing the game as text."

    last_move = (9,9,False)
    
    for i, move in enumerate(move_history):
        if move is None or len(move) == 0:
            continue

        if move[0] != Board.NOT_MOVED and move[0] is not None:
            ans.write(board.print_board())
            board.__apply_move_write__(move[0])
            ans.write("\n\n" + board.__queen_1__ + " moves to (" + str(move[0][0]) + "," + str(move[0][1]) + ")\r\n")

            if len(move) > 1 and move[0][2] is True:
                my_x, my_y = last_move[0][0], last_move[0][1]
                enemy_x, enemy_y = move[0][0], move[0][1]

                new_enemy_x, new_enemy_y = calculate_enemy_push_location(my_x, my_y, enemy_x, enemy_y)

                if board.move_is_in_board(new_enemy_x, new_enemy_y):
                    board.__apply_move_write__((new_enemy_x, new_enemy_y, False))
                ans.write("\n\n" + board.__queen_2__ + " pushed to (" + str(new_enemy_x) + "," + str(new_enemy_y) + ")\r\n")
                board.__active_players_queen__, board.__inactive_players_queen__ = board.__inactive_players_queen__, board.__active_players_queen__


        if len(move) > 1 and move[1] != Board.NOT_MOVED and move[0] is not None:
            ans.write(board.print_board())
            board.__apply_move_write__(move[1])
            ans.write("\n\n" + board.__queen_2__ + " moves to (" + str(move[1][0]) + "," + str(move[1][1]) + ")\r\n")

            if move[1] is not None and move[1][2] is True:
                my_x, my_y = last_move[1][0], last_move[1][1]
                enemy_x, enemy_y = move[1][0], move[1][1]

                new_enemy_x, new_enemy_y = calculate_enemy_push_location(my_x, my_y, enemy_x, enemy_y)

                if board.move_is_in_board(new_enemy_x, new_enemy_y):
                    board.__apply_move_write__((new_enemy_x, new_enemy_y, False))
                ans.write("\n\n" + board.__queen_1__ + " pushed to (" + str(new_enemy_x) + "," + str(new_enemy_y) + ")\r\n")
                board.__active_players_queen__, board.__inactive_players_queen__ = board.__inactive_players_queen__, board.__active_players_queen__

        last_move = move

    ans.write("\n"+str(winner)+" has won. Reason: "+ str(termination))
    return ans.getvalue()

def calculate_enemy_push_location(my_x, my_y, enemy_x, enemy_y):
    push_direction_x = enemy_x - my_x
    if push_direction_x != 0:
        push_direction_x /= abs(push_direction_x)
    push_direction_y = enemy_y - my_y
    if push_direction_y != 0:
        push_direction_y /= abs(push_direction_y)
    return enemy_x + push_direction_x, enemy_y + push_direction_y
