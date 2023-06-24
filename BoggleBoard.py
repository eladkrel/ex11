from boggle_board_randomizer import randomize_board
import ex11_utils
from typing import List, Tuple, Iterable, Optional, Set
from copy import deepcopy

Board = List[List[str]]
Path = List[Tuple[int, int]]
Coordinate = Tuple[int, int]
VisitedBoard = List[List[bool]]


WORDS_PATH = "boggle_dict.txt"


class BoggleBoard:
    def __init__(self):
        """
        Initialize the Boggle Board
        """
        self.__board = randomize_board()
        self.__load_game_words()
        self.__max_score_paths = ex11_utils.max_score_paths(self.__board,
                                                            self.__words)
        self.__paths = set()
        self.__submitted_words = set()

    def __load_game_words(self):
        """
        Function loads all the game words from boggle_dict.txt
        """
        with open(WORDS_PATH, "rb") as f:
            self.__words = f.readlines()

    def get_next_possible_moves(self, row, col):
        """
        Function receives an index of a button on the board and changes that
        all the buttons next to it are gray and enabled and the other buttons
        are white and disabled.
        :param row: row index
        :param col: col index
        """
        next_possible_moves = set()

        for r in range(len(self.__board)):
            for c in range(len(self.__board[0])):
                if ex11_utils.is_in_board(self.__board, (r,c)) and \
                        ex11_utils.is_valid_distance((row, col), (r, c)):
                    next_possible_moves.add((r, c))
        return next_possible_moves

    def add_submitted_word(self, path: Path) -> bool:
        if not ex11_utils.is_valid_path():
            return False
        word = ex11_utils.build_word(path, self.__board)
        if word not in self.__submitted_words and word in self.__words:
            self.__submitted_words.add(word)
            self.__paths.add(path)
            return True
        return False

    def get_board_copy(self):
        return deepcopy(self.__board)





