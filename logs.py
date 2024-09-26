import file_utils
from player import Player
from datetime import datetime

class MyLog():
    '''this class manage the saved data about the players and game while 
    it active or restored. saving data each turn'''

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    GAME_INDEX_FILE = "game_files/game_index.pkl"
    LOGS_START = "game_files/log_game"
    LOGS_END = ".txt"

    def __init__(self, player_list=[], id=0) -> None:
        all_games = file_utils.get_dict_from_pickle(MyLog.GAME_INDEX_FILE)
        if not id:
            self.__gameid = len(all_games) + 1
            self.__playersid= player_list
            self.__wins = False
            self.__all_moves = []
            all_games[self.__gameid] = player_list , self.__wins
            file_utils.save_dict_to_pickle(all_games, MyLog.GAME_INDEX_FILE)

        elif all_games.get(id):
            self.__wins = all_games[id][1] is not False
            self.__gameid = id
            self.__playersid = all_games[id][0]
            self.__all_moves = file_utils.get_lines_from_file(
                self.get_log_path())
    
    def get_id(self):
        '''this function return id of the game'''
        return self.__gameid
    
    def get_players_from_log(self):
        '''this function returns the list of the players in the game'''
        try:
            return file_utils.get_players_from_list(self.__playersid)
        except:
            return []
    
    def get_log_path(self):
        '''this function returns the path of the log file of the game'''
        return MyLog.LOGS_START+str(self.__gameid)+MyLog.LOGS_END
    
    def get_moves_from_log(self):
        '''this function return list of all the moves have done in the game'''
        return self.__all_moves
    

    def update_index(self):
        ''''this function updates the data of the game in files'''
        all_games = file_utils.get_dict_from_pickle(MyLog.GAME_INDEX_FILE)
        all_games[self.__gameid] = self.__playersid, self.__wins
        file_utils.save_dict_to_pickle(all_games, MyLog.GAME_INDEX_FILE)

    def update_log_file(self, playerid, start, end):
        '''this function gets 2 coordinates ande player, updates the move 
        that the player did in log file'''
        formatted_time = datetime.now().strftime(MyLog.TIME_FORMAT)
        x1,y1 = start
        x2,y2 = end
        path = self.get_log_path()
        file_utils.add_line_to_file(path, 
            f"{self.__gameid},{formatted_time},{playerid},{x1},{y1},{x2},{y2}\n")

    def delete_player(self, id):
        '''this function deletes players by givven the id of the player'''
        if id in self.__playersid:
            self.__playersid.remove(id)
            self.update_index()
    
    def update_winner_log(self, player_id):
        '''this function updating the data of the game, updating the winner
          and save it in file'''
        if not self.__wins:
            self.__wins = player_id
            self.update_index()
            file_utils.update_winner_and_loses(player_id, self.__playersid)