import keyboard
import time
import sys


class TicTacToe:
    def __init__(self):
        self.__moves_table = [[None] * 3, [None] * 3, [None] * 3]
        self.__keys_table = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.__players = 'XO'
        self.__player = None
        self.__player_won = False
        self.__place_array = lambda x: int(x) - 1
        self.__message = ''
        self.__set_player()
        self.write_board()

    def __set_player(self):
        self.__player = self.__players[0] if self.__player == None else \
            self.__players[1] if self.__player == self.__players[0] else self.__players[0]

    def write_board(self):
        print(f'__moves_table:{self.__moves_table}, __keys_table:{self.__keys_table}')
        for row_number in range(0, len(self.__moves_table)):
            row = ''
            for col_number in range(0, len(self.__moves_table[row_number])):
                row += f'{self.__moves_table[row_number][col_number]}│' \
                    if self.__moves_table[row_number][col_number] is not None \
                    else f'{self.__keys_table[row_number][col_number]}│'
            print(f"{row[:-1]}")
            if row_number != len(self.__moves_table) - 1:
                print(f"{''.join(['─┼' * 3])[:-1]}")
        print(f'Turn:{self.__player}\n{self.__message}')

    def put_marker(self, _place, _row):
        if self.__moves_table[_row][_place] == None:
            self.__moves_table[_row][_place] = self.__player
            player_won = self.__check_if_player_win()
            if player_won is True:
                self.__message = f'Player {self.__player} won !!!'
                self.__player_won = True
            else:
                self.__set_player()
        else:
            self.__message = 'Wrong turn!'

    def __check_if_player_win(self):
        p = self.__player
        mt = self.__moves_table
        return any([all(i == p for i in [mt[0][0], mt[0][1], mt[0][2]]),
                    all(i == p for i in [mt[1][0], mt[1][1], mt[1][2]]),
                    all(i == p for i in [mt[2][0], mt[2][1], mt[2][2]]),
                    all(i == p for i in [mt[0][0], mt[1][0], mt[2][0]]),
                    all(i == p for i in [mt[0][1], mt[1][1], mt[2][1]]),
                    all(i == p for i in [mt[0][2], mt[1][2], mt[2][2]]),
                    all(i == p for i in [mt[0][0], mt[1][1], mt[2][2]]),
                    all(i == p for i in [mt[0][2], mt[1][1], mt[2][0]]),
                    ])

    def refresh_board(self, place):
        self.__message = ''
        back_up_line = '\033[F'
        match place:
            case place if place in '123':
                self.put_marker(self.__place_array(place), 0)
            case place if place in '456':
                self.put_marker(self.__place_array(place) - 3, 1)
            case place if place in '789':
                self.put_marker(self.__place_array(place) - 6, 2)
        for i in range(1 + 5 + 2):
            sys.stdout.write(back_up_line)
            for x in range(75):
                print('*' * (75 - x), x, end='\x1b[1K\r')

        self.write_board()
        return self.__player_won


if __name__ == '__main__':
    game = TicTacToe()
    play_game = True
    while play_game:
        key = keyboard.read_event()
        if key.event_type == 'down':
            match key.name:
                case 'q':
                    break
                case key.name if key.name in '123456789':
                    play_game = True if game.refresh_board(key.name) == False else False
        time.sleep(.2)
    print('End game.')
