import pickle
from player import Player
import os

PLAYERS_FILE = "game_files/players.pkl"
LOGS_START = "game_files/log_game"
GAMES_FILE = "game_files/game_index.pkl"
LOGS_END = ".txt"

def get_dict_from_pickle(file_name):
    '''this function get name of pickle file and return 
    a dictionary from a pickle file.'''
    try:
        with open(file_name, 'rb') as pickle_file:
            return pickle.load(pickle_file)
    except:
         return {}

def save_dict_to_pickle(my_dict, file_name):
    '''this dunction get dict and file name, and Saves it to pickle file.'''
    with open(file_name, 'wb') as f:
            pickle.dump(my_dict, f)

def isint(text):
    '''this function checks if givven string is number'''
    try:
        int(text)
        return True
    except:
        return False
    
def line_to_data(data):
    '''this function spliting line in txt file to list with int and strings'''
    return [int(k) if isint(k) else k for k in data.split(",")]

def get_lines_from_file(file_name):
    '''this function get file name and reads lines from a file.
    returns list of all lines without break line'''
    try:
        with open(file_name, "r") as f:
            #replace break down in empty char in the list
            return [line_to_data(line.replace("\n","")) for line in f.readlines()]
    except:
        return []
    
def add_line_to_file(file_name, line):
    '''this function add line to text file'''
    with open(file_name, 'a') as file:
        # Add a line of text to the end of the file
        file.write(line)

def get_players_from_list(playerlist):
    '''this function gets list of players id and returns list
    of players object matched to th egivven data'''
    players = get_dict_from_pickle(PLAYERS_FILE)
    rtn = []
    for pl in playerlist:
        if 0 < pl:
            rtn.append(Player(*players[pl][:2], pl))
        else:
            rtn.append(Player(F"computer{-1*pl}", max(0,-1*pl), pl))
    return rtn

def update_winner_and_loses(winner_id, player_list):
    '''this function gets list of players id and id of winner
    updating for every one the score'''
    all_players = get_dict_from_pickle(PLAYERS_FILE)
    for pl in player_list:
        if all_players.get(pl):
            #wins in the 2th in the list. loses in the 3th in list
            all_players[pl][3 - int(pl == winner_id)] +=1
    save_dict_to_pickle(all_players, PLAYERS_FILE)

def remove_all_games():
    '''this function remove all games history and deletes all log
    files and games data that exist'''
    all_games = get_dict_from_pickle(GAMES_FILE)
    for game in all_games:
        path = LOGS_START + str(game) + LOGS_END
        if os.path.exists(path):
            # Remove the file
            os.remove(path)
    save_dict_to_pickle({}, GAMES_FILE)

def remove_all_players():
    '''this function remove all players data from the saved
    data file'''
    save_dict_to_pickle({}, PLAYERS_FILE)