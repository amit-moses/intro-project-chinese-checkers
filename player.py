
import file_colors
class Player:
    '''this class represent player and information about the player that
    esstansial to the game, in addition all the tools in the board
    will be represent as player object of this class. '''

    #emojy can be printed in cmd or therminal represents player tool in
    #textual game only
    COLORS = "🔴🟠🟡🟢🔵🟣🟤🍪🍩🏀🥎⚽🌍🌀🥝"
    COMPUTER = "🉐🉑🧿📀👽😈🤖"
    
    def __init__(self, name, color, id) -> None:
        self.__name = name
        self.__color = color
        self.__id = id
        self.__corner = 1

    def is_human(self):
        '''return if the players is human (id is positive) else its computer'''
        return 0 < self.__id
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def set_corner(self, cor):
        self.__corner = cor
    
    def get_home_cornner(self):
        return self.__corner 
    
    def get_color_id(self):
        return self.__color
    
    def __str__(self):
        #returns the str represent for the player to be printed in board
        return Player.COLORS[
            self.__color] if self.is_human() else Player.COMPUTER[self.__color]
    
    def get_color_gui(self):
        '''this function returns the current color to gui'''
        return file_colors.COLORS_CODE[
            self.__color] if self.is_human() else file_colors.COMP_COLORS[self.__color] 