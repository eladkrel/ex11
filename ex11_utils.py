from typing import List, Tuple, Iterable, Optional, Set

import boggle_board_randomizer

Board = List[List[str]]
Path = List[Tuple[int, int]]
Coordinate = Tuple[int, int]


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
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
    curr_row, curr_col = curr_coordinate
    rows = len(board)
    cols = len(board[0])
    return 0 <= curr_row < rows and 0 <= curr_col < cols


def is_valid_distance(curr_coordinate: Coordinate, next_coordinate: Coordinate) -> bool:
    curr_y, curr_x = curr_coordinate
    next_y, next_x = next_coordinate
    if abs(curr_y - next_y) > 1 or abs(curr_x - next_x) > 1:
        return False
    return True


# def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
#     # Inner function for depth-first search (DFS) traversal
#     def dfs(i: int, j: int, path: Path, visited: List[List[bool]], word: str, result: List[Path]):
#         # Base case: out-of-bounds or already visited cell
#         if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]) or visited[i][j] or len(word) == n+1:
#             return
#
#         # Append current coordinate to the path
#         path.append((i, j))
#         visited[i][j] = True
#
#         # Check if the path forms a word of length n from the words list
#         if len(word) == n and word in words and path not in result:
#             result.append(path[:])  # Append a copy of the path to the result list
#
#         # Explore neighboring cells using DFS
#         for di in [-1, 0, 1]:
#             for dj in [-1, 0, 1]:
#                 ni, nj = i + di, j + dj
#                 if ni >= 0 and ni < len(board) and nj >= 0 and nj < len(board[0]):
#                     next_word = word + board[ni][nj]
#                     dfs(ni, nj, path, visited, next_word, result)
#
#         # Backtrack: mark current cell as unvisited and remove it from the path
#         visited[i][j] = False
#         path.pop()
#
#     # Initialize result list, visited matrix, and perform DFS for each cell in the game board
#     result = []
#     visited = [[False] * len(board[0]) for _ in range(len(board))]
#
#     for i in range(len(board)):
#         for j in range(len(board[0])):
#             word = board[i][j]  # Start a new word from each cell
#             dfs(i, j, [], visited, word, result)
#
#     return [[tuple(coord) for coord in path] for path in result]


def backtrack(row, col, path, visited, board, valid_words, result, n,
              curr_word):
    rows = len(board)
    cols = len(board[0])

    # Append the current letter to the path
    curr_word += board[row][col]
    path.append((row, col))

    # Mark the current position as visited
    visited[row][col] = True
    valid_words = relevant_words(valid_words, curr_word, n)
    if len(valid_words) == 0:
        return
    # Check if the path forms a valid word of length n
    if len(path) == n and curr_word in valid_words:
        result.append(path[:])
        return


    # Explore all possible directions
    for dx, dy in DIRECTIONS:
        new_row = row + dy
        new_col = col + dx

        # Check if the new position is within the board boundaries and not visited
        if is_in_board(board, (new_row, new_col)) and not visited[new_row][new_col]:
            path_copy = path[:]
            visited_copy = [row[:] for row in visited]
            backtrack(new_row, new_col, path_copy, visited_copy,
                      board, valid_words, result, n, curr_word)

    #path.pop()
    visited[row][col] = False


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    rows = len(board)
    if rows == 0:
        return []

    cols = len(board[0])
    if cols == 0:
        return []

    # Create a set of valid words for efficient lookup
    valid_words = get_word_letters_in_board(board, words)

    # Initialize the result list to store all found words
    result = []

    # Iterate through each cell of the board and perform backtracking
    for i in range(rows):
        for j in range(cols):
            # Initialize a visited matrix for each starting cell
            visited = [[False] * cols for _ in range(rows)]
            backtrack(i, j, [], visited, board, valid_words, result, n, "")

    return result


def get_word_letters_in_board(board: Board, words: List[str]):
    valid_words = set()
    board_letters = get_letters_in_board(board)
    # for word in words:
    #     if set(word).issubset(board_letters):
    #         valid_words.add(word)

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
    board_letters = set()
    for row_i in range(len(board)):
        for col_i in range(len(board[0])):
            board_letters.update(set(board[row_i][col_i]))
    return board_letters

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass


def relevant_words(words: Iterable[str], partial_word: str, n: int) -> set:
    """
    Function filter the given words according
    to a given partial word and an int.
    """
    relevant = set()
    length = len(partial_word)

    for word in words:
        if len(word) == n and partial_word == word[:length]:
            relevant.add(word)
    return relevant
