import random
import numpy as np
import time

class Agent:
    """
    Agent Minimax Expert
    Utilise une Heuristique "Heatmap" issue de la recherche et des poids exponentiels.
    """
    def __init__(self, env, player_name=None):
        self.env = env
        self.rows = 6
        self.cols = 7
        self.time_limit = 2.85
        self.player_name = player_name or "Minimax_Expert"
        
        

        self.evaluation_table = np.array([
            [3, 4, 5, 7, 5, 4, 3],  
            [4, 6, 8, 10, 8, 6, 4], 
            [5, 8, 11, 13, 11, 8, 5], 
            [5, 8, 11, 13, 11, 8, 5], 
            [4, 6, 8, 10, 8, 6, 4], 
            [3, 4, 5, 7, 5, 4, 3]   
        ])

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        start_time = time.time()

        if isinstance(observation, dict) and "observation" in observation:
            board = observation["observation"]
        else:
            board = observation

        if action_mask is not None:
            valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        else:
            valid_actions = self._get_valid_moves(board)

 
       
        winning = self._find_winning_move(board, valid_actions, 0)
        if winning is not None: return winning

        
        blocking = self._find_winning_move(board, valid_actions, 1)
        if blocking is not None: return blocking

       
        safe_actions = []
        for col in valid_actions:
            if not self._gives_opponent_win(board, col, 0):
                safe_actions.append(col)
        
        candidates = safe_actions if safe_actions else valid_actions

       
        for col in candidates:
            if self._move_creates_double_threat(board, col, 0): return col
        for col in candidates:
            if self._move_creates_double_threat(board, col, 1): return col

  
        center_col = 3
        candidates.sort(key=lambda x: abs(x - center_col))
        best_move = candidates[0] if candidates else 0

        try:
            for depth in range(1, 43): 
                current_duration = time.time() - start_time
                if current_duration > 0.01:
                    if current_duration + (current_duration * 6) > self.time_limit:
                        break 

                best_val = float('-inf')
                best_move_depth = candidates[0]
                
                for action in candidates:
                    if time.time() - start_time > self.time_limit:
                        raise TimeoutError()

                    new_board = self._simulate_move(board, action, 0)
                    val = self._minimax(new_board, depth - 1, float('-inf'), float('inf'), False, start_time)
                    
                    if val > best_val:
                        best_val = val
                        best_move_depth = action
                
                best_move = best_move_depth
                
                if best_val > 900000: break

        except TimeoutError:
            pass 
            
        return best_move

    def _minimax(self, board, depth, alpha, beta, maximizing, start_time):
        if (time.time() - start_time) > self.time_limit:
            raise TimeoutError()

        if self._check_win(board, 0): return 1000000 + depth
        if self._check_win(board, 1): return -1000000 - depth

        valid_moves = self._get_valid_moves(board)
        if depth == 0 or not valid_moves:
            return self._evaluate(board)
            
        center = 3
        valid_moves.sort(key=lambda x: abs(x - center))

        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, 0)
                score = self._minimax(new_board, depth - 1, alpha, beta, False, start_time)
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, 1)
                score = self._minimax(new_board, depth - 1, alpha, beta, True, start_time)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha: break
            return min_eval

  

    def _evaluate(self, board):
        score = 0
        player = 0
        opp = 1
        
  
        my_pieces = (board[:, :, player] == 1)
        opp_pieces = (board[:, :, opp] == 1)
        
        score += np.sum(self.evaluation_table * my_pieces)
        score -= np.sum(self.evaluation_table * opp_pieces)


        for r in range(self.rows):
            for c in range(self.cols - 3):
                window = board[r, c:c+4, :]
                score += self._score_window(window, player, opp)
    
        for r in range(self.rows - 3):
            for c in range(self.cols):
                window = board[r:r+4, c, :]
                score += self._score_window(window, player, opp)
      
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                w1 = np.array([board[r+i, c+i, :] for i in range(4)])
                score += self._score_window(w1, player, opp)
                
                w2 = np.array([board[r+3-i, c+i, :] for i in range(4)])
                score += self._score_window(w2, player, opp)

        return score

    def _score_window(self, window, player, opp):
        """
        Calcule le score d'une fenêtre de 4 cases.
        Poids basés sur la littérature Connect 4.
        """
        score = 0
        us = np.count_nonzero(window[:, player] == 1)
        them = np.count_nonzero(window[:, opp] == 1)
        empty = np.count_nonzero((window[:, 0] == 0) & (window[:, 1] == 0)) 

    
        if us == 4: score += 1000000
        elif us == 3 and empty == 1: score += 100  
        elif us == 2 and empty == 2: score += 5    

        
        if them == 3 and empty == 1: 
            score -= 80000 
        elif them == 2 and empty == 2:
            score -= 10 

        return score

 
    def _find_winning_move(self, board, valid_actions, channel):
        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is not None:
                if self._check_win_from_position(board, row, col, channel):
                    return col
        return None

    def _gives_opponent_win(self, board, col, channel):
        my_row = self._get_next_row(board, col)
        if my_row is None: return False
        opp_row = my_row - 1
        if opp_row < 0: return False
        
        
        board[my_row, col, channel] = 1
        opponent = 1 - channel
        gives_win = self._check_win_from_position(board, opp_row, col, opponent)
        board[my_row, col, channel] = 0
        return gives_win

    def _move_creates_double_threat(self, board, col, channel):
        temp_board = board.copy()
        row = self._get_next_row(temp_board, col)
        if row is None: return False
        temp_board[row, col, channel] = 1
        
        threats = 0
        valid = self._get_valid_moves(temp_board)
        for c in valid:
            r = self._get_next_row(temp_board, c)
            if r is not None and self._check_win_from_position(temp_board, r, c, channel):
                threats += 1
        return threats >= 2

    def _simulate_move(self, board, col, channel):
        new_board = board.copy()
        for r in range(self.rows - 1, -1, -1):
            if new_board[r, col, 0] == 0 and new_board[r, col, 1] == 0:
                new_board[r, col, channel] = 1
                break
        return new_board

    def _get_valid_moves(self, board):
        valid = []
        for c in range(self.cols):
            if board[0, c, 0] == 0 and board[0, c, 1] == 0:
                valid.append(c)
        return valid

    def _get_next_row(self, board, col):
        for r in range(self.rows - 1, -1, -1):
            if board[r, col, 0] == 0 and board[r, col, 1] == 0:
                return r
        return None

    def _check_win_from_position(self, board, row, col, channel):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < self.rows and 0 <= c < self.cols and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < self.rows and 0 <= c < self.cols and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc
            if count >= 4: return True
        return False

    def _check_win(self, board, channel):
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if np.all(board[r, c:c+4, channel] == 1): return True
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if np.all(board[r:r+4, c, channel] == 1): return True
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(board[r+i, c+i, channel] == 1 for i in range(4)): return True
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if all(board[r-i, c+i, channel] == 1 for i in range(4)): return True
        return False