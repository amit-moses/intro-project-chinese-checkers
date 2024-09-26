import tkinter as tk
from tkinter import messagebox
from board import Board
from player import Player
from logs import MyLog

class RoundButton(tk.Canvas):
    '''class for round button with color of the player'''
    def __init__(self, gui, master=None, radius=25, outline_radius=None, cor=None, *args, **kwargs):
        super().__init__(master, width=2 * radius, height=2 * radius, highlightthickness=0, *args, **kwargs)
        self.radius = radius
        self.outline_radius = outline_radius if outline_radius is not None else radius
        self.update_style()
        self.bind("<Button-1>", self.on_button_click)
        self.cord = cor
        self.gui_board = gui

        
    def delete_text(self):
        '''delete the text inside the button (marker)'''
        for item in self.find_withtag("text"):
            self.delete(item)
    
    def update_style(self, bg_color="#ffffff", outline_width=1, outline_color="#000000"):
        '''update the style of the button'''
        if not outline_width:
            outline_width = 1
        try:
            self.create_oval(0, 0, 2 * self.radius, 2 * self.radius, 
                         outline=outline_color, width=outline_width, fill=bg_color)
        except:
            pass

    def on_button_click(self, event):
        '''click event - single_turn'''
        if not self.gui_board.check_winner():
            self.gui_board.single_turn(self.cord)
        


class GuiBoard(Board):
    '''this clas implimented from Board class, according this class, 
    build user interface to the game using gui, this class updates
    all moves in gui board and manage clicks, history view and hints of game'''
    MARKER = "⚫"
    def __init__(self, gui = False, firebase = False):
        super().__init__()
        self.master = None
        self.__buttons = {}
        self.temp_hint = []
        self.start = None
        self.loger_gui = None
        self.show_hint = False
        self.turn_history = 0
        self.plyer_label = None
        self.history_viewer = False
        self.online = firebase
        if gui:
            self.start_gui()

    def auto_mov(self):
        '''this functoion make auto move for computer player
        will be called after human turn or the begining of game'''
        start, end = self.make_ramdom_comp_move(self.get_player_turn())
        self.loger_gui.update_log_file(self.get_player_turn().get_id(), start, end)
        self.update_move_gui(start, end, self.get_player_turn())
        winner = self.check_winner()
        if not winner:
            self.turn_update()
        return winner
    
    def single_turn(self, selected_point):
        '''this function manage single turn'''
        if not self.history_viewer:
            winnner = self.check_winner()
            if self.get_player_turn().is_human() and not winnner:
                #human player - select the coordinates by clicking buttons
                if self.player_move(selected_point, self.get_player_turn()):
                    winnner = self.check_winner()
                    if not winnner:
                        self.turn_update()
            
            #run all the auto computers players after human turn
            while not self.get_player_turn().is_human() and not winnner:
                winnner = self.auto_mov()
            
            if winnner:
                self.show_victory_label()
            else:
                self.change_text(self.get_player_turn().get_name())

    def player_move(self, cord, player1: Player):
        '''this function manage human turn, saving last clicks and 
        make moves if its valid'''
        if self.playerid_in(*cord) == player1.get_id():
            #clicking on tool belongs to the player
            if not self.start:
                #first click in board
                if self.show_hint:
                    #show hint of the first click
                    self.temp_hint = self.hint_end_turn(player1, cord)
                    self.update_hint(self.temp_hint, True)
                    
                self.mark_coord(cord, True)
                self.start = cord

            elif cord == self.start:
                #second click on the same button
                if self.show_hint:
                    #close hint
                    self.update_hint(self.temp_hint, False)
                self.mark_coord(self.start, False)
                self.start = None

        elif self.start and self.start != cord:
            #second click - new coordinate (end)
            movs = self.make_move(player1, self.start, cord, False)
            if movs:
                #succes move done, updating board, log and gui
                if self.loger_gui:
                    self.loger_gui.update_log_file(
                        player1.get_id(), self.start, cord)

                if self.show_hint:
                    #close hint
                    self.update_hint(self.temp_hint, False)
                self.mark_coord(self.start, False)
                self.update_move_gui(self.start, cord, player1)
                self.start = None
            return movs

    
    def builder(self, loger = None, history = False):
        '''this function build the iterface gui board'''
        if not self.online:
            self.loger_gui = loger
        self.master = tk.Tk()
        self.master.title("Chinese Checkers local game")
        self.create_buttons(history)

    def change_text(self, text_label=""):
        '''this function change the text located at the top'''
        try:
            for widget in self.plyer_label.winfo_children():
                widget.destroy()

            datelabel = tk.Label(self.plyer_label, text=text_label)
            datelabel.pack(side=tk.BOTTOM)
            self.plyer_label.pack()
        except:
            pass

    
    def history(self, next=True):
        '''this function loading the last/next action turn and show on board'''
        all_moves = self.loger_gui.get_moves_from_log()
        player_dict = {pl.get_id():pl for pl in self.get_players_list()}
        if next and 1<len(all_moves):
            #update the next action in log
            if self.turn_history < len(all_moves) -1:
                self.turn_history += 1
                old_move = all_moves[self.turn_history]

                #gui update action
                self.update_move_gui(tuple(old_move[3:5]), 
                            tuple(old_move[5:]), player_dict.get(old_move[2]))
                self.change_text(f"{old_move[1]}, {player_dict.get(old_move[2]).get_name()}")
            else:
                messagebox.showinfo("end of view","you are in the end")
        elif 1<len(all_moves):
            #update the previes action in log
            if 0 < self.turn_history:
                self.turn_history -=1
                old_move = all_moves[self.turn_history]

                #gui update action
                self.update_move_gui(tuple(old_move[5:]),
                            tuple(old_move[3:5]), player_dict.get(old_move[2]))
                self.change_text(f"{old_move[1]}, {player_dict.get(old_move[2]).get_name()}")
            else:
                messagebox.showinfo("start of view","you are in the start")

    def autoplayers_first(self):
        '''this function for all the auto players at the begining game'''
        winnner = self.check_winner()
        while not self.get_player_turn().is_human() and not winnner:
            winnner = self.auto_mov()
        self.change_text(self.get_player_turn().get_name())

    def start_gui(self, loger = None, history = True):
        '''this function loading the game, gets loger'''
        self.builder(loger, history)
        self.history_viewer = history
        if not history:
            #just if loaded as history view show the next/back buttns
            self.change_text(self.get_player_turn().get_name())
            self.autoplayers_first()

        if self.check_winner():
            self.show_victory_label()
        
        self.master.mainloop()
    
    def __update_btn(self, x, y, color="#ffffff"):
        '''this function update style of one button after move'''
        self.__buttons[x][y].update_style(color)

    def update_move_gui(self, start, end ,player: Player):
        '''this functin gets start and end coordinates and
        updates the gui board according the move'''
        if self.valid_coord(*start) and self.valid_coord(*end):
            self.__update_btn(*start)
            self.__update_btn(*end, player.get_color_gui())
    
    def turn_hint(self):
        '''this function close/show hints. by call it the function
        show the hints of current selected coordinate or hide it'''
        self.show_hint = not self.show_hint
        if self.start:
            self.temp_hint = self.hint_end_turn(self.get_player_turn(), self.start)
            self.update_hint(self.temp_hint, self.show_hint)

    def show_victory_label(self):
        '''this function show the bottom victory label and updating the log file'''
        player = self.get_player_turn()
        if self.loger_gui and not self.history_viewer:
            self.loger_gui.update_winner_log(player.get_id())
        vic_label = tk.Label(self.master, text=f"{player.get_name()} won!", bg=player.get_color_gui())
        vic_label.pack(side=tk.TOP, pady=10)

    def create_buttons(self, history, online=False):
        '''this function create all buttons in the gui interface board'''
        if not online:
            #label for current turn player  
            self.plyer_label = tk.Frame(self.master)
            datelabel = tk.Label(self.plyer_label, text="game history" if history else "")
            datelabel.pack(side=tk.BOTTOM)
            self.plyer_label.pack()
        
        row = tk.Frame(self.master)
        row.pack()
        if history:
            #load the next/back buttons if history is on
            back_button = tk.Button(row, text="Back", 
                            command=lambda: self.history(False))
            back_button.pack(side=tk.LEFT)

            next_button = tk.Button(row, text="Next", 
                            command=lambda: self.history(True))
            next_button.pack(side=tk.LEFT)
            if not self.online:
                self.turn_history = len(self.loger_gui.get_moves_from_log())
        
        #build buttons board according to the board coordinate
        brd = self.get_board()
        for x in brd:
            row_frame = tk.Frame(self.master)
            row_frame.pack()
            for y in brd[x]:
                button = RoundButton(self, row_frame, radius=10, cor=(x,y))
                if brd[x][y]:
                    #update style if player tool inside the cell
                    button.update_style(bg_color=brd[x][y].get_color_gui())
                if self.__buttons.get(x):
                    self.__buttons[x][y] = button
                else:
                    self.__buttons[x] = {y: button}
                button.pack(side=tk.LEFT, padx=5, pady=5)
        
        if not history:
            #checkbox gor hint show
            checkbox = tk.Checkbutton(self.master, text="Show moves hint", 
                                command=lambda: self.turn_hint())
            checkbox.pack(side=tk.BOTTOM, pady=10)


    def valid_coord(self, x,y):
        '''this function check if the givven coordinate is valid'''
        return self.__buttons.get(x) and self.__buttons.get(x).get(y)
             
    def mark_coord(self, coord, marked):
        '''this function gets coordinate and remove/show mark point
        of selected start button'''
        x1,y1 = coord
        if self.valid_coord(x1,y1):
            btn = self.__buttons[x1][y1]
            if marked:
                btn.create_text(btn.radius, btn.radius, tags="text", 
                                text=GuiBoard.MARKER, fill="black")
            else:
                btn.delete_text()

    def mark_hint(self, coord, marked):
        '''this function gets coordinate and remove/show mark point
        of hint button of the selected button'''
        x1,y1 = coord
        if self.valid_coord(x1,y1):
            btn = self.__buttons[x1][y1]
            btn.update_style(outline_width = 3 * int(marked))     

    def update_hint(self, hint_list, marked):
        '''this function gets coordinate and remove/show all hints 
        of selected start button'''
        for coord in hint_list:
            self.mark_hint(coord, marked)
        self.temp_hint = hint_list if marked else []