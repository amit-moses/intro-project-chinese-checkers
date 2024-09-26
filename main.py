#################################################################
# FILE : main.py
# WRITER : Amit Moses , amit.moses1
# EXERCISE : intro2cs final project
#################################################################

#the project has data for example run 'python main.py clear-all' to clear it


import sys
import game_utils 
from gui_main import MainGui
import file_utils

INSTRUCTION = ["run 'python main.py' - for using gui interface game",
               "run 'python main.py text' - for runing textual game ",
               "run 'python main.py clear-games' - for clear all games history",
               "run 'python main.py clear-all' - for clear games and players data",
               "run 'python main.py --help' for help menu"]

if __name__ == "__main__":
    if 1 < len(sys.argv) and sys.argv[1] == "text":
        game_utils.main_text()
    elif 1 < len(sys.argv) and sys.argv[1] == "--help":
        print(*INSTRUCTION, sep="\n")
    elif 1 < len(sys.argv) and sys.argv[1] == "clear-all":
        file_utils.remove_all_games()
        file_utils.remove_all_players()
        print("all data removed")
    elif 1 < len(sys.argv) and sys.argv[1] == "clear-games":
        file_utils.remove_all_games()
        print("all games removed")

    else:
        app = MainGui()
        app.mainloop()

