from tkinter import ttk
import tkinter as tk
import json

class LeaderBoard(ttk.Frame):
    def __init__(self, master=None, next_screen=lambda:None):
        ttk.Frame.__init__(self, master)
        try:
            with open('leaderboard.json') as file:
                score_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            score_data = []
        score_data.sort(reverse=True)
        style = ttk.Style(self)
        style.configure('Lboard.TButton', font=('Helvetica', 30),
                        foreground='red', background='black')
        ttk.Button(self, text='Back to Main Menu', style='Lboard.TButton',
                   command=next_screen).grid(row=0, columnspan=4)
        ttk.Label(self, text='Score').grid(row=1, column=1)
        ttk.Label(self, text='Username').grid(row=1, column=2)
        
        for i, (score, username) in enumerate(score_data[:5]):
            ttk.Label(self, text=str(score)).grid(row=i + 2, column=1)
            ttk.Label(self, text=username).grid(row=i + 2, column=2)
