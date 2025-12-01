from numba import njit 
import numpy as np
import time
from numba import njit


@njit(fastmath=True, cache=True)
def fast_check_win(board, player):
    """
    Vérification de victoire ultra-rapide (JIT compiled).
    Ne vérifie que pour le joueur spécifié.
    """
    for r in range(6):
        for c in range(4):
            if (board[r, c, player] == 1 and board[r, c+1, player] == 1 and
                board[r, c+2, player] == 1 and board[r, c+3, player] == 1):
                return True
    
    for r in range(3):
        for c in range(7):
            if (board[r, c, player] == 1 and board[r+1, c, player] == 1 and
                board[r+2, c, player] == 1 and board[r+3, c, player] == 1):
                return True
                
    for r in range(3):
        for c in range(4):
            if (board[r, c, player] == 1 and board[r+1, c+1, player] == 1 and
                board[r+2, c+2, player] == 1 and board[r+3, c+3, player] == 1):
                return True

    for r in range(3, 6):
        for c in range(4):
            if (board[r, c, player] == 1 and board[r-1, c+1, player] == 1 and
                board[r-2, c+2, player] == 1 and board[r-3, c+3, player] == 1):
                return True
                
    return False

@njit(fastmath=True, cache=True)
def fast_evaluate(board, player_idx):
    """
    Fonction d'évaluation heuristique optimisée.
    Scan le plateau sans allocations mémoire inutiles.
    """
    opp_idx = 1 - player_idx
    score = 0
    

    center_count = 0
    for r in range(6):
        if board[r, 3, player_idx] == 1:
            center_count += 1
    score += center_count * 3


    for r in range(6):
        for c in range(4):
            us = 0
            them = 0
            for k in range(4):
                if board[r, c+k, player_idx] == 1: us += 1
                elif board[r, c+k, opp_idx] == 1: them += 1
            
            if us == 3 and them == 0: score += 5
            elif us == 2 and them == 0: score += 2
            elif them == 3 and us == 0: score -= 1000 
            elif them == 2 and us == 0: score -= 10

    for r in range(3):
        for c in range(7):
            us = 0
            them = 0
            for k in range(4):
                if board[r+k, c, player_idx] == 1: us += 1
                elif board[r+k, c, opp_idx] == 1: them += 1
            
            if us == 3 and them == 0: score += 5
            elif us == 2 and them == 0: score += 2
            elif them == 3 and us == 0: score -= 1000
            elif them == 2 and us == 0: score -= 10

    for r in range(3):
        for c in range(4):
            us = 0
            them = 0
            for k in range(4):
                if board[r+k, c+k, player_idx] == 1: us += 1
                elif board[r+k, c+k, opp_idx] == 1: them += 1
            
            if us == 3 and them == 0: score += 5
            elif us == 2 and them == 0: score += 2
            elif them == 3 and us == 0: score -= 1000
            elif them == 2 and us == 0: score -= 10

    for r in range(3, 6):
        for c in range(4):
            us = 0
            them = 0
            for k in range(4):
                if board[r-k, c+k, player_idx] == 1: us += 1
                elif board[r-k, c+k, opp_idx] == 1: them += 1
            
            if us == 3 and them == 0: score += 5
            elif us == 2 and them == 0: score += 2
            elif them == 3 and us == 0: score -= 1000
            elif them == 2 and us == 0: score -= 10

    return score

@njit(fastmath=True, cache=True)
def fast_get_valid_moves(board):
    """Retourne un tableau booléen des coups valides [True, True, False...]"""
    valid = np.zeros(7, dtype=np.int8)
    for c in range(7):
        if board[0, c, 0] == 0 and board[0, c, 1] == 0:
            valid[c] = 1
    return valid

@njit(fastmath=True, cache=True)
def fast_simulate_move(board, col, player):
    """
    Applique la gravité et retourne un NOUVEAU plateau.
    """
    new_board = board.copy()
    for r in range(5, -1, -1):
        if new_board[r, col, 0] == 0 and new_board[r, col, 1] == 0:
            new_board[r, col, player] = 1
            break
    return new_board

class Agent:
    """
    Agent Minimax Numba-Accelerated
    Utilise Iterative Deepening + Numba JIT pour une profondeur maximale.
    """
    def __init__(self, env, player_name=None):
        self.env = env
        self.cols = 7
        self.rows = 6
        self.time_limit = 2.85
        self.player_name = player_name or "Minimax_Numba"
        
   
        print("Compiling Numba functions...")
        dummy_board = np.zeros((6, 7, 2), dtype=np.int8)
        fast_check_win(dummy_board, 0)
        fast_evaluate(dummy_board, 0)
        fast_simulate_move(dummy_board, 3, 0)
        fast_get_valid_moves(dummy_board)
        print("Numba Ready!")

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        start_time = time.time()

        if isinstance(observation, dict) and "observation" in observation:
            board = observation["observation"]
        else:
            board = observation
        
        board = board.astype(np.int8)

        if action_mask is not None:
            valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        else:
            mask = fast_get_valid_moves(board)
            valid_actions = [i for i, v in enumerate(mask) if v == 1]

     
        for col in valid_actions:
            temp = fast_simulate_move(board, col, 0)
            if fast_check_win(temp, 0): return col
            
        for col in valid_actions:
            temp = fast_simulate_move(board, col, 1) 
            if fast_check_win(temp, 1): return col

        safe_actions = []
        for col in valid_actions:
            if not self._gives_opponent_win(board, col, 0):
                safe_actions.append(col)
        
        candidates = safe_actions if safe_actions else valid_actions

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

                    new_board = fast_simulate_move(board, action, 0)
                    val = self._minimax(new_board, depth - 1, float('-inf'), float('inf'), False, start_time)
                    
                    if val > best_val:
                        best_val = val
                        best_move_depth = action
                
                best_move = best_move_depth
                if best_val > 90000: break

        except TimeoutError:
            pass
            
        return best_move

    def _minimax(self, board, depth, alpha, beta, maximizing, start_time):
        
        if (time.time() - start_time) > self.time_limit:
            raise TimeoutError()

        
        if fast_check_win(board, 0): return 100000 + depth
        if fast_check_win(board, 1): return -100000 - depth

       
        if depth == 0:
            return fast_evaluate(board, 0)
            
  
        mask = fast_get_valid_moves(board)
        
        valid_moves = [i for i, v in enumerate(mask) if v == 1]
        
        
        valid_moves.sort(key=lambda x: abs(x - 3))

        if not valid_moves: # Match nul
            return 0

        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = fast_simulate_move(board, col, 0)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, False, start_time)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = fast_simulate_move(board, col, 1)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, True, start_time)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha: break
            return min_eval

    def _gives_opponent_win(self, board, col, channel):
        """Vérifie le Zugzwang (Version Numba-Accelerated)"""
        
        try:
            temp_board = fast_simulate_move(board, col, channel)
        except:
            return False
            
        
        opponent = 1 - channel
        try:
            temp_board_2 = fast_simulate_move(temp_board, col, opponent)
            if fast_check_win(temp_board_2, opponent):
                return True
        except:
            pass
            
        return False