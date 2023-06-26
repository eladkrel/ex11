from boggle_board_randomizer import randomize_board
import ex11_utils
from typing import List, Tuple, Set
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
        self.__paths = []
        self.__submitted_words = []
        self.__score = 0
        self.__current_path = []
        self.__hit_max_score = False

    def __load_game_words(self) -> None:
        """
        Function loads all the game words from boggle_dict.txt
        """

        # Open the file and read its contents
        with open(WORDS_PATH, "r") as file:
            content = file.read()

        # Split the contents into individual words and remove whitespace
        self.__words = [word for word in content.split()]

    def get_next_possible_moves(self, coordinate: Coordinate) \
            -> Set[Coordinate]:
        """
        Function receives a coordinate of a button on the board and changes
        that all the buttons next to it are gray and enabled and the other
        buttons are white and disabled.
        :param coordinate: The coordinate indexes
        """
        next_possible_moves = set()
        row, col = coordinate
        for r in range(len(self.__board)):
            for c in range(len(self.__board[0])):
                if ex11_utils.is_in_board(self.__board, (r, c)) and \
                        ex11_utils.is_valid_distance((row, col), (r, c)):
                    # if player can do this move
                    next_possible_moves.add((r, c))
        return next_possible_moves

    def add_submitted_word(self, ) -> bool:
        """
        Function adds a word that has been submitted and from the
        self.__current_path. Returns True if successful, False otherwise.
        :return: True if addition successful, False otherwise.
        """
        path = self.__current_path
        self.__current_path = []
        if not ex11_utils.is_valid_path(self.__board, path, self.__words):
            return False
        word = ex11_utils.build_word(path, self.__board)
        if word not in self.__submitted_words:
            self.__submitted_words.insert(0, word)
            self.__paths.append(path)
            self.__update_score()
            if set(self.__max_score_paths) == set(self.__paths):
                self.__hit_max_score = True
            return True
        return False

    def get_board_copy(self) -> Board:
        """Returns a copy of the game board"""
        return deepcopy(self.__board)

    def __update_score(self) -> None:
        """
        Function updates the game score.
        """
        score = 0
        for path in self.__paths:
            score += len(path) ** 2
        self.__score = score

    def get_score(self) -> int:
        """Returns the game score"""
        return self.__score

    def add_coordinate(self, coordinate: Coordinate) -> bool:
        """
        Function tries to add a coordinate as the next step. If successful
        returns True, False otherwise.
        :param coordinate: coordinates of the next step.
        :return: True if valid next coordinate, False otherwise.
        """
        if coordinate in self.get_next_possible_moves(coordinate):
            self.__current_path.append(coordinate)
            return True
        else:
            return False

    def get_submitted_words(self) -> List[str]:
        """Return the submitted words in the game"""
        return self.__submitted_words

    def is_max_score(self):
        """Function returns True if the game has reached the max score,
        False otherwise."""
        return self.__hit_max_score
