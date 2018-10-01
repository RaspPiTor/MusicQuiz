from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import random

import auth_management
import music_quiz
import update_music
import leaderboard

class LoadScreen(ttk.Frame):
    def __init__(self, master=None, next_screen=lambda:None):
        ttk.Frame.__init__(self, master)
        style = ttk.Style(self)
        style.configure('Lscreen.TLabel', font=('Helvetica', 128),
                        foreground='red', background='black')
        main_text = ttk.Label(self, text='Music Quiz 0.1', style='Lscreen.TLabel')
        main_text.grid(row=0, column=0)
        self.load_songs = update_music.LoadSongs(self, next_screen)
        self.load_songs.grid(row=1, column=0, sticky='nesw')
        self.load_songs.columnconfigure(0, weight=1)

class MainMenu(ttk.Frame):
    def __init__(self, master, username, auth, quiz, leaderboard):
        ttk.Frame.__init__(self, master)
        ttk.Label(self, text='Username:').grid(row=0, column=0)
        ttk.Label(self, text=username).grid(row=0, column=1)
        ttk.Button(self, text='Logout', command=auth).grid(row=1, columnspan=2)
        ttk.Button(self, text='Quiz', command=quiz).grid(row=2, columnspan=2)
        ttk.Button(self, text='Leaderboard', command=leaderboard).grid(row=3, columnspan=2)
        

class QuizManager(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.current = LoadScreen(self, self.finished_loading)
        self.current.grid(row=0, column=0)
    def finished_loading(self, songs):
        self.songs = list(songs)
        style = ttk.Style(self)
        style.configure('Manager.TLabel', font=('Helvetica', 30),
                        foreground='red', background='black')
        ttk.Label(self, text='Music Quiz 0.1',
                  style='Manager.TLabel').grid(row=0, columnspan=2)
        self.auth_screen()
    def auth_screen(self):
        self.current.destroy()
        self.current = auth_management.AuthManagement(self, self.logged_in)
        self.current.grid(row=1)
    def logged_in(self, username):
        self.username = username
        self.start_screen()
    def start_screen(self):
        self.current.destroy()
        self.current = MainMenu(self, self.username, self.auth_screen,
                                self.quiz_screen, self.leaderboard_screen)
        self.current.grid(row=1)
    def quiz_screen(self):
        self.current.destroy()
        self.current =  music_quiz.MusicQuiz(self.username, self.songs, self,
                                             self.start_screen)
        self.current.grid(row=1)
    def leaderboard_screen(self):
        self.current.destroy()
        self.current = leaderboard.LeaderBoard(self, self.start_screen)
        self.current.grid(row=1)
        


if __name__ == '__main__':
    quiz = QuizManager()
    quiz.grid()
    quiz.mainloop()
