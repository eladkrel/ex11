import tkinter as tk
import time
import pygame
from BoggleBoard import *

GAME_TIME = 200  # 3 minutes in seconds
FONT = 'Helvetica'
LOBBY_BEFORE_START_PATH = 'sounds/lobby_before_start.mp3'
GAME_PLAY_PATH = 'sounds/game_play.mp3'
POP_PATH = 'sounds/pop.mp3'
END_GAME_PATH = 'sounds/end_game.mp3'
CORRECT_SOUND_PATH = 'sounds/submit_correct_word.mp3'
INCORRECT_SOUND_PATH = 'sounds/submit_incorrect_word.mp3'
START_GAME_PATH = './start_game_button.png'

class BoggleGUI:
    def __init__(self, boggle_board: BoggleBoard):
        self.root = tk.Tk()
        self.root.title("Boggle Game")
        self.root.geometry("500x500")
        self.__boggle_board = boggle_board
        self.board_frame = None
        self.board_buttons = []
        self.words_text = None
        self.submit_button = None
        self.start_button = None
        self.timer_label = None
        self.start_time = None
        self.word_entry = None
        self.submitted_words = []
        self.clicked_buttons = set()
        self.next_possible_buttons = set()

        self.invalid_word_label = None

        pygame.mixer.init()

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        self.start_pic = tk.PhotoImage(file=START_GAME_PATH)
        self.start_button = tk.Button(self.root,
                                      command=self.start_game,
                                      image=self.start_pic)
        self.start_button.pack(pady=30, padx=30, side=tk.TOP)

        self.timer_label = tk.Label(self.root, text="", font=(FONT, 16))
        self.timer_label.pack()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
            LOBBY_BEFORE_START_PATH), loops=-1)

    def start_game(self):
        self.start_button.destroy()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(GAME_PLAY_PATH),
                                     loops=-1)

        self.board_frame = tk.Frame(self.root, width=400, height=400)
        self.board_frame.pack()

        self.board_buttons = []
        board = self.__boggle_board.get_board_copy()
        for row in range(len(board)):
            row_buttons = []
            for col in range(len(board[0])):
                coordinate = (row, col)
                button = tk.Button(self.board_frame, text=board[row][col],
                                   width=6, height=3,
                                   command=lambda c=coordinate: self.add_letter(c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

        self.word_entry = tk.Entry(self.root, font=(FONT, 12))
        self.word_entry.pack()

        self.words_text = tk.Text(self.root, height=5)
        self.words_text.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_words)
        self.submit_button.pack()

        self.submitted_words = []
        self.word_listbox = tk.Listbox(self.root, height=10, width=30)
        self.word_listbox.pack()

        self.invalid_word_label = tk.Label(self.root, text="", font=(FONT, 12))
        self.invalid_word_label.pack()

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(GAME_TIME - elapsed_time, 0)

        minutes = remaining_time // 60
        seconds = remaining_time % 60

        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        self.timer_label.configure(text=timer_text)

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="Time's up!")
            pygame.mixer.Channel(0).stop()
            pygame.mixer.music.load(END_GAME_PATH)
            pygame.mixer.music.play()

    def add_letter(self, coordinate: Coordinate):
        row, col = coordinate
        letter = self.board_buttons[row][col]['text']

        button = self.board_buttons[row][col]
        button.config(state=tk.DISABLED, bg="light gray")
        self.clicked_buttons.add(button)
        self.update_possible_buttons(coordinate)
        self.__boggle_board.add_coordinate(coordinate)
        current_word = self.word_entry.get()
        new_word = current_word + letter
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(tk.END, new_word)

        pygame.mixer.music.load(POP_PATH)
        pygame.mixer.music.play()

    def update_possible_buttons(self, coordinate: Coordinate):
        """
        Function receives an index of a button on the board and changes that
        all the buttons next to it are gray and enabled and the other buttons
        are white and disabled.
        :param coordinate: coordinate indexes
        """
        self.next_possible_buttons = set()
        next_moves = self.__boggle_board.get_next_possible_moves(coordinate)
        row, col = coordinate
        for r in range(len(self.board_buttons)):
            for c in range(len(self.board_buttons[0])):
                button = self.board_buttons[r][c]
                if button not in self.clicked_buttons:
                    if (r, c) in next_moves:
                        self.next_possible_buttons.add(button)
                        button.config(state=tk.NORMAL, bg="gray")
                    else:
                        button.config(state=tk.DISABLED, bg="white")

    def submit_words(self):
        word = self.word_entry.get()
        self.word_entry.delete(0, tk.END)

        valid = self.__boggle_board.add_submitted_word()
        if valid:
            self.update_word_list()
            self.invalid_word_label.config(text="")
            pygame.mixer.music.load(CORRECT_SOUND_PATH)
            pygame.mixer.music.play()
        else:
            self.invalid_word_label.config(text="Invalid word!")
            pygame.mixer.music.load(INCORRECT_SOUND_PATH)
            pygame.mixer.music.play()

        # for button in self.clicked_buttons:
        #     button.config(bg="white")

        self.clicked_buttons.clear()

        for row in self.board_buttons:
            for button in row:
                button.config(state=tk.NORMAL, bg="white")

    def update_word_list(self):
        self.word_listbox.delete(0, tk.END)
        for word in self.__boggle_board.get_submitted_words():
            self.word_listbox.insert(tk.END, word)


if __name__ == "__main__":
    boggle_gui = BoggleGUI(BoggleBoard())
