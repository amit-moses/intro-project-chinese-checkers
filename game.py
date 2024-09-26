from gui_board import GuiBoard
from player import Player
from logs import MyLog

class Game:
    '''class for manging one game, connecting to loger - class that craete the log files
    text game in cmd with printing using emojys, load old games, '''
    ORDER = {2: (1,4), 3: (1,3,5), 4:(2,3,5,6), 6:(1,2,3,4,5,6)}
    FIRST_INFO = ["Press x,y .. for select tool to move (x – line, y-the location in line ltr (exmp. 0,0 is the head)",
                  "Press !  .... for stop the game"]
    SECOND_INFO = ["Press x,y .. for select tool target location", 
                   "Press 1 .... for hint all possible moves", 
                   "Press B .... for back to tool selection"]
    STOP_GAME ="!"
    BACK_STEP = "B"
    HINT = "1"
    def __init__(self, old_game = 0, show_result = True, gui = False) -> None:
        self.__board = GuiBoard() 
        self.__loger = None
        self.__gui = gui

        if old_game:
            self.load_old_game(old_game, show_result)
    
    def load_gui(self, history = False):
        '''this function loads the gui inteface for this game'''
        self.__gui = True
        if not self.__loger:
            self.__loger = MyLog([pl.get_id() for pl in self.__board.get_players_list()])
        self.__board.start_gui(self.__loger, history)
    
    def add_players(self, players_list):
        '''this function add the players to the board'''
        self.__board.set_players_in_board(players_list)

    def underline(self, text):
        '''underline text in therminal/cmd'''
        return '\033[4m' + text + '\033[0m'
    
    def winner_print(self, player):
        '''print winner with border of *'''
        player_won_name = player.get_name()
        print("*"*(len(player_won_name) + 9),  
              "* " + player_won_name + " won! *", 
              "*"*(len(player_won_name) + 9), sep="\n")
    
    def is_game_ended(self):
        '''check if the game ended'''
        try:
            return self.__board.check_winner()
        except:
            return False


    def load_old_game(self, game_id, show = False):
        '''this function gets id of old_game and load it. 
        can start to play from this point'''
        self.__loger = MyLog(id=game_id)
        self.__board.set_players_in_board(
            self.__loger.get_players_from_log(), False)

        #make dict of all players in the game
        player_dict = {pl.get_id():pl 
                       for pl in self.__board.get_players_list()}

        #load old movs from lof dile and update the game to the last move
        try:
            for old_move in self.__loger.get_moves_from_log():
                if show and not self.__gui:
                    print(self.__board)
                player1 = player_dict.get(old_move[2])
                if show and not self.__gui:
                    print(old_move[1], self.underline(player1.get_name()))
                mov = self.__board.make_move(player1, 
                                tuple(old_move[3:5]), tuple(old_move[5:]), False)
                if not player1.is_human() and mov:
                    self.__board.update_comp_coord(player1, *mov)
                if not self.__board.check_winner():
                    self.__board.turn_update()
        except:
            pass

        if show and not self.__gui:
            print(self.__board)
        if self.__board.check_winner() and show and not self.__gui:
            self.winner_print(self.__board.get_player_turn())


    def check_valid_input(self, chose, player, is_start):
        '''check validation of input'''
        try:
            my_select = chose.split(",")
            if len(my_select) != 2:
                return None
            coord = int(my_select[0]), int(my_select[1])
            if is_start:
                if self.__board.check_start(player, coord):
                    return coord
            else:
                if self.__board.check_end(coord):
                    return coord
        except:
            return None
    
    def start_select(self, player):
        '''selext the start of the move'''
        if not self.__gui:
            print(*Game.FIRST_INFO, sep="\n")
        while True:
            player_chose = input("your choose: ")
            if player_chose == Game.STOP_GAME:
                return False
            coords = self.check_valid_input(player_chose, player, True)
            if coords:
                return coords
            if not self.__gui:
                print("error value, please try again")

    def end_select_and_move(self, start, player):
        '''select the end of the move'''
        if not self.__gui:
            print(*Game.SECOND_INFO, sep="\n")
        while True:
            player_chose = input("your choose: ")
            if player_chose == Game.BACK_STEP:
                return False
            if player_chose == Game.HINT:
                if not self.__gui:
                    print(self.__board.get_hint(player, start))
                continue
            end = self.check_valid_input(player_chose, player, False)
            if end:
                mov = self.__board.make_move(player, start, end)
                if mov:
                    return mov
            if not self.__gui:
                print("error value, please try again")

    def singale_turn(self, player:Player):
        '''singale turn manage'''
        if not self.__gui:
            print(self.underline(player.get_name()))
        if player.is_human():
            while True:
                start = self.start_select(player)
                if start:
                    mov = self.end_select_and_move(start, player)
                    if mov:
                        self.__loger.update_log_file(player.get_id(), *mov)
                        return True
                else:
                    return False
        else:
            mov = self.__board.make_ramdom_comp_move(player) 
            if mov:
                self.__loger.update_log_file(player.get_id(), *mov)
                return True      
        return False

    def start_play(self):  
        '''start play, if this is old game, the game will 
        be start from where it stopped'''
        if not self.__loger:
            self.__loger = MyLog([pl.get_id() for pl in self.__board.get_players_list()])
        has_winner = False
        while not has_winner:
            if not self.__gui:
                print(self.__board)
            if self.singale_turn(self.__board.get_player_turn()):
                has_winner = self.__board.check_winner()
                if not has_winner:
                    self.__board.turn_update()
            else:
                break
        if not self.__gui:
            print(self.__board)

        if has_winner:
            winner = self.__board.get_player_turn()
            self.winner_print(winner)
            self.__loger.update_winner_log(winner.get_id())
            return True
        elif not self.__gui:
            print("game in pause. you can come back by loading log of game id:", self.__loger.get_id())