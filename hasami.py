class HasamiShogiGame:

  def __init__(self):
    """
    Detailed text description of how to handle the scecnarios
    1. Make 2d arrays with x blocks in y for board creation. 
    At a stage board will have pieces (red/black) which will be added
    to the array (as binary) as the players make their move.
    Add pieces and their info as dictionary. 
    Set x_rows label from a to i

    2. In init method:
    initialise the board with red and black pieces on either sides. 
    Set turn to black. 
    Players wont have any captured pieces in the start so set both dictionary y_cols to 0
    """
    """
    initialises data members
    
    args:
    none
    
    returns:
    none
    """
    self.__board = [[0 if yblock == 0 else (1 if yblock == 8 else None) for xblock in range(0,9)] for yblock in range(0,9)]
    self.__pieces = ["RED", "BLACK"]
    self.__game_state ="UNFINISHED"
    self.__labelname = ["a","b","c","d","e","f","g","h","i"]
    self.__current_chance = self.__pieces[1]
    self.__pieces_captured = {"RED": 0, "BLACK": 0}
    self.__pos_as_int = {0: "RED", 1: "BLACK", None: None}

  def get_game_state(self):
    """
    gives game state
    
    args:
    none
    
    returns:
    str: game state
    """
    return self.__game_state
  
  def get_active_player(self):
    """
    Detailed text description of how to handle the scecnarios
    3. Return self's turn y_col which get's interchanged 
    every successful move
    """
    """
    tells active player
    
    args:
    none
    
    returns:
    str: player whose turn it is
    """
    return self.__current_chance
  
  def get_num_captured_pieces(self, pcolor):
    """
    number of captured pieces of the argument's color
    
    args:
    pcolor: str, piece
    
    returns:
    int: amount of pieces the argument color has captured
    """
    count = self.__pieces_captured[pcolor]
    return count
  
  def make_move(self, from_square_location, to_square_location):
    """
    Detailed text description of how to handle the scecnarios
    4. Check if the player is moving right color piece
    Check the game state
    Check if the move is not to origin and is within bounds
    make the move if legal 
    5. Capture the pieces that are between current player's 
    pieces if in horizontal or vertical line
    if the piece is at corner then capture it if orthogonal grids
    are current player's pieces
    6. Check if the game's state is not UNFINISHED, 
    then end the game
    """
    """
    Checks if the move is legal and the 
    piece at from belongs to the right player 
    and then makes the move while also updating 
    states and capturing pieces if any
    
    args:
    from_square_location: str, location to move the piece from
    to_square_location: str, piece destination
    
    returns:
    boolean: if move was successful or not
    """
    start_x = self.__labelname.index(from_square_location[0])
    start_y = int(from_square_location[1]) - 1
    dest_x = self.__labelname.index(to_square_location[0])
    dest_y = int(to_square_location[1]) - 1
    curr_active = self.get_active_player()
    if start_x != dest_x and start_y != dest_y:
      return False
    elif curr_active != self.__pos_as_int[self.__board[start_x][start_y]]:
      return False
    elif self.get_square_occupant(to_square_location) != "NONE":
      return False
    elif self.__game_state != "UNFINISHED":
      return False
    else:
      if start_x == dest_x:
        strt, end = start_y, dest_y
        if start_y > dest_y:
          strt, end = dest_y, start_y
        for count in range(strt+1,end):
          if self.__board[dest_x][count] != None:
            return False
      else: 
        strt, end = start_x, dest_x
        if start_x > dest_x:
          strt, end = dest_x, start_x
        for count in range(strt+1,end):
          if self.__board[count][dest_y] != None:
            return False

      self.__board[start_x][start_y] = None
      self.__board[dest_x][dest_y] = self.__pieces.index(curr_active)
      
      idr = start_x
      rx = self.__board[idr]
      curr_a = None
      curr_b = None
      afind = False
      rem_arr = []
      #l to r
      active = self.__pieces.index(curr_active)
      opp = 1 if active == 0 else 0
      pconsecutive_right = 0
      pconsecutive_left = 0
      removable = False
      if dest_y < 7 :
        for r_def in range (dest_y+1,9):
          ele = self.__board[dest_x][r_def]
          if ele == active and r_def - dest_y == 1:
            pconsecutive_right = 0
            break
          elif ele == opp:
            pconsecutive_right += 1
          elif ele == active and r_def - dest_y > 1:
            removable = True
            break
          else:
            break
      if dest_y > 2:
        for r_def in range (dest_y-1,-1,-1):
          ele = self.__board[dest_x][r_def]
          if ele == active and dest_y - r_def == 1:
            pconsecutive_left = 0
            break
          elif ele == opp:
            pconsecutive_left += 1
          elif ele == active and dest_y - r_def > 1:
            removable = True
            break
          else:
            break
      if pconsecutive_left > 0 and removable:
        for del_ran in range(pconsecutive_left):
          self.__board[dest_x][dest_y - del_ran - 1] = None
          self.__pieces_captured[curr_active] += 1
      if pconsecutive_right > 0 and removable: #changes here
        for del_ran in range(pconsecutive_right):
          self.__board[dest_x][dest_y + del_ran + 1] = None
          self.__pieces_captured[curr_active] += 1

      opp = 1 if active == 0 else 0
      pconsecutive_up = 0
      pconsecutive_below = 0
      removable = False
      if dest_x < 7:
        for r_def in range (dest_x+1,9):
          ele = self.__board[r_def][dest_y]
          if ele == active and r_def - dest_x == 1:
            pconsecutive_up = 0
            break
          elif ele == opp:
            pconsecutive_up += 1
          elif ele == active and r_def - dest_x > 1:
            removable = True
            break
          else:
            break
      if dest_x > 2:
        for r_def in range (dest_x-1,-1,-1):
          ele = self.__board[r_def][dest_y]
          if ele == active and dest_x - r_def == 1:
            pconsecutive_below = 0
            break
          elif ele == opp:
            pconsecutive_below += 1
          elif ele == active and dest_x - r_def > 1:
            removable = True
            break
          else:
            break
      if pconsecutive_below > 0 and removable:
        for del_ran in range(pconsecutive_below):
          self.__board[dest_x - del_ran - 1][dest_y] = None
          self.__pieces_captured[curr_active] += 1
      if pconsecutive_up > 0 and removable: #changes here
        for del_ran in range(pconsecutive_up):
          self.__board[dest_x + del_ran + 1][dest_y] = None
          self.__pieces_captured[curr_active] += 1

        
      for cran in range(-1,1):
        for idx, r_def in enumerate(self.__board[cran]):
          if r_def != self.__pieces.index(curr_active) and r_def != None:
            ortho_accept = idx-1, idx+1
            if [cran,idx] in [[0,0],[0,8],[8,0],[8,8]]:
              if all(j>=0 and j<len(self.__board[cran]) for j in ortho_accept) :
                  if (self.__board[cran][idx-1] == self.__pieces.index(curr_active)) or (self.__board[cran][idx+1] == self.__pieces.index(curr_active)):
                    if cran == -1:
                      if self.__board[cran-1][idx] == self.__pieces.index(curr_active):
                          self.__pieces_captured[curr_active] += 1
                          self.__board[cran][idx] = None

              elif idx+1>0 and idx+1<len(self.__board[cran]):
                if self.__board[cran][idx+1] == self.__pieces.index(curr_active):
                    if cran == -1:
                      if self.__board[cran-1][idx] == self.__pieces.index(curr_active):
                          self.__pieces_captured[curr_active] += 1 
                          self.__board[cran][idx] = None
                          
              elif idx-1>0 and idx-1<len(self.__board[cran]):
                if self.__board[cran][idx-1] == self.__pieces.index(curr_active):
                    if cran == -1:
                      if self.__board[cran-1][idx] == self.__pieces.index(curr_active):
                          self.__pieces_captured[curr_active] += 1               
                          self.__board[cran][idx] = None

      if self.__pieces_captured["RED"] > 7:
        self.__game_state= "RED_WON"
      elif self.__pieces_captured["BLACK"] > 7:
        self.__game_state= "BLACK_WON"
      else:
        self.__game_state="UNFINISHED"
    if self.__current_chance == "BLACK":
      self.__current_chance = "RED"
    else: 
      self.__current_chance = "BLACK"
     
    return True
    
  def get_square_occupant(self, square_location):
    """
    gives the color of argument square's occupant
    
    args:
    square_location: str, location of square 
    
    returns:
    str: color of piece occupying the square if any
    """
    inp_label = square_location[0] 
    sq_x = self.__labelname.index(inp_label)
    inp_id = square_location[1]
    sq_y = int(inp_id)-1
    piece_at_given_sq = self.__board[sq_x][sq_y]
    if piece_at_given_sq != None:
        occupant = self.__pos_as_int[piece_at_given_sq]
    else: occupant = 'NONE'
    return occupant

    #to be removed before submission
  def show_board(self):
    print("\n"," ===== Board ===== ","\n")
    
    print(" ",end=" ")
    [print(col_val, end=" ") for col_val in range(1,10)]
    print("\n", end="")
    for ii, x_row in enumerate(self.__board):
      for jj, y_col in enumerate(x_row):
        printable_val = {None:'.', 0:'R', 1:'B',}
        to_print = printable_val[y_col]
        if jj == 0:
         print(self.__labelname[ii] + " " + to_print, end=" ") 
        elif jj == len(x_row)-1:
          print(to_print, end="\n")
        else:
          print(to_print, end=" ")

