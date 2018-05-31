from random import randint


class Board(object):
    def __init__(self, size):
        assert isinstance(size, int)
        self.size = size
        self.positions = [["-"] * self.size for i in range(self.size)]

    def __repr__(self):
        board_string = '\n'.join(['|'.join(self.positions[i]) for i in range(self.size)])
        return 'I am board of size %i \n' % self.size + board_string

    def __getitem__(self, positions):
        return self.positions[positions[0]][positions[1]]

    def clear(self):
        self.positions = [["    -"] * self.size for i in range(self.size)]

    def insert(self, symbol_type, positions):
        assert (symbol_type == 'X' or symbol_type == 'Y')
        self.positions[positions[0]][positions[1]] = symbol_type

    def check_victory_conditions(self):
        rows = list(map(lambda x: ''.join(x), self.positions))
        columns = list(map(lambda x: ''.join(x), zip(*self.positions)))
        antydiag = list(map(lambda x: ''.join(x), [[self.positions[i][j]
                                                    for i in range(self.size)
                                                    for j in range(self.size)
                                                    if i + j == k]
                                                   for k in range(2 * self.size - 1)]))
        diag = list(map(lambda x: ''.join(x), [[self.positions[i][j]
                                                for i in range(self.size)
                                                for j in range(self.size)
                                                if -i + j == k]
                                               for k in range(-self.size + 1, self.size)]))

        return 'X' * self.size in rows or 'Y' * self.size in rows \
               or 'X' * self.size in columns or 'Y' * self.size in columns \
               or 'X' * self.size in diag or 'Y' * self.size in diag \
               or 'X' * self.size in antydiag or 'Y' * self.size in antydiag


class NoughtsAndCorsses(object):

    def __init__(self, size):
        self.board = Board(size)

    def _play_turn(self, player_mark):
        assert player_mark in 'XY'
        fieldpos_x = randint(0, self.board.size - 1)
        fieldpos_y = randint(0, self.board.size - 1)
        while (self.board[fieldpos_x, fieldpos_y] != '-'):
            fieldpos_x = randint(0, self.board.size - 1)
            fieldpos_y = randint(0, self.board.size - 1)

        return (fieldpos_x, fieldpos_y)

    def play_bot_game(self):
        turn = 0
        end = False
        while not end and turn < self.board.size ** 2:
            turn += 1
            mark = 'X' if turn % 2 == 0 else 'Y'
            self.board.insert(mark, self._play_turn(mark))
            print(self.board)
            end = self.board.check_victory_conditions()

        outcome = 'Winner is player %s' % mark if (turn < self.board.size ** 2) \
            else "The game ended with draw"
        print(outcome)


game = NoughtsAndCorsses(5)
game.play_bot_game()
