from typing import List, Tuple, Iterable, Optional, Set
from copy import deepcopy

Board = List[List[str]]
Path = List[Tuple[int, int]]
Coordinate = Tuple[int, int]
VisitedBoard = List[List[bool]]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1),
              (1, 1)]


def is_valid_path(board: Board, path: Path, words: Iterable[str]) \
        -> Optional[str]:
    """
    Function receives a board, a path on the board and an iterable of words
    and checks if the given path is valid a and creates a word that is in
    the words iterable.
    :param board: A game board
    :param path: A path of coordinates
    :param words: An iterable of words
    :return: The word created by the path if the path is valid and word is
    in the words iterable, None otherwise.
    """
    if len(path) == 0:
        return None
    word = ""
    for i in range(len(path)):
        curr_coordinate = path[i]
        if not is_in_board(board, curr_coordinate):
            return None
        if i < len(path) - 1:
            next_coordinate = path[i + 1]
            if not is_valid_distance(curr_coordinate, next_coordinate):
                return None
        word += board[curr_coordinate[0]][curr_coordinate[1]]
    if word in words:
        return word


def is_in_board(board: Board, curr_coordinate: Coordinate) -> bool:
    """
    Function checks if coordinates are within the board
    :param board: the game board
    :param curr_coordinate: coordinates to check
    :return: True if within the board, False otherwise
    """
    curr_row, curr_col = curr_coordinate
    rows = len(board)
    cols = len(board[0])
    if 0 <= curr_row < rows and 0 <= curr_col < cols:
        return True
    return False


def is_valid_distance(curr_coordinate: Coordinate, next_coordinate:
                      Coordinate) -> bool:
    """
    Function checks if the distance between two coordinates is valid.
    :param curr_coordinate: A coordinate
    :param next_coordinate: A coordinate
    :return: True if valid distance, False otherwise.
    """
    curr_y, curr_x = curr_coordinate
    next_y, next_x = next_coordinate
    if abs(curr_y - next_y) > 1 or abs(curr_x - next_x) > 1:
        return False
    return True


def backtrack_path_finder(row: int, col: int, path: List[Coordinate],
                          visited: VisitedBoard, board: Board,
                          valid_words: Iterable[str], result: List[Path],
                          n: int, curr_word: str, length_type) -> None:
    """
    Function helps find all the appropriate paths using backtracking.
    :param row: The index of the row
    :param col: The index of the column
    :param path: The current path to explore
    :param visited: A board of all the visited places, so they aren't explored
    :param board: A game board
    :param valid_words: An iterable of all the words that are possible
    :param result: A list of coordinates of the possible paths
    :param n: The variable n that controls the length of the path or word
    :param curr_word: The current word being built
    :param length_type: If n represents the length of path or length of word
    :return: Function does not return, updates results argument in place.
    """
    # Append the current letter to the current word and coordinate to path list
    curr_word += board[row][col]
    curr_path = path + [(row, col)]

    visited[row][col] = True    # Mark the current position as visited
    valid_words = get_relevant_words(valid_words, curr_word, n)
    if len(valid_words) == 0:
        return

    # Check if length of path or word is valid and the word is in valid_words
    if length_type == "path":
        if len(curr_path) == n and curr_word in valid_words:
            result.append(deepcopy(curr_path))
            return
    if length_type == "word":
        if len(curr_word) == n and curr_word in valid_words:
            result.append(deepcopy(curr_path))
            return

    # Move through all directions
    for dy, dx in DIRECTIONS:
        new_row, new_col = row + dy, col + dx

        # Check if the new coord is within the board boundaries and not visited
        if is_in_board(board, (new_row, new_col)) \
                and not visited[new_row][new_col]:
            backtrack_path_finder(new_row, new_col, curr_path[:],
                                  deepcopy(visited), board, valid_words,
                                  result, n, curr_word, length_type)


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) \
        -> List[Path]:
    """
    Function receives a board, a length n and an iterable of words and
    returns a list of paths that build words in the words iterable of path
    length n.
    :param n: A length int
    :param board: A game board
    :param words: An iterable of words
    :return: A list of paths of all the valid words of path length n
    """
    rows = len(board)
    cols = len(board[0])
    if rows == 0 or cols == 0:
        return []

    # Remove words that their letters are not on the board
    valid_words = get_word_letters_in_board(board, words)
    result = []

    # Iterate through each cell of the board and perform backtracking
    for i in range(rows):
        for j in range(cols):
            visited = [[False] * cols for _ in range(rows)]
            backtrack_path_finder(i, j, [], visited, board, valid_words,
                                  result, n, "", "path")

    return result


def get_word_letters_in_board(board: Board, words: Iterable[str]) -> \
        Set[str]:
    """
    Function receives an iterable of words and returns a set of all the
    words that their letters appear on the board.
    :param board: A game board
    :param words: An iterable of words
    :return: A new set of words that all their letters appear on the board
    """
    valid_words = set()
    board_letters = get_letters_in_board(board)

    for word in words:
        is_valid_word = True
        word_letters = set(word)
        for letter in word_letters:
            if letter not in board_letters:
                is_valid_word = False
                break
        if is_valid_word:
            valid_words.add(word)
    return valid_words


def get_letters_in_board(board: Board) -> Set[str]:
    """
    Function receives a board and returns a set of all the letters on the
    board.
    :param board: A game board
    :return: A set of all the letters on the board.
    """
    board_letters = set()
    for row_i in range(len(board)):
        for col_i in range(len(board[0])):
            board_letters.update(set(board[row_i][col_i]))
    return board_letters


def find_length_n_words(n: int, board: Board, words: Iterable[str])\
        -> List[Path]:
    """
        Function receives a board, a length n and an iterable of words and
        returns a list of paths that build words in the words iterable of
        length n.
        :param n: A length int
        :param board: A game board
        :param words: An iterable of words
        :return: A list of paths of all the valid words of length n
        """
    rows = len(board)
    cols = len(board[0])

    if rows == 0 or cols == 0:
        return []

    # Remove words that their letters are not on the board
    valid_words = get_word_letters_in_board(board, words)
    result = []

    # Iterate through each cell of the board and perform backtracking
    for i in range(rows):
        for j in range(cols):
            # Initialize a visited matrix for each starting cell
            visited = [[False] * cols for _ in range(rows)]
            backtrack_path_finder(i, j, [], visited, board, valid_words,
                                  result, n, "", "word")

    return result


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Function receives a board and an iterable of words and returns a list
    paths the yield the highest score for the board.
    :param board: A game board
    :param words: An iterable of words
    :return: A list of paths that yield the highest score
    """
    max_path_length = len(board) * len(board[0])
    result = dict()
    visited_words = dict()
    good_words = get_word_letters_in_board(board, words)

    for n in range(max_path_length):
        curr_valid_words = set([word for word in good_words if len(word) >= n])
        if len(curr_valid_words) == 0:
            break
        n_paths_results = find_length_n_paths(n, board, curr_valid_words)
        for path in n_paths_results:
            curr_word = build_word(path, board)
            curr_score = len(path) ** 2
            if curr_word in visited_words.keys():
                if curr_score > visited_words[curr_word]:
                    visited_words[curr_word] = curr_score
                    result[curr_word] = path
            else:
                visited_words[curr_word] = curr_score
                result[curr_word] = path
    return list(result.values())


def get_relevant_words(words: Iterable[str], curr_word: str, n: int) \
        -> Set[str]:
    """
    Function receives a words iterable, the start of a word and a length n
    and returns all the words that are currently optional and relevant given
    the current word.
    :param words: An iterable of words
    :param curr_word: the current word to see if it is the start of a word
    in the words iterable
    :param n: The length of the word
    :return: A reduced set of all the words that are currently relevant.
    """
    relevant_words_set = set()
    curr_length = len(curr_word)

    for word in words:
        # len(word) >= n because length of word can be longer than length of
        # path. Deals with instance of 'QU'
        if len(word) >= n and curr_word == word[:curr_length]:
            relevant_words_set.add(word)
    return relevant_words_set


def build_word(path: Path, board: Board) -> str:
    """
    Function receives a path and a board and returns the built word from the
    given path.
    :param path: A list of coordinates
    :param board: A game Board
    :return: str of the built word from the path on the board
    """
    word = ""
    for coordinate in path:
        row, col = coordinate
        word += board[row][col]
    return word
