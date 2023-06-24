import tkinter as tk
import time
import pygame

class BoggleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Boggle Game")
        self.root.geometry("500x500")

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
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.timer_label.pack()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
            'sounds/lobby_before_start.mp3'), loops=-1)

    def start_game(self):
        self.start_button.destroy()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
            'sounds/game_play.mp3'), loops=-1)

        self.board_frame = tk.Frame(self.root, width=400, height=400)
        self.board_frame.pack()

        self.board_buttons = []
        for row in range(4):
            row_buttons = []
            for col in range(4):
                button = tk.Button(self.board_frame, text="A", width=6, height=3,
                                   command=lambda r=row, c=col: self.add_letter(r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

        self.word_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.word_entry.pack()

        self.words_text = tk.Text(self.root, height=5)
        self.words_text.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_words)
        self.submit_button.pack()

        self.submitted_words = []
        self.word_listbox = tk.Listbox(self.root, height=10, width=30)
        self.word_listbox.pack()

        self.invalid_word_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.invalid_word_label.pack()

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(20 - elapsed_time, 0)

        minutes = remaining_time // 60
        seconds = remaining_time % 60

        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        self.timer_label.configure(text=timer_text)

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="Time's up!")
            pygame.mixer.Channel(0).stop()
            pygame.mixer.music.load('sounds/end_game.mp3')
            pygame.mixer.music.play()

    def add_letter(self, row, col):
        letter = self.board_buttons[row][col]['text']

        button = self.board_buttons[row][col]
        button.config(state=tk.DISABLED, bg="light gray")
        self.clicked_buttons.add(button)
        self.update_possible_buttons(row, col)

        current_word = self.word_entry.get()
        new_word = current_word + letter
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(tk.END, new_word)

        pygame.mixer.music.load('sounds/pop.mp3')
        pygame.mixer.music.play()

    def update_possible_buttons(self, row, col):
        self.next_possible_buttons.clear()

        for r in range(4):
            for c in range(4):
                button = self.board_buttons[r][c]
                if button not in self.clicked_buttons:
                    if abs(r - row) <= 1 and abs(c - col) <= 1:
                        self.next_possible_buttons.add(button)
                        button.config(state=tk.NORMAL, bg="gray")
                    else:
                        button.config(state=tk.DISABLED, bg="white")

    def submit_words(self):
        word = self.word_entry.get()
        self.word_entry.delete(0, tk.END)

        valid = self.check_word(word)

        if valid:
            self.submitted_words.append(word)
            self.update_word_list()
            self.invalid_word_label.config(text="")
            pygame.mixer.music.load('sounds/submit_correct_word.mp3')
            pygame.mixer.music.play()
        else:
            self.invalid_word_label.config(text="Invalid word!")
            pygame.mixer.music.load('sounds/submit_incorrect_word.mp3')
            pygame.mixer.music.play()

        for button in self.clicked_buttons:
            button.config(bg="white")

        self.clicked_buttons.clear()

        for row in self.board_buttons:
            for button in row:
                button.config(state=tk.NORMAL, bg="white")

    def check_word(self, word):
        if word in self.submitted_words:
            return False
        elif len(word) < 3:
            return False
        else:
            return True

    def update_word_list(self):
        self.word_listbox.delete(0, tk.END)
        for word in self.submitted_words:
            self.word_listbox.insert(tk.END, word)


if __name__ == "__main__":
    boggle_gui = BoggleGUI()
