import tkinter as tk
from tkinter import PhotoImage
from gui_history import GameHistoryGui
from gui_game import GameManageGui

class MainGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chinese Checkers")
        self.image_path = "game_files/img1.png"
        self.image = PhotoImage(file=self.image_path)
        self.image = self.image.subsample(5)  # Adjust image size
        self.label_image = tk.Label(self, image=self.image)
        self.label_image.pack()
        self.button1 = tk.Button(self, text="New Game", 
                                width=20, height=5, command=self.show_game_manage_gui)
        self.button1.pack()
        self.button2 = tk.Button(self, text="Games History", 
                                width=20, height=5, command=self.show_game_history_gui)
        self.button2.pack()

    def show_game_manage_gui(self):
        self.destroy()  # Destroy the current window
        game_manage_window = GameManageGui()
        game_manage_window.mainloop()

    def show_game_history_gui(self):
        self.destroy()  # Destroy the current window
        game_history_window = GameHistoryGui()
        game_history_window.mainloop()