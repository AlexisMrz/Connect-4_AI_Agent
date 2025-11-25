import random
from loguru import logger

class SmartAgent:
    """
    A rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        valid_actions = self._get_valid_actions(action_mask)
        if isinstance(observation, dict):
            board = observation['observation']
        else:
            board = observation
    
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            logger.success(f"{self.player_name}: WINNING MOVE -> column {winning_move}")
            return winning_move

        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            logger.warning(f"{self.player_name}: BLOCKING -> column {blocking_move}")
            return blocking_move

        for col in valid_actions:
            if self._creates_double_threat(board,col,channel=0):
                logger.info(f"{self.player_name}:  DOUBLE THREAT TRAP  -> column {col}")
                return col 
    

        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in valid_actions:
                return col

        action = random.choice(valid_actions)
        logger.debug(f"{self.player_name}: RANDOM -> column {action}")
        return action
        
    def _creates_double_threat(self, board, col, channel):
        """
        Vérifie si jouer dans 'col' crée deux opportunités de victoire au tour suivant.
        """

        temp_board = board.copy()
        row = self._get_next_row(temp_board, col)
        if row is None: return False
        temp_board[row, col, channel] = 1 

        winning_opportunities = 0
        
      
        for next_col in range(7):
  
            next_row = self._get_next_row(temp_board, next_col)
            if next_row is not None:
                
                if self._check_win_from_position(temp_board, next_row, next_col, channel):
                    winning_opportunities += 1
        
        
        return winning_opportunities >= 2

        

    def _get_valid_actions(self, action_mask):
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        valid_columns=[]
        for index,is_valid in enumerate(action_mask):
            if is_valid==1:
                valid_columns.append(index)
        return valid_columns

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        if isinstance(observation, dict):

            board = observation['observation']
        else:
   
            board = observation
        for column in valid_actions:
            row=self._get_next_row(board,column)
            if row is not None :
                if self._check_win_from_position(board,row,column,channel):
                    return column
        return None
        

    def _get_next_row(self, board, col):
        """
        Find which row a piece would land in if dropped in column col

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)

        Returns:
            row index (0-5) if space available, None if column full
        """
       
        rows=6
        for row in range(rows-1,-1,-1):
            if board[row,col,0]==0 and board[row,col,1]==0:
                return row
        return None
        

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        
        directions = [(1, 0), (0, 1), (-1, 1), (1, 1)]
        
        rows, cols = 6, 7

        for dr, dc in directions:
            count = 1 
         
            r, c = row + dr, col + dc
            while 0 <= r < rows and 0 <= c < cols and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc

           
            r, c = row - dr, col - dc
            while 0 <= r < rows and 0 <= c < cols and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc
         
            if count >= 4:
                return True
                
        return False




        