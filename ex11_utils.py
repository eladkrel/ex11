from typing import List, Tuple, Iterable, Optional

import boggle_board_randomizer

Board = List[List[str]]
Path = List[Tuple[int, int]]
Coordinate = Tuple[int, int]


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    word = ""
    for i in range(len(path)):
        curr_coordinate = path[i]
        if is_out_of_bounds(board, curr_coordinate):
            return None
        if i < len(path)-1:
            next_coordinate = path[i + 1]
            if not is_valid_distance(curr_coordinate, next_coordinate):
                return None
        word += board[curr_coordinate[0]][curr_coordinate[1]]
    if word in words:
        return word


def is_out_of_bounds(board: Board, curr_coordinate: Coordinate) -> bool:
    y, x = curr_coordinate
    if y > len(board) - 1 or y < 0 or \
            x > len(board[0]) or x < 0:
        return True
    return False


def is_valid_distance(curr_coordinate: Coordinate, next_coordinate: Coordinate) -> bool:
    curr_y, curr_x = curr_coordinate
    next_y, next_x = next_coordinate
    if abs(curr_y - next_y) > 1 or abs(curr_x - next_x) > 1:
        return False
    return True


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    # Inner function for depth-first search (DFS) traversal
    def dfs(i: int, j: int, path: Path, visited: List[List[bool]], word: str, result: List[Path]):
        # Base case: out-of-bounds or already visited cell
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]) or visited[i][j] or len(word) == n+1:
            return

        # Append current coordinate to the path
        path.append((i, j))
        visited[i][j] = True

        # Check if the path forms a word of length n from the words list
        if len(word) == n and word in words and path not in result:
            result.append(path[:])  # Append a copy of the path to the result list

        # Explore neighboring cells using DFS
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if ni >= 0 and ni < len(board) and nj >= 0 and nj < len(board[0]):
                    next_word = word + board[ni][nj]
                    dfs(ni, nj, path, visited, next_word, result)

        # Backtrack: mark current cell as unvisited and remove it from the path
        visited[i][j] = False
        path.pop()

    # Initialize result list, visited matrix, and perform DFS for each cell in the game board
    result = []
    visited = [[False] * len(board[0]) for _ in range(len(board))]

    for i in range(len(board)):
        for j in range(len(board[0])):
            word = board[i][j]  # Start a new word from each cell
            dfs(i, j, [], visited, word, result)

    return [[tuple(coord) for coord in path] for path in result]





def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass



