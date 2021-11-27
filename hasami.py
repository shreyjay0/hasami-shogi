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
      self.__board[start_x][start_y] = None
      self.__board[dest_x][dest_y] = self.__pieces.index(curr_active)
      
      for idr,rx in enumerate(self.__board):
        curr_a = None
        curr_b = None
        afind = False
        rem_arr = []
        for r_def in rx:
          if curr_a == None and r_def != None:
            afind = True
            curr_b = r_def
            rem_arr = []
          elif curr_a != None and r_def != None and r_def == curr_b and afind == True:
            afind = False
            for idx in rem_arr:
              self.__board[idr][idx] = None
              self.__pieces_captured[curr_active] += 1
            rem_arr=[]
          elif curr_a != None and r_def != None and r_def != curr_b and afind == True:
            rem_arr.append(rx.index(r_def))
          elif r_def == None:
            curr_b = None
            afind = False            
            rem_arr = []
          curr_a = r_def

      idr = 0
      for rx in zip(*self.__board):
        curr_a, curr_b= None, None
        afind = False
        rem_arr = []
        for r_def in rx:
          if curr_a == None and r_def != None :
            curr_b = r_def
            afind = True
            rem_arr = []
          elif curr_a != None and r_def != None and r_def != curr_b and afind == True:
            rem_arr.append(rx.index(r_def))
          elif curr_a != None and r_def != None and r_def == curr_b and afind == True:
            afind = False
            for idx in rem_arr:
              self.__board[idx][idr] = None
              self.__pieces_captured[curr_active] += 1
            rem_arr=[]
          elif r_def == None:
            afind = False            
            curr_b = None
            rem_arr = []
          curr_a = r_def
        idr += 1
      for cran in range(-1,1):
        for idx, r_def in enumerate(self.__board[cran]):
          if r_def != self.__pieces.index(curr_active) and r_def != None:
            ortho_accept = idx-1, idx+1
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
