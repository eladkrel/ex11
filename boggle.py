import tkinter as tk
import time
import pygame
from BoggleBoard import *

import random  # check if can



GAME_TIME = 180  # 3 minutes in seconds
FONT = 'Bell MT'  # NEW
LOBBY_BEFORE_START_PATH = 'sounds/lobby_before_start.mp3'
GAME_PLAY_PATH = 'sounds/game_play.mp3'
POP_PATH = 'sounds/pop.mp3'
END_GAME_PATH = 'sounds/end_game.mp3'
CORRECT_SOUND_PATH = 'sounds/submit_correct_word.mp3'
INCORRECT_SOUND_PATH = 'sounds/submit_incorrect_word.mp3'
START_GAME_PATH = './start_game_button.png'
SUBMIT_BUTTON_PATH = './submit_1.png'
BG_COLOR = 'light blue'


def disable_backspace(event):  # NEW
    """
    Function cancel 'backspace' when trying to delete information
    from word entry.
    :param event: KeyEvent
    """
    if event.keysym == 'BackSpace':
        return 'break'  # Prevent Backspace key press from being processed


def random_sounds():
    """
    Function randomize sound from specific folder.
    """
    icytower_sounds = ['sounds/icy_tower/aight.ogg', 'sounds/icy_tower/amazing.ogg', 'sounds/icy_tower/cheer.ogg',
                 'sounds/icy_tower/extreme.ogg', 'sounds/icy_tower/fantastic.ogg', 'sounds/icy_tower/good.ogg',
                 'sounds/icy_tower/great.ogg', 'sounds/icy_tower/splendid.ogg', 'sounds/icy_tower/super.ogg',
                 'sounds/icy_tower/sweet.ogg', 'sounds/icy_tower/unbelievable.ogg', 'sounds/icy_tower/wow.ogg']
    random_file = random.choice(icytower_sounds)
    return random_file


class BoggleGUI:
    def __init__(self, boggle_board: BoggleBoard):
        self.root = tk.Tk()
        self.root.config(bg=BG_COLOR)  # NEW
        self.root.title("Boggle Game")
        self.root.geometry("700x600")  # NEW
        self.__boggle_board = boggle_board
        self.board_frame = None
        self.board_buttons = []
        self.words_text = None
        self.submit_button = None
        self.start_button = None
        self.start_pic = tk.PhotoImage(file=START_GAME_PATH)
        self.submit_pic = tk.PhotoImage(file=SUBMIT_BUTTON_PATH)
        self.timer_label = None
        self.start_time = None
        self.word_entry = None
        self.word_listbox = None
        self.submitted_words = []
        self.clicked_buttons = set()
        self.next_possible_buttons = set()
        self.invalid_word_label = None
        pygame.mixer.init()
        self.create_widgets()
        self.root.mainloop()
        self.score_label = None  # NEW

    def create_widgets(self):
        """
        Function create widgets before game starts.
        """
        self.start_button = tk.Button(self.root,
                                      command=self.start_game,
                                      image=self.start_pic)
        self.start_button.pack(pady=200, padx=30, side=tk.TOP)

        self.timer_label = tk.Label(self.root, text="", font=(FONT, 16), bg=BG_COLOR)
        self.timer_label.pack()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
            LOBBY_BEFORE_START_PATH), loops=-1)


    def buttons_for_letters(self, board):
        """
        Function make buttons of all random letters in board.
        :param board: Board
        """
        for row in range(len(board)):
            row_buttons = []
            for col in range(len(board[0])):
                coord = (row, col)
                button = tk.Button(self.board_frame, text=board[row][col],
                                   width=8, height=4,
                                   command=lambda c=coord: self.add_letter(c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

    def start_game(self):
        """
        Function update game with all widgets and tools needed for the game to run.
        """
        self.start_button.destroy()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(GAME_PLAY_PATH),
                                     loops=-1)

        self.board_frame = tk.Frame(self.root, width=400, height=400)
        self.board_frame.pack()
        self.board_buttons = []
        board = self.__boggle_board.get_board_copy()
        self.buttons_for_letters(board)  # create buttons for random letters  # NEW
        self.word_entry = tk.Entry(self.root, font=(FONT, 12))
        self.word_entry.pack()
        self.word_entry.bind('<KeyPress>', disable_backspace)  # NEW
        self.submit_button = tk.Button(self.root, image=self.submit_pic,
                                       command=self.submit_words, bg=BG_COLOR)
        self.submit_button.pack()
        self.submitted_words = []
        self.word_listbox = tk.Listbox(self.root, height=17, width=25, bg=BG_COLOR)
        self.word_listbox.place(x=500, y=31)
        self.invalid_word_label = tk.Label(self.root, text="", font=(FONT, 12), bg=BG_COLOR)
        self.invalid_word_label.pack()
        self.score_label = tk.Label(self.root, text="Score: 0", font=(FONT, 16), bg=BG_COLOR)   #NEW
        self.score_label.pack()  #NEW
        self.start_time = time.time()
        self.update_timer()


    def update_timer(self):  # NEED TO UNDERSTAND
        """
        Function updates the timer every second and handle the program
        when game ends.
        """
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(GAME_TIME - elapsed_time, 0)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        self.timer_label.configure(text=timer_text)

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)
        # else:
        #     self.timer_label.configure(text="Time's up!")
        #     pygame.mixer.Channel(0).stop()
        #     pygame.mixer.music.load(END_GAME_PATH)
        #     pygame.mixer.music.play()

        else:  #NEW

            self.timer_label.configure(text="Time: 00:00")
            self.board_frame.destroy()
            self.word_entry.destroy()
            self.submit_button.destroy()
            end_frame = tk.Frame(self.root, bg=BG_COLOR)
            end_frame.pack()
            self.end_label = tk.Label(end_frame, text="Time's up! Play another game?", font=(FONT, 16), bg=BG_COLOR)
            self.end_label.grid(row=0, column=0, columnspan=2)
            self.y_button = tk.Button(end_frame, text='Yes!!', font=(FONT, 20), command=self.start_over, bg=BG_COLOR)
            self.y_button.grid(row=1, column=0)
            self.n_button = tk.Button(end_frame, text='Nope', font=(FONT, 20), command=self.end_game, bg=BG_COLOR)
            self.n_button.grid(row=1, column=1)

            pygame.mixer.Channel(0).stop()
            pygame.mixer.music.load(END_GAME_PATH)
            pygame.mixer.music.play()





    def add_letter(self, coordinate: Coordinate):
        """
        Function updates the word the player is reaching
        with adding the current letter.
        """
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
        """
        Function checks if word is valid. If so, word is added to the word list
        and player gets points.
        """
        self.word_entry.delete(0, tk.END)

        valid = self.__boggle_board.add_submitted_word()
        if valid:
            # word is good
            self.update_word_list()
            self.invalid_word_label.config(text="")
            pygame.mixer.music.load(random_sounds())  # NEW
            # pygame.mixer.music.load(CORRECT_SOUND_PATH)
            pygame.mixer.music.play()
            self.score_label.config(text=f"Score: {self.__boggle_board.get_score()}")  # NEW
        else:
            # word is no good
            self.invalid_word_label.config(text="Invalid word!")
            pygame.mixer.music.load(INCORRECT_SOUND_PATH)
            pygame.mixer.music.play()

        # for button in self.clicked_buttons:
        #     button.config(bg="white")

        # reset the board so player can start look for other word.
        self.clicked_buttons.clear()
        for row in self.board_buttons:
            for button in row:
                button.config(state=tk.NORMAL, bg="white")

    def update_word_list(self):  # NEED TO UNDERSTAND
        self.word_listbox.delete(0, tk.END)
        for word in self.__boggle_board.get_submitted_words():
            self.word_listbox.insert(tk.END, word)



    def start_over(self):  #NEW
        """
        Function starts new game if player wants to.
        """
        self.root.destroy()
        new_game = BoggleGUI(BoggleBoard())

    def end_game(self):  #NEW
        """
        Function exit game if player wants to.
        """
        self.root.destroy()
        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    boggle_gui = BoggleGUI(BoggleBoard())


