from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

import urllib.request
import html
import re

import threading
import queue


class LoadSongs(ttk.Frame):
    def __init__(self, master=None, next_screen=lambda songs:None):
        ttk.Frame.__init__(self, master)
        self.progress = ttk.Progressbar(self, orient='horizontal',
                                        mode='determinate')
        self.progress.grid(row=0, column=0, sticky='nesw')
        self.progress.columnconfigure(0, weight=1)
        self.progress['value'] = 0
        self.progress['maximum'] = 1
        self.in_queue = queue.Queue()
        self.updater = Updater(self.in_queue)
        self.updater.start()
        self.songs = set()
        self.after(5, self.render_new_songs)
        self.next_screen = next_screen
        
    def render_new_songs(self):
        try:
            while True:
                song, artist, value, maximum = self.in_queue.get(0)
                self.progress['value'] = value + 1
                self.progress['maximum'] = maximum
                self.songs.add((song, artist))
            self.after(5, self.render_new_songs)
        except queue.Empty:
            if self.updater.is_alive():
                self.after(5, self.render_new_songs)
            else:
                self.next_screen(self.songs)

class Updater(threading.Thread):
    REGEX = re.compile('<div class="chart-list-item  " data-rank="[0-9]+" '
                   'data-artist="([^"]+)" data-title="([^"]+)"')

    URLs = ['https://www.billboard.com/charts/hot-100',
            'https://www.billboard.com/charts/billboard-200',
            'https://www.billboard.com/charts/radio-songs',
            'https://www.billboard.com/charts/digital-song-sales',
            'https://www.billboard.com/charts/streaming-songs',
            'https://www.billboard.com/charts/on-demand-songs',
            'https://www.billboard.com/charts/top-album-sales',
            'https://www.billboard.com/charts/digital-albums',
            'https://www.billboard.com/charts/vinyl-albums',
            'https://www.billboard.com/charts/independent-albums',
            'https://www.billboard.com/charts/catalog-albums',
            'https://www.billboard.com/charts/tastemaker-albums'
            ]
    def __init__(self, output_queue):
        threading.Thread.__init__(self)
        self.output_queue = output_queue

    def run(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        for i, url in enumerate(self.URLs):
            print(i, url)
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                source = response.read().decode('utf-8', 'ignore')

                for artist, song in self.REGEX.findall(source):
                   song, artist = html.unescape(song), html.unescape(artist)
                   self.output_queue.put((song, artist, i, len(self.URLs)))
                if not self.REGEX.findall(source):
                    print(url, 'empty')
