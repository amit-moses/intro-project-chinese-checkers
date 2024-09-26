import tkinter as tk
from tkinter import messagebox
import file_utils
import file_colors
from game import Game
PLAYERS_FILE = "game_files/players.pkl"
GAMES_FILE = "game_files/game_index.pkl"

class GameHistoryGui(tk.Tk):
    '''history viewer windows'''
    def __init__(self):
        super().__init__()
        self.title("Games History")
        self.create_widgets()
    
    def restore(self, idx, play = False):
        '''restore old game - watch old moves'''
        try:
            if idx:
                game = Game(idx, show_result=False)
                game.load_gui(not play)
        except:
            pass

    def create_widgets(self):
        '''creates history table'''
        games = file_utils.get_dict_from_pickle(GAMES_FILE)
        players =  file_utils.get_dict_from_pickle(PLAYERS_FILE) 

        self.players = file_utils.get_dict_from_pickle(PLAYERS_FILE)
        # Populate table with player data
        self.player_widgets = {}

        #create row for each game
        for game_id in games:

            id_label = tk.Label(self, text=str(game_id))
            id_label.grid(row=game_id, column=0)

            one_game = games[game_id]

            #add all players and colored background if the player won
            for i, player_id in enumerate(one_game[0]):
                if 0 < player_id and players.get(player_id):
                    pl_label = tk.Label(self, text=players[
                        player_id][0].center(10), bg= file_colors.COLORS_CODE[players[
                            player_id][1]] if player_id is one_game[1] else None)
                else:
                    pl_label = tk.Label(self, 
                                text=f"computer{-1*player_id}".center(10), 
                                bg= file_colors.COMP_COLORS[max(0, -1*player_id)
                                ] if player_id is one_game[1] else None)
                    
                pl_label.grid(row=game_id, column=i+1)
            
            restore = tk.Button(self, text="restore", 
                        command=lambda idx=game_id: self.restore(idx, False))
            restore.grid(row=game_id, column=7)

            play = tk.Button(self, text="continue", 
                        command=lambda idx=game_id: self.restore(idx, True))
            play.grid(row=game_id, column=8)
        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.grid()

    def back(self):
        '''back to main page'''
        try:
            self.destroy()
            from gui_main import MainGui
            appi = MainGui()
            appi.mainloop()
        except:
            pass