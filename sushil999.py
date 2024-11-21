import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
from mutagen.mp3 import MP3

# Initialize Pygame mixer
pygame.mixer.init()

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("600x400")

        self.current_song = None
        self.is_playing = False
        
        # Create widgets
        self.play_button = tk.Button(self, text="Play", command=self.toggle_play)
        self.play_button.pack()

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_music)
        self.stop_button.pack()

        self.next_button = tk.Button(self, text="Next", command=self.next_song)
        self.next_button.pack()

        self.previous_button = tk.Button(self, text="Previous", command=self.previous_song)
        self.previous_button.pack()

        self.volume_slider = tk.Scale(self, from_=0, to=100, orient="horizontal", label="Volume")
        self.volume_slider.set(50)
        self.volume_slider.pack()

        self.progress_bar = tk.Scale(self, from_=0, to=100, orient="horizontal", label="Progress")
        self.progress_bar.pack()

        self.playlist = tk.Listbox(self)
        self.playlist.pack()

        self.add_button = tk.Button(self, text="Add Song", command=self.add_song)
        self.add_button.pack()

    def toggle_play(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            if not self.current_song:
                self.current_song = self.playlist.get(tk.ACTIVE)
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            self.play_button.config(text="Pause")
        self.is_playing = not self.is_playing

    def stop_music(self):
        pygame.mixer.music.stop()
        self.play_button.config(text="Play")
        self.is_playing = False

    def next_song(self):
        current_index = self.playlist.curselection()[0]
        next_index = (current_index + 1) % len(self.playlist.get(0, tk.END))
        self.playlist.select_set(next_index)
        self.toggle_play()

    def previous_song(self):
        current_index = self.playlist.curselection()[0]
        previous_index = (current_index - 1) % len(self.playlist.get(0, tk.END))
        self.playlist.select_set(previous_index)
        self.toggle_play()

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.insert(tk.END, file_path)

    def update_progress(self):
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
            song_length = MP3(self.current_song).info.length
            progress = (current_time / song_length) * 100
            self.progress_bar.set(progress)
        self.after(1000, self.update_progress)

if __name__ == "__main__":
    app = MusicPlayer()
    app.update_progress()
    app.mainloop()
