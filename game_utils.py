#this file manage the game in the therminal/cmd board without gui

from player import Player
from game import Game
from file_utils import get_dict_from_pickle, save_dict_to_pickle, isint
import random


VALID_PLAYERS = [2,3,4,6]
COMPUTER = ["computer", -1, "", ""]
PLAYERS_FILE = "game_files/players.pkl"
GAMES_FILE = "game_files/game_index.pkl"
BACK_M = "press B for back"
BACK_CHAR = "B"
ADD_CHAR = "A"
SELRCT_CHAR = "V"
ACT1 = ["Press the id number to select player to edit",
        "Press A for add a new player"]

def underline(text):
    '''this function gets text and returns it with underline'''
    return '\033[4m' + text + '\033[0m'

def game_show(id, game_info ,players):
    '''this function returns game info with the players (row)'''
    names = ""
    for pl in game_info[0]:
        #add the name of player if id is <0 is not human
        to_add = players[pl][0] if 0 < pl and players.get(pl) else f"computer{-1*pl}"
        spacing = (12-len(to_add))*" "
        if pl == game_info[1]:
            #undeline winner name
            to_add = underline(to_add)
        names += to_add + spacing
    status = "(ended) " if game_info[1] else "(stoped)"
    return f"{id}. {status}  players: {names}"

def player_show(id, player):
    '''this function returns player info with number of wins and loses'''
    vics_lose = str(player[2]).center(5) + str(player[3]).center(5) 
    symbol = Player.COLORS[player[1]] if id else "🖥️ "
    return str(id)+". "+ symbol + (3-int(id)//10)*" " +player[0] + (12-len(player[0]))*" " + vics_lose

def select_act(all_players):
    '''this function wating for user response to add new player or edit details'''
    if len(all_players):
        print(ACT1[0])
    if len(all_players) < 15:
        print(ACT1[1])
    print(BACK_M)
    while True:
        act = input("your select: ")
        if act in [BACK_CHAR, ADD_CHAR]:
            #valid answer back or add new player
            return act
        if all_players.get(act):
            #valid answer edit player
            return act
        if len(all_players):
            if isint(act):
                if 0 < int(act) < len(all_players)+1:
                    add_edit_player(all_players, int(act))
                    return True
                else:
                    print("player not found, please insert valid input")
            else:
                print("not valid input")
    
def insert_name(all_players , id):
    '''check validation of new name'''
    print(underline("plaese select new name"))
    print(BACK_M)

    #all name except the original player for edit
    all_names = [all_players[pl][0] for pl in all_players if pl != id]
    while True:
        select = input("your select: ")
        if select == BACK_CHAR:
            return False
        elif not 3 < len(select) < 11:
            print("player name should be 3-10 chars!")
        elif select in all_names:
            print("this name is already taken by other player!")
        else:
            return select

def select_color(all_players, id = 0):
    '''check validation of new color'''
    #get all colors except the user for editing
    all_colors = [all_players[pl][1] for pl in all_players if pl != id]
    for col in range(len(Player.COLORS)):
        if not col in all_colors:
            print("press", str(col), "for", Player.COLORS[col])
    print(underline("please select color from the list"))
    print(BACK_M)
    while True:
        select = input("your select: ")
        if select == BACK_CHAR:
            return BACK_CHAR
        if isint(select):
            if not int(select) in all_colors:
                #color id valid
                return int(select)
        
        
def add_edit_player(all_players, id = 0):
    '''this function manage add or edit new player'''
    if id:
        #print selected player if is edit id not 0
        print(player_show(id, all_players[id]))
    while True:
        #check new name validation
        new_name = insert_name(all_players, id)
        if new_name:
            #check new color validation
            new_color = select_color(all_players, id)
            if new_color != BACK_CHAR:
                if id:
                    #edit
                    all_players[id][0] = new_name
                    all_players[id][1] = new_color
                else:
                    #add
                    all_players[len(all_players) + 1] = [new_name, new_color, 0,0]
                save_dict_to_pickle(all_players, PLAYERS_FILE)
                return True
            else:
                return False
        else:
            return False

def player_list():
    '''this function prints the list of player details, returns after list of
    all players'''
    all_players = get_dict_from_pickle(PLAYERS_FILE)
    for pl in all_players:
        #row for each players of the player details 
        print(player_show(pl, all_players[pl]))
    return all_players

def player_manage():
    '''this function manage edit players details (add/edit)'''
    while True:
        #get the players list after print thier details
        all_players = player_list()
        #check valid of selected act
        act1 = select_act(all_players)
        if act1 == BACK_CHAR:
            return False
        else:
            if act1== ADD_CHAR:
                add_edit_player(all_players)


def all_players_in_list(pl_set, all_players):
    '''check validation of selected player to play with'''
    for pl in pl_set:
        if isint(pl):
            if int(pl) and 1 < pl_set.count(pl):
                #check amount of players
                return False
            if not int(pl) in all_players and int(pl):
                #check valid of humans player
                return False
        else:
            return False
    return True

def print_instruction():
    '''print instruction for how to select the players for one game'''
    print(underline("select players to play"))
    print(player_show(0, COMPUTER))
    all_players = player_list()
    print("select 2/3/4/6 players by press the id")
    print("every player can be selected ONE except computer")
    print("please insert the players ('0,0,2,3' will be game with 2 computers and players 2 and 3)")
    print(BACK_M)
    return all_players

def select_player_to_play():
    '''this functuion wating for user response to select players to play with'''
    while True:
        #select players by id - 0 is computers
        all_players = print_instruction()
        text = input("your select: ")
        if text == BACK_CHAR:
            return BACK_CHAR
        players_id = list(text.split(","))
        #check validation of amount
        if len(players_id) in VALID_PLAYERS:
            #check validation of the inserted id
            if all_players_in_list(players_id, all_players):
                players = [(int(k), all_players[int(k)] if int(k) else COMPUTER) for k in players_id]
                print(underline("selected players:"))
                for k in players:
                    #print all selected players to the game
                    print(player_show(k[0], k[1]))
                return players
        else:
            print("select 2/3/4/6 players")


def final_players():
    '''this function wating for user response to approve selected players'''
    while True:
        #select the players
        players = select_player_to_play()
        if players != BACK_CHAR:
            print("insert V to start the game with the players")
            print(BACK_M)
            text = input("your select (V/B): ")
            while text not in ["B", SELRCT_CHAR]:
                print("not valid input")
                text = input("your select (V/B): ")
            if text == SELRCT_CHAR:
                #user select to start the game
                return players
            elif text == BACK_CHAR:
                return BACK_CHAR
        else:
            return BACK_CHAR


def get_game(players):
    '''this function create new game object'''
    new_game = Game()
    total_players = []

    #list of symboles to computers
    comp_symbole = set(range(len(Player.COMPUTER)))
    comp_id = 0
    for k in players:
        if k[0]:
            #id not 0 is human player, add the players list
            total_players.append(Player(*k[1][:2], k[0]))
        else:
            #add computer player
            comp_id -=1
            color = random.choice(list(comp_symbole))
            comp_symbole -= {color}
            total_players.append(Player(f"computer{-1*comp_id}" ,color, comp_id))
    new_game.add_players(total_players)
    return new_game

def new_game_manage(players= None, game=None):
    '''this function start a new game with selected playeres
    the function can get players list to play again with the same players
    the dunction can get old game to start drom the stop point'''
    if not players:
        #select players for new game
        players = final_players()
    while True:
        if players == BACK_CHAR:
            return BACK_CHAR
        elif players:
            if game:
                #start from the end point of the game
                game.start_play()
            else:
                #start new game
                get_game(players).start_play()
            print("press 1 for new game with new players")
            print("press 2 for new game with same players")
            print(BACK_M)
            text = input("your select: ")
            while text not in ["1", "2", BACK_CHAR]:
                print("not valid input")
                text = input("your select: ")
            if text == BACK_CHAR:
                return BACK_CHAR
            elif text == "1":
                #new game with ne players - select new players
                players = final_players()

def print_games(games, players):
    '''this function prints all game history and details of games'''
    for gm in games:
        #each game is row
        print(game_show(gm, games[gm], players))

def game_select(games, players):
    '''select game id for restore old game'''
    print("history of games")
    print_games(games, players)
    print("select game by insert id")
    print(BACK_M)
    text = input("your select: ")
    while True:
        if text == BACK_CHAR:
            return False
        if isint(text):
            #check if the selected id is valid game
            if int(text) in games:
                return int(text)
        print("not valid input")
        text = input("your select: ")

def history_manage():
    '''this function restore old game'''
    games = get_dict_from_pickle(GAMES_FILE)
    players =  get_dict_from_pickle(PLAYERS_FILE)
    while True:
        #select the valid id of game to restore
        ga = game_select(games, players)
        if ga:
            #new game object for selected old game, restores moves
            old_game = Game(ga, True, False)
            if not old_game.is_game_ended():
                #if the game not ended continue it if user want to
                print("press V for keep playing, press anything else for back")
                text = input("your select: ")
                if text == SELRCT_CHAR:
                    new_game_manage(games[ga][0], old_game)
        else:
            return False

def main_text():
    '''main menu of textual game'''
    while True:
        print("press 1 ... for new game", 
              "press 2 ... for games history", 
              "press 3 ... for player manager",
              "press B ... for exit", sep="\n")
        select = input("your select: ")
        if select == "1":
            new_game_manage()
        elif select == "2":
            history_manage()
        elif select == "3":
            player_manage()
        elif select == "B":
            return True
        else:
            print("please insert valid input")