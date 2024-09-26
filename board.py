from player import Player
import random

class Board:
    '''this class manage the board. saving all coordinates, players, 
    and computer coordinates,manage the turn devision, checking moves 
    and make random moves for computers'''
    
    EMPTY = "⚪"
    HINT = "🔘"
    KODKODS = {1:(8,-4), 2:(4,4), 3:(-4,8), 4:(-8,4), 5:(-4,-4), 6:(4,-8)}
    ORDER = {2: (1,4), 3: (1,3,5), 4:(2,3,5,6), 6:(1,2,3,4,5,6)}
    NEIGHBOORS = [(0, -1), (0,  1), (1,  0), (-1,  0), (1,  -1), (-1,  1)]

    def __init__(self) -> None:
        self.__cordinates = {}
        self.__board = {}
        self.__computer_coords = {}
        self.__playerslist = []
        self.__turn = 0
        
        #create the board
        #for each line in the star 
        #the middle of the star will be (0,0)
        for m in range(4):
            self.__board[8-m] = {-4+t: 0 for t in range(m+1)}
        for m in range(4):
            self.__board[4-m] = {t-8: 0 for t in range(m,13)}
        for m in range(5):
            self.__board[0-m] = {-4+t: 0 for t in range(9+m)}
        for m in range(4):
            self.__board[-5 - m] = {t+1: 0 for t in range(m,4)}

        #saving all the triangles
        self.set_edges()

    def get_board(self):
        '''this function returns the board's dictionery'''
        return self.__board
    
    def get_players_list(self):
        '''this function returns list of all the players by order the turns'''
        return self.__playerslist
    
    def get_player_turn(self):
        '''this function return the current player is game now'''
        return self.__playerslist[max(0, self.__turn)]
    
    def turn_update(self):
        '''this function change the current turn to next one'''
        self.__turn = (self.__turn + 1) % len(self.__playerslist)

    def get_turn_num(self):
        '''this function return the current index of player is its turn'''
        return self.__turn
    
    def set_edges(self):
        '''this function save coordinates of start position triangle corner'''
        for x in self.__board:
            for y in self.__board.get(x):
                cor = self.get_area(x , y)
                if  cor:
                    if self.__cordinates.get(cor):
                        self.__cordinates[cor].add((x , y))
                    else:
                        self.__cordinates[cor] = {(x , y)}

    def set_players_in_board(self, player_list, splash = True):
        '''this function gets players list and insert to board'''
        self.__playerslist = player_list[:]
        if splash:
            #make random order for turn playing
            random.shuffle(self.__playerslist)
        oedering = Board.ORDER[len(self.__playerslist)]

        #updating the corner of player 
        for pl in range(len(self.__playerslist)):
            self.__playerslist[pl].set_corner(oedering[pl])

        for pl in self.__playerslist:
            #save all auto players coordinates tools
            pl_home = pl.get_home_cornner()
            if not pl.is_human():
                coord = self.__cordinates.get(pl_home)
                if coord:
                    self.__computer_coords[pl_home] = coord.copy()

            #put tools of players in corner
            for point in self.__cordinates[pl_home]:
                self.__setvalue(*point, pl)
    
    def check_is_winner(self, player):
        '''this function check if the givven player is won'''
        target = self.get_target_side(player.get_home_cornner())

        #checking all target coordinates for determinate if all tools in
        for cor in self.__cordinates.get(target):
            if self.get_value_in_board(*cor) != player:
                return False
        return True
    
    def check_winner(self):
        '''this function check if the curent player is won'''
        return self.check_is_winner(self.get_player_turn())
    
    def in_edge(self, player: Player, home= False):
        '''this function gets player and return all the coordinates of
        tools contain in target triangle or home triangle'''
        fromhome = player.get_home_cornner()
        target = fromhome if home else self.get_target_side(fromhome)
        total = set()

        #checking if coordinate contain the player tool
        for cor in self.__cordinates.get(target):
            if self.get_value_in_board(*cor) == player:
                total.add(cor)
        return total
    
    def playerid_in(self, x,  y):
        '''this function returns the id of current player in specific cell'''
        if self.__in_range_check_inside(x,y, True):
            return self.__board[x][y].get_id()
    
    def __in_range(self, x,y):
        '''this functin checks if the coordinate (x,y) in board'''
        return self.__board.get(x) is not None and self.__board[x].get(y) is not None
        
    def __in_range_check_inside(self, x,y, taken):
        '''this functin checks if the coordinate (x,y) and if player inside'''
        return self.__in_range(x,y) and bool(self.__board[x][y]) == taken
        
    def __setvalue(self, x,y, value):
        '''this function get coordinate and change its value in board'''
        if self.__in_range(x,y):
            self.__board[x][y] = value
    
    def get_neighboors(self, x, y, is_empty):
        '''this function get coordinate, returns set with all the cell around'''
        return [(x+dx, y+dy) for dx, dy in Board.NEIGHBOORS 
                if self.__in_range_check_inside(x+dx, y+dy, is_empty)]
    
    def parser_from_reg(self, x, y):
        '''this function gets regular coordinate (0,0) the top for exanple
        and transfer to the board coordinate'''
        if self.__board.get(8-x):
            return (8-x, y+min(self.__board[8-x]))
            
    def get_area(self, x, y):
        '''this function gets coordinate and return the serial number
        of the area the coordinate in, 0 if netral'''
        if 5 <= x <= 8:
            return 1
        elif 5 <= y <= 8:
            return 3
        elif -8 <= x <= -5:
            return 4
        elif -8 <= y <= -5:
            return 6
        elif 1 <= x <= 4 and 5 <= x+y <= 8 and 1 <= y <= 4:
            return 2
        elif -4 <= x <= -1 and -8 <= x+y <= -5 and -4 <= y <=-1:
            return 5
        return 0
    
    def get_target_side(self, home):
        '''this function gets serial number of triangle and returns
        the serial number infront of the givven number'''
        if home ==3:
            return 6
        return (home +3)%6 if 0 < home <=6 else 0
    
    def delete_player(self, player):
        '''this function delete player from all board'''
        for x in self.__board:
            for y in self.__board.get(x):
                if self.get_value_in_board(x,y) == player:
                    self.__setvalue(x,y, 0)
        
    def get_value_in_board(self, x, y):
        '''this function gets coordinate, returns the value in'''
        return self.__board[x][y]
    
    def get_empty_cells_of_neighboors(self, start):
        '''this function get coordinate, returns all the empty cell
        around all each one of neighboor's of givven coordinate'''
        valid_moves = set()
        for neig in self.get_neighboors(*start, True):
            for target in self.get_neighboors(*neig, False):
                if target != start:
                    valid_moves.add(target)
        return valid_moves
                
    def valid_one_move(self, start, player):
        '''this function gets, player and cell, returns all the 
        possible one step moving around the cell, cannot enter
        to other home wich not its target, cannot player's home '''
        valid_moves = set()
        player_home = player.get_home_cornner() 
        player_des = self.get_target_side(player_home) 
        start_area = self.get_area(*start) 
        is_start_in_des = player_des == start_area
        for neig in self.get_neighboors(*start, False):
            cell_area = self.get_area(*neig)
            if is_start_in_des:
                #the tool cannot moving out when located in target triangle
                if cell_area == player_des:
                    valid_moves.add(neig)

            elif cell_area == player_home:
                #the tool cannot moving back to player's home
                if start_area == cell_area:
                    valid_moves.add(neig)
            else:
                valid_moves.add(neig) 
        return valid_moves
    
    def add_valid_move(self, valid, player: Player):
        '''this function returns all the valid moves of specific
        tool around in game - if tool can skip othe tool can move
        to all empty cell the skipped tool'''
        all_for_valids = {valid}
        for neig in self.get_neighboors(*valid, True):
            if self.get_area(*neig) != player.get_home_cornner():
                empties = self.get_neighboors(*neig, False)
                if 1 < len(empties):
                    #add only if 2 cells empty around the tool
                    for empty in  empties:
                        all_for_valids.add(empty)
        return all_for_valids
    
    def valid_all_moves(self, player: Player, start):
        '''this function gets player and coordinate, returns the
        all possible moving for one step skiping from the coordinate'''
        valid_moves = set()
        empty_cell_around = self.get_neighboors(*start, False) 
        player_home = player.get_home_cornner() 
        player_des = self.get_target_side(player_home) 
        start_area = self.get_area(*start) 
        is_start_in_des = player_des == start_area 
        for cell in self.get_empty_cells_of_neighboors(start):
            if cell not in empty_cell_around:
                cell_area = self.get_area(*cell)
                is_foreign_target = cell_area not in [0, player_des]
                if is_start_in_des:
                    #the tool cannot moving out when located in target triangle
                    if cell_area == start_area:
                        valid_moves.update(self.add_valid_move(cell, player))

                elif is_foreign_target or player_home == cell_area:
                    #the tool can move as free in its home
                    if player_home == cell_area:
                        if start_area == cell_area:
                            valid_moves.update(self.add_valid_move(cell, player))

                    #the tool can enter ot not its target or its home back just
                    #for skiping other tools inside
                    for valid in self.get_empty_cells_of_neighboors(cell):
                        cell_valid =self.get_area(*valid)
                        if player_home == cell_area !=  cell_valid or cell_valid != cell_area:
                            valid_moves.update(self.add_valid_move(cell, player))
                else:
                    valid_moves.update(self.add_valid_move(cell, player))

        return valid_moves
    
    def more_valids_of_valid(self, player, new_valids):
        '''this function get valids coordinates moving and return 
        all coordinates the player can move in two steps moving from
        all the coordinates'''
        new_set = new_valids.copy()
        for valid in new_valids:
            new_set.update(self.valid_all_moves(player, valid))
        return new_set
    
    def get_all_valid_end_turn_helper(self, player: Player, start, myset):
        '''this function gets player, and start position of move
        return all the possible move with k-th steps by skiping others tools'''
        extend = self.more_valids_of_valid(
            player, self.valid_all_moves(player, start))
        keep = extend.issubset(myset)
        myset.update(extend)
        if keep:
            #recursaion will be stopped if there is no more valid moves to add
            myset.update(self.more_valids_of_valid(player, myset))
            return myset
        
        #for each possible new move call for this function with new position
        for new_start in extend:
            return self.get_all_valid_end_turn_helper(player, new_start, myset)
    
    def hint_end_turn(self, player: Player, start):
        '''this function returns all the possible moves the player
        can finish in one move. around and skiping'''
        #remove the player temporal from the board
        self.__setvalue(*start, 0)

        #add all skiping possible moves
        rtn = self.more_valids_of_valid(player, 
                self.get_all_valid_end_turn_helper(player, start, set()))
        
        #add the one steps possible mpve
        rtn.update(self.valid_one_move(start, player))
        self.__setvalue(*start, player)
        home = player.get_home_cornner()
        start_area = self.get_area(*start)
        get_target = self.get_target_side(home)

        #make sure all the coordinates is in valid area for the tool 
        return {cor for cor in rtn if self.get_area(
            *cor) in [0, get_target, home if start_area == home else 0
                      ] and cor != start and self.get_value_in_board(*cor) == 0}
        
    def check_start(self, player, start, regular = True):
        '''this function returns if the start position is valid'''
        try:
            parser_start = self.parser_from_reg(*start) if regular else start
            start_in_board = self.__in_range(*parser_start)
            valid_player = player == self.get_value_in_board(*parser_start)
            return start_in_board and valid_player
        except:
            return False
    
    def check_end(self, end, regular = True):
        '''this function check if the end position is valid'''
        try:
            parser_end = self.parser_from_reg(*end) if regular else end
            end_in_board = self.__in_range_check_inside(*parser_end, False)
            return parser_end and end_in_board and end_in_board
        except:
            return False
    
    def update_moves_ater_check(self, start, end, player):
        '''this function update the final move in the board'''
        self.__setvalue(*start, 0)
        self.__setvalue(*end, player)

    def make_move(self, player:Player, start, end , regular = True):
        '''this function gets start and end positions and try to move
        if succes return the coordinates, regular is for parsing from normal'''
        if self.check_end(end, regular) and self.check_start(player, start, regular):
            parser_start = self.parser_from_reg(*start) if regular else start
            parser_end = self.parser_from_reg(*end) if regular else end
            all_valid_end = self.hint_end_turn(player, parser_start)
            if parser_end in all_valid_end:
                self.update_moves_ater_check(parser_start, parser_end, player)
                return parser_start, parser_end
    
    def __get_circale(self, x, y, coords = []):
        '''this function get one coordinate and return the char
        for printing in the board, if the coordinate in coords
        will be retturn char of hint else regular'''
        if self.__board[x][y]:
            return str(self.__board[x][y])
        else:
            return Board.HINT if (x,y) in coords else Board.EMPTY

    def board_to_string(self, coords = []):
        '''this function transfer the board to text string for printing
        if the list will be givven - check the char for hint or no'''
        return "\n".join(["ᅠ".join([self.__get_circale(x,y,coords)
                            for y in self.__board[x]]).center(25)
                            for x in self.__board ])
    
    def get_hint(self, player, start):
        '''this function get player and start and returns the hint
        board for all possible move in string'''
        start_parser = self.parser_from_reg(*start)
        return self.board_to_string(self.hint_end_turn(player, start_parser))
    

    def __str__(self) -> str:
        '''board to string'''
        return self.board_to_string()
    
    def update_comp_coord(self, player, start, end):
        '''change the computer coords afyer turn'''
        home = player.get_home_cornner()
        self.__computer_coords[home].discard(start)
        self.__computer_coords[home].add(end)


    def distance_to_point(self, start, end):
        '''this function gets two coordinates returns the distance between'''
        x1,y1 = start
        x2,y2 = end
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    def compare_by_distance(self, player, optinals, act):
        '''this function gets player and optional moves return 
        the closest cell to the edge of target move or the farest
        from the home'''
        home = player.get_home_cornner()
        target = Board.KODKODS[self.get_target_side(home)]
        mov_coord = None
        #according the board no 2 point with disatance 100
        distance = 100 if act else 0
        for mov in optinals:
            new_distance = self.distance_to_point(mov, target)
            if act:
                if new_distance < distance:
                    mov_coord, distance = mov, new_distance
            else:
                if new_distance > distance:
                    mov_coord, distance = mov, new_distance
        return mov_coord

    def make_ramdom_comp_move(self, player):
        '''this function gets player and make move towards the target'''
        home = player.get_home_cornner()
        trys = self.__computer_coords[home].copy()
        while trys:
            if random.randint(0, 3):
                #75% select random start coordinate of auto player 
                start = random.choice(list(trys))  
            else:
                #25% select the farest tool from the target
                start = self.compare_by_distance(player, trys, False)
            all_moves = self.hint_end_turn(player, start)
            if all_moves:
                #select end point that closing the selected towards to target 
                mov_coord = self.compare_by_distance(player,all_moves, True)
                if mov_coord:
                    if self.make_move(player, start, mov_coord, False):
                        self.update_comp_coord(player,start, mov_coord)
                        return start, mov_coord
            trys.discard(start)