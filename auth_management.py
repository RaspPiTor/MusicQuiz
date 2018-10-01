from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import json
import hashlib
class AuthManagement(ttk.Frame):
    def __init__(self, master=None, next_screen=lambda user:None):
        ttk.Frame.__init__(self, master)
        try:
            with open('users.json') as file:
                self.login_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.login_data = {}
        ttk.Label(self, text='Username:').grid(row=1, column=0)
        self.username = tk.Text(self, width=20, height=1)
        self.username.grid(row=1, column=1)
        ttk.Label(self, text='Password:').grid(row=2, column=0)
        self.password = tk.Text(self, width=20, height=1)
        self.password.grid(row=2, column=1)
        ttk.Button(self, text='Login', command=self.login).grid(row=3, column=0)
        ttk.Button(self, text='Register', command=self.register).grid(row=3,
                                                                      column=1)
        self.next_screen = next_screen
    def login(self):
        username = self.username.get('1.0', 'end-1c')
        password = self.password.get('1.0', 'end-1c').encode()
        password_hash = hashlib.sha3_512(password).hexdigest()
        if username in self.login_data:
            if self.login_data[username] == password_hash:
                self.next_screen(username)
            else:
                messagebox.Message(message='Incorrect password').show()
        else:
            messagebox.Message(message='User doesn\'t exist').show()

    def register(self):
        username = self.username.get('1.0', 'end-1c')
        password = self.password.get('1.0', 'end-1c').encode()
        password_hash = hashlib.sha3_512(password).hexdigest()
        if username not in self.login_data:
            self.login_data[username] = password_hash
            with open('users.json', 'w') as file:
                json.dump(self.login_data, file)
            self.next_screen(username)
        else:
            messagebox.Message(message='User exists').show()
