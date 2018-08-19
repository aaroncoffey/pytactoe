"""Python curses implementation of TicTacToe.

This isn't complete or an example of my best work. But, it works,
and I challenged myself to put _something_ up publicly, so here we are.
Written in late 2017.
"""

import curses
import time
import random

# TODO: AI should remember "dangerous" moves.
#       Track board state right before loseing, check to avoid that state again next round.
# TODO: Set startup modes. AI vs AI mode. Curses / Non-curses. Human vs Human.
#       Set AI intelligence, strategic, intiutive, dumb.

__author__ = 'Aaron Coffey (aaron@coffey.works)'
__version__ = '0.0.1'


class Board():
    def __init__(self):
        """
        g h i
        d e f
        a b c
        """
        self.a = [0, 0, ' ']
        self.b = [1, 0, ' ']
        self.c = [2, 0, ' ']
        self.d = [0, 1, ' ']
        self.e = [1, 1, ' ']
        self.f = [2, 1, ' ']
        self.g = [0, 2, ' ']
        self.h = [1, 2, ' ']
        self.i = [2, 2, ' ']
        self.winning_combinations = [
            [self.a, self.b, self.c],
            [self.d, self.e, self.f],
            [self.g, self.h, self.i],
            [self.a, self.d, self.g],
            [self.b, self.e, self.h],
            [self.c, self.f, self.i],
            [self.g, self.e, self.c],
            [self.a, self.e, self.i]
        ]
        self.corners = [self.a, self.c, self.g, self.i]
        self.possible_pieces = ['x', 'o']
        self.winner = None
        self.last_turn = 'x'
        self.gametick = 0
        self.banner = 'Welcome to pyTacToe'
        self.game_num = 0
        self.mode = ''
        self.curses_y_start = 4
        self.curses_y_positions = [
            self.curses_y_start + 4, self.curses_y_start + 2, self.curses_y_start
        ]
        self.curses_x_positions = [(0, 1, 2), (4, 5, 6), (8, 9, 10)]
        self.message = ''
        self.using_curses = False
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.gameover = False

    def __iter__(self):
        for attr, value in [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i]:
            yield attr, value

    def move(self, x, y, piece):
        """
        Returns:
            0, Try again.
            1, Success.
            2, Failure, don't try again.
        """
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            self.render_board()
            return 0

        if x > 2 or x < 0 or y > 2 or y < 0:
            self.render_board()
            return 0

        if piece not in self.possible_pieces:
            self.render_board()
            return 0

        if self.winner:
            self.render_board()
            return 2

        else:
            for attr, value in list(self.__dict__.items()):
                try:
                    if value[0] == x and value[1] == y:
                        self.place_piece(attr, piece)
                        return 1
                except IndexError:
                    print('Python 3.6 or higher required.')
                    raise

    def place_piece(self, key, piece):
        spot = getattr(self, key)

        if spot[2] == ' ':
            spot[2] = piece
            self.last_turn = piece
            self.gametick += 1
            self.check_for_winner()
            self.render_board()
            return True

        self.render_board()
        return False

    def check_for_winner(self):
        if self.gameover:
            if self.winner:
                self.message = '{0} is the winner!'.format(self.winner)

            else:
                self.message = 'DEADLOCK!'

            self.render_board()
            return True

        for win_combo in self.winning_combinations:
            for piece in self.possible_pieces:
                count = 0
                for place in win_combo:
                    if place[2] == piece:
                        count += 1

                if count >= 3:
                    self.winner = piece
                    self.message = '{0} is the winner!'.format(piece)
                    self.gameover = True
                    if self.winner == 'x':
                        self.x_wins += 1
                    else:
                        self.o_wins += 1

                    self.render_board()
                    if self.using_curses:
                        # Pause for dramatic effect.
                        self.using_curses.getch()
                    else:
                        input('Enter to continue.')
                    return True

        if self.gametick > 8:
            self.message = 'DEADLOCK!'
            self.draws += 1
            self.gameover = True
            self.render_board()
            if self.using_curses:
                # Pause for dramatic effect.
                self.using_curses.getch()
            else:
                input('Enter to continue.')
            return True

        return False

    def render_board(self):
        stdscr = self.using_curses
        board_str = ' {g} | {h} | {i} \n---|---|---\n {d} | {e} | {f} \n---|---|---\n {a} | {b} | {c} '.format(
            a=self.a[2],
            b=self.b[2],
            c=self.c[2],
            d=self.d[2],
            e=self.e[2],
            f=self.f[2],
            g=self.g[2],
            h=self.h[2],
            i=self.i[2],
        )
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, self.banner)
            stdscr.addstr(1, 0, 'Game: {0} Mode: {1}'.format(
                str(self.game_num).zfill(5),
                self.mode
            ))
            stdscr.addstr(2, 0, self.message)
            stdscr.addstr(self.curses_y_start, 0, board_str)
            stdscr.addstr(self.curses_y_start + 6, 0,
                          'X Wins: {0}'.format(self.x_wins))
            stdscr.addstr(self.curses_y_start + 7, 0,
                          'O Wins: {0}'.format(self.o_wins))
            stdscr.addstr(self.curses_y_start + 8, 0,
                          'Draws:  {0}'.format(self.draws))
            stdscr.refresh()
        else:
            print(self.banner)
            print('Game: {0} Mode: {1}'.format(
                str(self.game_num).zfill(5), self.mode))
            print(self.message)
            print()
            print(board_str)

    def dumb_ai_move(self, piece='o'):
        self.message = 'AI "thinking"...'
        self.render_board()
        time.sleep(.3)
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            resp = self.move(x, y, piece)
            if resp == 2:
                return False
            elif resp == 1:
                return True

    def move_suggestion(self, piece, return_decent=True):
        # take a random winning combination.
        for win_combo in random.sample(self.winning_combinations, len(self.winning_combinations)):
            # Count how many pieces occupy this combo.
            pieces = len([item for item in win_combo if item[2] == piece])
            # Count how many of the opponents pieces occupy the same.
            opponents = len([item for item in win_combo if item[2]
                             == ('x' if piece == 'o' else 'o')])
            # Take a winning move.
            if pieces == 2 and opponents == 0:
                winner = [item for item in win_combo if item[2] == ' '][0]
                return [winner[0], winner[1]]
            # Block an opponents winning move.
            elif pieces == 0 and opponents == 2:
                stealer = [item for item in win_combo if item[2] == ' '][0]
                return [stealer[0], stealer[1]]
            # Return an intuitive but not strategic option.
            elif pieces == 1 and opponents == 0 and return_decent:
                decent = [item for item in win_combo if item[2]
                          == ' '][random.randint(0, 1)]
                return [decent[0], decent[1]]

        return None

    def random_move_suggestion(self, piece):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            for _, value in list(self.__dict__.items()):
                if value[0] == x and value[1] == y:
                    if value[2] == ' ':
                        return [x, y]
                    else:
                        break

    def strategic_ai_move(self, piece='o'):
        pause_speed = .2
        self.message = 'AI looks deep into your soul.'
        self.render_board()
        time.sleep(pause_speed)

        # If a winning move exists, take it.
        # If player about to win, steal the move.
        self.message = 'AI - Calculating move.'
        self.render_board()
        time.sleep(pause_speed)
        next_move = self.move_suggestion(piece, False)
        if next_move:
            self.move(next_move[0], next_move[1], piece)
            return True

        # Take an edge, starting with corners.

    def intuitive_ai_move(self, piece='o'):
        pause_speed = .2
        self.message = 'AI carefully considering options...'
        self.render_board()
        time.sleep(pause_speed)

        # If a winning move exists, take it.
        # If player about to win, steal the move.
        # If that fails, take a move that steps non-strategically in the right direction.
        self.message = 'AI - Checking for winning move.'
        self.render_board()
        time.sleep(pause_speed)
        next_move = self.move_suggestion(piece)
        if next_move:
            self.move(next_move[0], next_move[1], piece)
            return True

        # If center available, take it.
        self.message = 'AI - Checking for center position.'
        self.render_board()
        time.sleep(pause_speed)
        if self.e[2] == ' ':
            self.move(1, 1, piece)
            return True

        # If all else has failed, select randomly.
        self.message = 'AI - Moving randomly.'
        self.render_board()
        time.sleep(pause_speed)
        random_move = self.random_move_suggestion(piece)
        if random_move:
            self.move(random_move[0], random_move[1], piece)
            return True

        self.message = 'Something has gone very wrong!'
        self.render_board()
        time.sleep(10)
        quit(1)

    def player_move(self, piece='x'):
        self.message = "Puny human's turn!"
        self.render_board()
        while True:
            x = input('x coord? ')
            y = input('y coord? ')
            resp = self.move(x, y, piece)
            if resp == 2:
                self.message = 'WRONG! You GET NOTHING!'
                self.render_board()
                return False
            if resp == 1:
                # successful placement
                return True

            self.message = 'Invalid, please try again.'
            self.render_board()

    def turn(self):
        if self.last_turn == 'x':
            return 'o'

        return 'x'

    def translate_curses_xy(self, cx, cy):
        tx = None
        ty = None
        try:
            ty = self.curses_y_positions.index(cy)
        except ValueError:
            return None

        for pos in self.curses_x_positions:
            try:
                if pos.index(cx):
                    tx = self.curses_x_positions.index(pos)
            except ValueError:
                pass

        if tx is not None and ty is not None:
            return (tx, ty)

        return None

    def clear(self):
        self.a[2] = ' '
        self.b[2] = ' '
        self.c[2] = ' '
        self.d[2] = ' '
        self.e[2] = ' '
        self.f[2] = ' '
        self.g[2] = ' '
        self.h[2] = ' '
        self.i[2] = ' '
        self.winner = None
        self.gametick = 0
        self.gameover = False
        self.render_board()


def main():
    bor = Board()
    bor.render_board()
    while True:
        if bor.check_for_winner():
            break
        else:
            if bor.turn() == 'o':
                bor.intuitive_ai_move('o')
            else:
                bor.player_move('x')


def main_curses(stdscr):
    player_piece = 'x'
    stdscr.clear()
    bor = Board()
    #bor.mode = 'DumbAI'
    bor.mode = 'Better AI'
    bor.using_curses = stdscr
    bor.render_board()
    while True:
        if bor.check_for_winner():
            bor.game_num += 1
            bor.clear()

        elif bor.turn() is not player_piece:
            #bor.dumb_ai_move('o' if player_piece is 'x' else 'x')
            bor.intuitive_ai_move('o' if player_piece is 'x' else 'x')

        else:
            bor.message = "Puny human's turn!"
            bor.render_board()
            event = stdscr.getch()
            if event == ord("q"):
                break
            if event == curses.KEY_MOUSE:
                # Curses errors when scrolled.
                try:
                    _, cx, cy, _, _ = curses.getmouse()
                except curses.error:
                    continue
                translated_coords = bor.translate_curses_xy(cx, cy)
                if translated_coords:
                    move_ret = bor.move(
                        translated_coords[0], translated_coords[1], player_piece)
                    if move_ret == 0:
                        bor.message = 'Invalid, please try again.'
                    if move_ret == 2:
                        bor.message = 'Something has gone very wrong.'
                    bor.render_board()


if __name__ == '__main__':
    # main()
    curses.initscr()
    curses.mousemask(1)
    curses.noecho()
    curses.wrapper(main_curses)
