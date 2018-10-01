from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import random
import json

class MusicQuiz(ttk.Frame):
    def __init__(self, username, music, master=None, next_screen=lambda: None):
        ttk.Frame.__init__(self, master)
        self.next_screen = next_screen
        self.username = username
        self.music = music
        ttk.Label(self, text='Score:').grid(row=1, column=0)
        self.score_label = ttk.Label(self)
        self.score_label.grid(row=1, column=1)
        ttk.Label(self, text='Artist:').grid(row=2, column=0)
        self.artist_label = ttk.Label(self)
        self.artist_label.grid(row=2, column=1)
        ttk.Label(self, text='Song Acronym:').grid(row=3, column=0)
        self.song_label = ttk.Label(self)
        self.song_label.grid(row=3, column=1)
        ttk.Button(self, text='Guess', command=self.take_guess).grid(row=4,
                                                                     column=0)
        self.guess = tk.Text(self, width=80, height=1)
        self.guess.grid(row=4, column=1)
        self.reset_game()
    def reset_game(self):
        self.score = 0
        self.next_song()
        self.rerender_music()
    def next_song(self):
        self.song, self.artist = random.choice(self.music)
        self.wrong = 0
    def rerender_music(self):
        self.score_label.configure(text=str(self.score))
        self.artist_label.configure(text=self.artist)
        self.song_label.configure(text=''.join(i[0] for i in self.song.split()))
    def take_guess(self):
        if self.guess.get('1.0', 'end-1c') == self.song:
            messagebox.Message(message='Correct').show()
            self.score += 3 - self.wrong * 2
            self.next_song()
        else:
            messagebox.Message(message='Incorrect Hint its:'+self.song).show()
            self.wrong += 1
            if self.wrong >= 2:
                messagebox.Message(message='Game over, you scored: %s'
                                   % self.score).show()
                print(self.username, 'scored', self.score)
                try:
                    with open('leaderboard.json') as file:
                        score_data = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    score_data = []
                score_data.append([self.score, self.username])
                with open('leaderboard.json', 'w') as file:
                    json.dump(score_data, file)
                self.next_screen()
        self.rerender_music()
