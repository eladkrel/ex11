import tkinter as tk
import time
from pygame import mixer
from BoggleBoard import *
import random

GAME_TIME = 20  # 3 minutes in seconds
FONT = 'Bell MT'
LOBBY_BEFORE_START_PATH = 'sounds/lobby_before_start.mp3'
GAME_PLAY_PATH = 'sounds/game_play.mp3'
POP_PATH = 'sounds/pop.mp3'
END_GAME_PATH = 'sounds/end_game.mp3'
CORRECT_SOUND_PATH = 'sounds/submit_correct_word.mp3'
INCORRECT_SOUND_PATH = 'sounds/submit_incorrect_word.mp3'
START_GAME_PATH = './start_game_button.png'
SUBMIT_BUTTON_PATH = './submit_1.png'
BG_COLOR = 'light blue'
MAX_SCORE_WIN = 'You Won! You got the max score!'
FOUND_ALL_WORDS = 'You found all the words in the game!'
INVALID_WORD = 'Invalid Word!'
ICYTOWER_SOUNDS = ['sounds/icy_tower/aight.ogg',
                   'sounds/icy_tower/amazing.ogg',
                   'sounds/icy_tower/cheer.ogg',
                   'sounds/icy_tower/extreme.ogg',
                   'sounds/icy_tower/fantastic.ogg',
                   'sounds/icy_tower/good.ogg',
                   'sounds/icy_tower/great.ogg',
                   'sounds/icy_tower/splendid.ogg',
                   'sounds/icy_tower/super.ogg',
                   'sounds/icy_tower/sweet.ogg',
                   'sounds/icy_tower/unbelievable.ogg',
                   'sounds/icy_tower/wow.ogg']
TIMES_UP = "Time's up! Play another game?"


class BoggleGUI:
    def __init__(self, boggle_board: BoggleBoard):
        """Init for the board GUI"""
        self.__root = tk.Tk()
        self.__root.config(bg=BG_COLOR)
        self.__root.title("Boggle Game")
        self.__root.geometry("700x600")
        self.__boggle_board = boggle_board
        self.__board_frame = None
        self.__board_buttons = []
        self.__words_text = None
        self.__submit_button = None
        self.__start_button = None
        self.__start_pic = tk.PhotoImage(file=START_GAME_PATH)
        self.__submit_pic = tk.PhotoImage(file=SUBMIT_BUTTON_PATH)
        self.__timer_label = None
        self.__start_time = None
        self.__word_entry = None
        self.__word_listbox = None
        self.__score_label = None
        self.__end_label = None
        self.__y_button = None
        self.__n_button = None
        self.__invalid_word_label = None
        self.__submitted_words = []
        self.__clicked_buttons = set()
        mixer.init()
        self.__create_widgets()
        self.__root.mainloop()

    def __create_widgets(self) -> None:
        """
        Function create widgets before game starts.
        """
        self.__start_button = tk.Button(self.__root,
                                        command=self.__start_game,
                                        image=self.__start_pic)
        self.__start_button.pack(pady=200, padx=30, side=tk.TOP)

        self.__timer_label = tk.Label(self.__root, text="", font=(FONT, 16),
                                      bg=BG_COLOR)
        self.__timer_label.pack()
        mixer.Channel(0).play(mixer.Sound(LOBBY_BEFORE_START_PATH), loops=-1)

    def __buttons_from_letters(self, board) -> None:
        """
        Function make buttons of all random letters in board.
        :param board: Board
        """
        for row in range(len(board)):
            row_buttons = []
            for col in range(len(board[0])):
                coord = (row, col)
                button = tk.Button(self.__board_frame, text=board[row][col],
                                   width=8, height=4,
                                   command=lambda c=coord: self.__add_letter(c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.__board_buttons.append(row_buttons)

    def __start_game(self) -> None:
        """
        Function update game with all widgets and tools needed for the game to
        run.
        """
        self.__start_button.destroy()
        mixer.Channel(0).play(mixer.Sound(GAME_PLAY_PATH), loops=-1)

        self.__board_frame = tk.Frame(self.__root, width=400, height=400)
        self.__board_frame.pack()
        self.__board_buttons = []
        board = self.__boggle_board.get_board_copy()
        self.__buttons_from_letters(board)
        self.__word_entry = tk.Entry(self.__root, font=(FONT, 12))
        self.__word_entry.pack()
        self.__word_entry.bind('<KeyPress>', lambda x: 'break')
        self.__submit_button = tk.Button(self.__root, image=self.__submit_pic,
                                         command=self.__submit_words,
                                         bg=BG_COLOR)
        self.__submit_button.pack()
        self.__submitted_words = []
        self.__word_listbox = tk.Listbox(self.__root, height=17, width=25,
                                         bg=BG_COLOR)
        self.__word_listbox.place(x=500, y=31)
        self.__invalid_word_label = tk.Label(self.__root, text="",
                                             font=(FONT, 12),
                                             bg=BG_COLOR)
        self.__invalid_word_label.pack()
        self.__score_label = tk.Label(self.__root, text="Score: 0",
                                      font=(FONT, 16), bg=BG_COLOR)
        self.__score_label.pack()
        self.__start_time = time.time()
        self.__update_timer()

    def __update_timer(self) -> None:
        """
        Function updates the timer every second and handle the program
        when game ends.
        """
        elapsed_time = int(time.time() - self.__start_time)
        remaining_time = max(GAME_TIME - elapsed_time, 0)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        self.__timer_label.configure(text=timer_text)

        if remaining_time >= 1:
            self.__root.after(1000 - (elapsed_time % 1000),
                              self.__update_timer)

        else:
            self.__timer_label.configure(text="Time: 00:00")
            self.__end_game()

    def __add_letter(self, coordinate: Coordinate) -> None:
        """
        Function updates the word the player is reaching
        with adding the current letter.
        :param coordinate: coordinate indexes
        """
        row, col = coordinate
        letter = self.__board_buttons[row][col]['text']

        button = self.__board_buttons[row][col]
        button.config(state=tk.DISABLED, bg="light gray")
        self.__clicked_buttons.add(button)
        self.__update_possible_buttons(coordinate)
        self.__boggle_board.add_coordinate(coordinate)
        current_word = self.__word_entry.get()
        new_word = current_word + letter
        self.__word_entry.delete(0, tk.END)
        self.__word_entry.insert(tk.END, new_word)

        mixer.music.load(POP_PATH)
        mixer.music.play()

    def __update_possible_buttons(self, coordinate: Coordinate) -> None:
        """
        Function receives an index of a button on the board and changes that
        all the buttons next to it are gray and enabled and the other buttons
        are white and disabled.
        :param coordinate: coordinate indexes
        """
        next_moves = self.__boggle_board.get_next_possible_moves(coordinate)
        for r in range(len(self.__board_buttons)):
            for c in range(len(self.__board_buttons[0])):
                button = self.__board_buttons[r][c]
                if button not in self.__clicked_buttons:
                    if (r, c) in next_moves:
                        button.config(state=tk.NORMAL, bg="gray")
                    else:
                        button.config(state=tk.DISABLED, bg="white")

    def __submit_words(self) -> None:
        """
        Function checks if word is valid. If so, word is added to the word list
        and player gets points.
        """
        self.__word_entry.delete(0, tk.END)

        valid = self.__boggle_board.add_submitted_word()
        if valid:
            # word is good
            self.__update_word_list()
            self.__invalid_word_label.config(text="")
            mixer.music.load(random.choice(ICYTOWER_SOUNDS))
            mixer.music.play()
            self.__score_label.config(text=f"Score: "
                                           f"{self.__boggle_board.get_score()}")
            if self.__boggle_board.is_max_score():
                self.__end_game()
        else:
            # word is no good
            self.__invalid_word_label.config(text=INVALID_WORD)
            mixer.music.load(INCORRECT_SOUND_PATH)
            mixer.music.play()

        # reset the board so player can start look for other word.
        self.__clicked_buttons.clear()
        for row in self.__board_buttons:
            for button in row:
                button.config(state=tk.NORMAL, bg="white")

    def __update_word_list(self) -> None:
        self.__word_listbox.delete(0, tk.END)
        for word in self.__boggle_board.get_submitted_words():
            self.__word_listbox.insert(tk.END, word)

    def __start_over(self) -> None:
        """
        Function starts new game if player wants to.
        """
        self.__root.destroy()
        BoggleGUI(BoggleBoard())

    def __exit_game(self) -> None:
        """
        Function exit game if player wants to.
        """
        self.__root.destroy()
        mixer.music.stop()
        quit()

    def __end_game(self) -> None:
        """
        Function handles the labels and widgets when the game ends.
        """
        self.__board_frame.destroy()
        self.__word_entry.destroy()
        self.__submit_button.destroy()
        end_frame = tk.Frame(self.__root, bg=BG_COLOR)
        end_frame.pack()
        end_text = self.__get_end_text()
        self.__end_label = tk.Label(end_frame, text=end_text,
                                    font=(FONT, 16), bg=BG_COLOR)
        self.__end_label.grid(row=0, column=0, columnspan=2)
        self.__y_button = tk.Button(end_frame, text='Yes!', font=(FONT, 20),
                                    command=self.__start_over, bg=BG_COLOR)
        self.__y_button.grid(row=1, column=0)
        self.__n_button = tk.Button(end_frame, text='Nope', font=(FONT, 20),
                                    command=self.__exit_game, bg=BG_COLOR)
        self.__n_button.grid(row=1, column=1)

        mixer.Channel(0).stop()
        mixer.music.load(END_GAME_PATH)
        mixer.music.play()

    def __get_end_text(self):
        if self.__boggle_board.is_max_score():
            return MAX_SCORE_WIN
        elif self.__boggle_board.is_found_all_words():
            return FOUND_ALL_WORDS
        else:
            return TIMES_UP


if __name__ == "__main__":
    boggle_gui = BoggleGUI(BoggleBoard())
