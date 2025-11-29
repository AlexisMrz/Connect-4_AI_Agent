import numpy as np
import random
import time

class MinimaxAgent:
    """
    Agent utilisant minimax et élagage alpha-beta 
    """

    def __init__(self, env, player_name=None):
        """
        Initialise un agent minimax
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.time_limit=2.85
        self.player_name = player_name or f"Minimax(d={6})"
        self.rows = 6
        self.cols = 7

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Joue le meilleur coup pour l'agent
        """
        start_time = time.time()
        
        if isinstance(observation, dict) and "observation" in observation:
            board = observation["observation"]
        else:
            board = observation
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        
        winning_move = self._find_winning_move(board, valid_actions, channel=0)

        if winning_move is not None:
            return winning_move
        

        blocking_move = self._find_winning_move(board, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move
        
        safe_actions = []
        for col in valid_actions:
            if not self._gives_opponent_win(board, col, channel=0):
                safe_actions.append(col)
        candidates = safe_actions if safe_actions else valid_actions
        
        for col in candidates:
            if self._creates_double_threat(board, col, channel=0):
                return col

        for col in candidates:
            if self._creates_double_threat(board, col, channel=1):
                return col
        
        valid_actions.sort(key=lambda x: abs(x - 3))
        
        best_move_overall = valid_actions[0] if valid_actions else 0

        try:
            
            for depth in range(1, 43): 
                
                current_duration = time.time() - start_time
                if current_duration > 0.01: 
                    estimated_next_duration = current_duration * 6
                    if current_duration + estimated_next_duration > self.time_limit:
                        break 

                best_move_this_depth = None
                best_val_this_depth = float('-inf')
                
                
                for action in valid_actions:
                    
                    if time.time() - start_time > self.time_limit:
                        raise TimeoutError("Stop")

                    new_board = self._simulate_move(board, action, channel=0)
                    
                    
                    val = self._minimax(new_board, depth - 1, float('-inf'), float('inf'), False, start_time)
                    
                    if val > best_val_this_depth:
                        best_val_this_depth = val
                        best_move_this_depth = action
                
                
                best_move_overall = best_move_this_depth
                
                
                if best_val_this_depth > 9000:
                    break

        except TimeoutError:
            pass 
        return best_move_overall

    def _minimax(self, board, depth, alpha, beta, maximizing, start_time):
        """
        Minimax avec élagage alpha beta
        """
        
        if (time.time() - start_time) > self.time_limit:
            raise TimeoutError()

        if self._check_win(board, 0):
            return 10000 + depth
        if self._check_win(board, 1):
            return -10000 - depth

        valid_moves = self._get_valid_moves(board)

        if depth == 0 or not valid_moves:
            return self._evaluate(board)
            
        
        valid_moves.sort(key=lambda x: abs(x - 3))

        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=0)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, False, start_time)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=1)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, True, start_time)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
        
    def _find_winning_move(self, observation, valid_actions, channel):
        """Cherche s'il y a une possibilité de victoire immédiate"""
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

    def _simulate_move(self, board, col, channel):
        """
        Reproduit et simule le tableau si on jouait dans la colonne col
        """
        new_board = board.copy()
        rows = new_board.shape[0]

        for row in range(rows - 1, -1, -1):
            if new_board[row, col, 0] == 0 and new_board[row, col, 1] == 0:
                new_board[row, col, channel] = 1
                break
        
        return new_board

    def _get_valid_moves(self, board):
        """
        Liste des indices de colonnes valides
        """
        valid_moves = []
        cols = board.shape[1]
        for c in range(cols):
            if board[0, c, 0] == 0 and board[0, c, 1] == 0:
                valid_moves.append(c)
        return valid_moves

    def _evaluate(self, board):
        """
        Fonction d'évaluation : Offensive ET Défensive
        """
        score = 0
        player = 0   # Nous
        opp = 1      # L'adversaire
        
        # 1. Contrôle du centre
        center_col = 3
        score += np.count_nonzero(board[:, center_col, player] == 1) * 3

        # 2. Analyse des fenêtres
        windows = []
        # Extraction de toutes les fenêtres de 4 possibles
        for r in range(self.rows):
            for c in range(self.cols - 3):
                windows.append(board[r, c:c+4, :])
        for r in range(self.rows - 3):
            for c in range(self.cols):
                windows.append(board[r:r+4, c, :])
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                windows.append(np.array([board[r+i, c+i, :] for i in range(4)]))
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                windows.append(np.array([board[r-i, c+i, :] for i in range(4)]))

        for w in windows:
            us = np.count_nonzero(w[:, player] == 1)
            them = np.count_nonzero(w[:, opp] == 1)
            
            # --- ATTAQUE ---
            if us == 3 and them == 0:
                score += 5  # Menace offensive
            elif us == 2 and them == 0:
                score += 2
            
            # --- DÉFENSE ---
            # CORRECTION : Augmentation drastique des pénalités
            # Si l'adversaire a 3 pions, c'est -1000 (plus fort que n'importe quelle attaque)
            if them == 3 and us == 0:
                score -= 1000 
            # On pénalise aussi les débuts de lignes adverses pour être proactif
            elif them == 2 and us == 0:
                score -= 10

        return score
    def _check_win(self, board, channel):
        """
        Regarde si le joueur channel a gagné
        """
        rows, cols = board.shape[0], board.shape[1]

        for r in range(rows):
            for c in range(cols - 3):
                if np.all(board[r, c:c+4, channel] == 1):
                    return True
        

        for r in range(rows - 3):
            for c in range(cols):
                if np.all(board[r:r+4, c, channel] == 1):
                    return True
        

        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r+i, c+i, channel] == 1 for i in range(4)):
                    return True
        
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(board[r-i, c+i, channel] == 1 for i in range(4)):
                    return True
                    
        return False



    def _count_pieces_in_center(self, board, channel):
        center_col = 3
        return np.sum(board[:, center_col, channel])

    def _count_three_in_row(self, board, channel):
        return self._count_pattern(board, channel, length=3)

    def _count_two_in_row(self, board, channel):
        return self._count_pattern(board, channel, length=2)

    def _count_pattern(self, board, channel, length):
        #Compte les suites de pions de channel de longueur length
        count = 0
        rows, cols = board.shape[0], board.shape[1]
        
        def check_window(window):
            nb_pions = np.sum(window[:, channel])
            nb_adverses = np.sum(window[:, 1-channel])
            return (nb_pions == length) and (nb_adverses == 0)


        for r in range(rows):
            for c in range(cols - 3):
                window = board[r, c:c+4, :]
                if check_window(window): count += 1
        

        for r in range(rows - 3):
            for c in range(cols):
                window = board[r:r+4, c, :]
                if check_window(window): count += 1

        for r in range(rows - 3):
            for c in range(cols - 3):
                w1 = np.array([board[r+i, c+i, :] for i in range(4)])
                if check_window(w1): count += 1
        
        for r in range(3, rows):
            for c in range(cols - 3):
                w2 = np.array([board[r-i, c+i, :] for i in range(4)])
                if check_window(w2): count += 1
                
        return count
    
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
    def _get_next_row(self, board, col):
        """Renvoie le numéro de ligne dans lequel tomberait 
        la pièce si elle était jouée dans la colonne col """
       
        rows=6
        for row in range(rows-1,-1,-1):
            if board[row,col,0]==0 and board[row,col,1]==0:
                return row
        return None
    def _check_win_from_position(self, board, row, col, channel):
        """Regarde si placer une pièce dans la case (row,col) donne
        la victoire à l'agent"""
        
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
    def _gives_opponent_win(self, board, col, channel):
        """
        Vérifie si jouer en 'col' permet à l'adversaire de gagner juste au-dessus.
        Méthode : Backtracking (On pose, on regarde, on retire).
        C'est plus sûr que l'optimisation pure.
        """
        my_row = self._get_next_row(board, col)
        if my_row is None: return False 
        
        opp_row = my_row - 1
        if opp_row < 0: return False 
        
        # 1. On pose notre pion temporairement
        board[my_row, col, channel] = 1
        
        # 2. On vérifie si l'adversaire gagne en jouant au-dessus
        opponent = 1 - channel
        gives_win = self._check_win_from_position(board, opp_row, col, opponent)
        
        # 3. On retire le pion (Backtracking) pour laisser le plateau propre
        board[my_row, col, channel] = 0
        
        return gives_win