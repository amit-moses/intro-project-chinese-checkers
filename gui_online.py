import tkinter as tk
from gui_board import GuiBoard
from player import Player

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import file_utils

GAMERS_TABLE = "games"
DB_CONFIG_JSON = 'game_files/config_firebase.json'

class FireBoard(GuiBoard):
    '''this class impliment from the GuiBoard and connected 
    to firebase service - firestore which allow to retrive data 
    in real time, this class manage the connection to the database 
    and update the moves while listiner to other player moves'''

    def __init__(self, mydb, player: Player, gui=False):
        super().__init__(gui)
        self.db = mydb
        self.server_listiner = None

        self.master = tk.Tk()
        self.plyer_label = tk.Frame(self.master)

        self.my_turn = False

        #determinate the following id
        self.gamer_id_server = self.get_last_player_id(GAMERS_TABLE) + 1
        self.gamer_other_id = 0
        self.other_gamer_in =False
        
        self.gamer =  player

        #select other color for other
        optional_colors = set(range(6)) - {player.get_color_id()}
        self.other_player = Player("other", random.choice(
            list(optional_colors)), player.get_id() + 1)
        self.insert_player_to_game()
    
    def turn_update(self):
        '''this function update the turn after move, override the original'''
        self.set_turn(not self.my_turn)

    def get_player_turn(self):
        '''this function get the curren turn player'''
        return self.gamer if self.my_turn else self.other_player
    
    def set_title(self):
        '''this function update the label at the top of window'''
        if self.other_gamer_in:
            change_to = "your turn" if self.get_player_turn() == self.gamer else "other turn"
        else:
            change_to = "waiting for other..."

        self.change_text(change_to)

    def insert_player_to_game(self):
        '''this function upload the player to the firebase database'''
        doc_ref = self.db.collection(
            GAMERS_TABLE).document(str(self.gamer_id_server))
        
        #the first in the game will wating to other and will be the first
        order = bool(self.gamer_id_server % 2)
        doc_ref.set({"id": self.gamer_id_server})
        self.set_turn(order)

        #the player game with other gamer with close in 1 to its id
        if self.gamer_id_server%2:
            #enter first
            self.gamer_other_id = self.gamer_id_server + 1
        else:
            #enter second
            self.gamer_other_id = self.gamer_id_server - 1

        #update players in the board - by the order of entry
        self.set_players_in_board([self.gamer, 
                                   self.other_player] if order else [
                                       self.other_player, self.gamer], False)

    
    def get_last_player_id(self, collection_name):
        '''this function conecting to firebase database and get the
        number id of the last player in the game'''
        collection_ref = self.db.collection(collection_name)
        query = collection_ref.order_by("id", direction=firestore.Query.DESCENDING).limit(1)
        docs = query.get()
        if len(docs):
            return docs[0].to_dict().get("id")
        else: return 0

    def update_moves_in_db(self, start, end):
        '''this function gets valid moves (start, end) and
        updating the move in firebase database - after updating
        will be ping the other player'''
        self.set_title() #updateing the label of game player turn
        doc_ref = self.db.collection(
            GAMERS_TABLE).document(str(self.gamer_id_server))
        
        #add the last move to database
        doc_ref.set({"start": start, "end":end, "id": self.gamer_id_server})

    def set_other_loged(self):
        '''this function upadate the second players in the game 
        after wating and first ping'''
        self.other_gamer_in = True
        self.set_title()

    def single_turn(self, selected_point):
        '''this function manage singale turn of current player, 
        override the original matched for online game'''
        if self.my_turn and self.other_gamer_in:
            movs = self.player_move(selected_point, self.gamer)
            if movs:
                self.update_moves_in_db(*movs)
                self.set_turn(False)
    

    def update_move_ping(self, start, end):
        '''this function update the other player move in the current board'''
        try:
            self.other_gamer_in = True
            self.update_moves_ater_check(start, end, self.other_player)
            self.update_move_gui(start, end, self.other_player)
            self.set_turn(True)
        except:
            pass

    def set_turn(self, tr=True):
        '''this function update the turn to the givven value'''
        if self.check_winner():
            #game finished - show winner
            self.show_victory_label()
            self.change_text("game ended")
            try:
                #updating the current player game result in the file
                file_utils.update_winner_and_loses(
                    self.get_player_turn().get_id(), [self.gamer.get_id()])
            except:
                pass
        else:
            self.my_turn = tr
            self.set_title()
    
    def get_other_id(self):
        '''this function returns the other player id'''
        return self.gamer_other_id
    
    def exit_before_other_loged_in(self):
        '''exit from window - remove the player from database'''
        try:
            doc_ref = self.db.collection(GAMERS_TABLE).document(str(self.gamer_id_server))
            # Delete player
            doc_ref.delete()
        except:
            pass
        self.master.destroy()

    def builder(self):
        '''this function build gui board, override the original'''
        self.master.title("Online Chinese Checker")
        self.create_buttons(False, True)
        self.set_title()
        self.master.protocol("WM_DELETE_WINDOW", self.exit_before_other_loged_in)
        self.master.mainloop()


class GameOnline:
    cred = credentials.Certificate(DB_CONFIG_JSON)
    app = firebase_admin.initialize_app(cred)
    def __init__(self, player) -> None:
        '''this function determinate the current player'''
        self.__player_gamer = player

    def start_game_online(self):
        '''this function genereates new online game, build 
        connection to firebase and use FireBoard class to manage it'''
        # Use a service account.
        db = firestore.client()
        fbd = FireBoard(db,self.__player_gamer)

        # listiner for query - other players. listiner when move will be done 
        games_collection = db.collection(
            GAMERS_TABLE).document(str(fbd.get_other_id()))

        # Define the callback function for the listener
        def on_snapshot(doc_snapshot, changes, read_time):
            if doc_snapshot:
                fbd.set_other_loged()
                doc = doc_snapshot[0].to_dict()
                start, end = doc.get("start") , doc.get("end")
                if start and end:
                    fbd.update_move_ping(start, end)

        # Set up the listener
        games_collection.on_snapshot(on_snapshot)
        fbd.builder()
        # Keep the script running by keep open the gui window