import tkinter as tk
from tkinter import messagebox
import file_utils
import file_colors
from game import Game


VALID_PLAYERS_NUM = [2,3,4,6]

PLAYERS_FILE = "game_files/players.pkl"
class GameManageGui(tk.Tk):
    '''game manger screen'''
    def __init__(self):
        super().__init__()
        self.title("New Game")
        self.players_to_play=set()
        self.auto_players = tk.IntVar(value=0)
        self.players = {}

        self.create_widgets()

    def clear_page(self):
        '''this function clear all the page from gui items'''
        for widget in self.winfo_children():
            widget.destroy()
    
    def add_or_delete(self, idx):
        '''this function gets id of player and delete it if exist
        or add it if not'''
        if idx in self.players_to_play:
            self.players_to_play.remove(idx)
        else:
            self.players_to_play.add(idx)

    def create_widgets(self):
        '''this function generates the players table and the buttons'''
        self.clear_page()
        self.players = file_utils.get_dict_from_pickle(PLAYERS_FILE)
        # Create headers
        headers = ["select", "ID", "Name", "Color", "Wins", "Losses", "Edit"]
        for i, header in enumerate(headers):
            label = tk.Label(self, text=header)
            label.grid(row=0, column=i)

        # Populate table with player data
        self.player_widgets = {}
        #generates row in table for each player
        for player_id in self.players:
            checkbox = tk.Checkbutton(self, 
                        command=lambda idx=player_id: self.add_or_delete(idx))
            player = self.players[player_id]
            checkbox.grid(row=player_id, column=0)
            id_label = tk.Label(self, text=player_id)
            id_label.grid(row=player_id, column=1)
            name_label = tk.Label(self, text=player[0])
            name_label.grid(row=player_id, column=2)
            color_label = tk.Label(self, text="   ", bg= file_colors.COLORS_CODE[player[1]])
            color_label.grid(row=player_id, column=3)
            wins_label = tk.Label(self, text=player[2])
            wins_label.grid(row=player_id, column=4)
            losses_label = tk.Label(self, text=player[3])
            losses_label.grid(row=player_id, column=5)
            
            edit_button = tk.Button(self, text="Edit", 
                            command=lambda idx=player_id: self.edit_player(idx))
            edit_button.grid(row=player_id, column=6)

            self.player_widgets[player_id] = {
                "id": id_label,
                "name": name_label,
                "color": color_label,
                "wins": wins_label,
                "losses": losses_label
            }
        
        tk.Label(self, text="Computers in game:").grid(
            row=len(self.players) + 3, column=1)
        comp = tk.OptionMenu(self, self.auto_players, *[0,1,2,3,4,5,6])
        comp.grid(row=len(self.players) + 3, column=2)

        start_button = tk.Button(self, text="Start game", command=self.start_new_game)
        start_button.grid(row=len(self.players) + 4, column=3, columnspan=7, pady=10)

        add_button = tk.Button(self, text="Add Player", 
                               command=self.add_player_window)
        add_button.grid(row=len(self.players) + 1, column=0, columnspan=7, pady=10)

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

    def edit_player(self, index):
        '''this function act when user click on player edit - edit screen'''
        player_info = self.players[index]
        EditPlayerWindow(player_info, self, index)

    def add_player_window(self):
        '''this function act when user click on player add - add screen'''
        AddPlayerWindow(self)
    
    def start_new_game(self):
        '''this function act when user click on start play - collecting
        all choosen players and add to the game'''
        if len(self.players_to_play) == 1 and not self.auto_players.get():
            try:
                #import online game just if the player asked for
                from gui_online import GameOnline

                #online game when slect 1 human player
                player = file_utils.get_players_from_list(self.players_to_play)[0]
                gm = GameOnline(player)
                gm.start_game_online()
            except:
                pass

        elif (self.auto_players.get() + len(self.players_to_play)) in VALID_PLAYERS_NUM:
            #local game 2/3/4/6 players also computers
            game = Game()
            total_players = {-com for com in range(self.auto_players.get())}
            total_players.update(self.players_to_play)
            game.add_players(file_utils.get_players_from_list(total_players))
            game.load_gui()
        else:
            messagebox.showinfo("Players error", 
                                "please select 2/3/4/6 players to play or one player for online game")

class EditPlayerWindow(tk.Toplevel):
    '''edit player screen'''
    def __init__(self, player_info, parent, index):
        super().__init__()
        self.parent = parent
        self.index = index
        self.player_info = player_info
        self.title("Edit Player")
        self.create_widgets()

    def create_widgets(self):
        '''create the window, adding inputs with the current data'''
        tk.Label(self, text="ID:").grid(row=0, column=0)
        self.id_label = tk.Label(self, text=self.index)
        self.id_label.grid(row=0, column=1)

        tk.Label(self, text="Name:").grid(row=1, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1)
        self.name_entry.insert(0, self.player_info[0])

        tk.Label(self, text="Color:").grid(row=2, column=0)
        self.color_var = tk.StringVar(value=file_colors.COLORS_NAME[self.player_info[1]])
        self.color_combobox = tk.OptionMenu(self, self.color_var, *file_colors.COLORS_NAME)
        self.color_combobox.grid(row=2, column=1)

        tk.Button(self, text="Save", 
                  command=self.save_player).grid(
                      row=3, column=0, columnspan=2, pady=10)

    def save_player(self):
        '''save player in file and update the table'''
        self.parent.players[self.index][0] = self.name_entry.get()
        self.parent.players[self.index][1] = file_colors.COLORS_NAME.index(self.color_var.get())
        file_utils.save_dict_to_pickle(self.parent.players, PLAYERS_FILE)
        self.parent.create_widgets()

class AddPlayerWindow(tk.Toplevel):
    '''add player window'''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Add Player")
        self.create_widgets()

    def create_widgets(self):
        '''creating window with empty inputs'''
        tk.Label(self, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Color:").grid(row=1, column=0)
        self.color_var = tk.StringVar(value=file_colors.COLORS_NAME[0])
        self.color_combobox = tk.OptionMenu(self, self.color_var, *file_colors.COLORS_NAME)
        self.color_combobox.grid(row=1, column=1)

        tk.Button(self, text="Save", 
                command=self.save_player).grid(
                    row=2, column=0, columnspan=2, pady=10)

    def save_player(self):
        '''save the player in file, updating the table'''
        self.parent.players[len(self.parent.players) + 1] = [
            self.name_entry.get(), file_colors.COLORS_NAME.index(
                self.color_var.get()) , 0 ,0]
        file_utils.save_dict_to_pickle(self.parent.players, PLAYERS_FILE)
        self.parent.create_widgets()