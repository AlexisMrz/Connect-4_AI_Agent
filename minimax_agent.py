import numpy as np
import random


class MinimaxAgent:
    """
    Agent utilisant minimax et élagage alpha-beta 
    """

    def __init__(self, env, depth=4, player_name=None):
        """
        Initialise un agent minimax
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.depth = depth
        self.player_name = player_name or f"Minimax(d={depth})"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Joue le meilleur coup pour l'agent
        """
        if isinstance(observation, dict) and "observation" in observation:
            board = observation["observation"]
        else:
            board = observation
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]

        best_action = None
        best_value = float('-inf')

     
        for action in valid_actions:
            #Simule un coup
            new_board = self._simulate_move(board, action, channel=0)

            # Evalue la qualité du coup, selon les coups de l'adversaire
            value = self._minimax(new_board, self.depth - 1, float('-inf'), float('inf'), False)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action if best_action is not None else random.choice(valid_actions)

    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        Minimax avec élagage alpha beta
        """

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
                #On évalue tous les coups permis
                new_board = self._simulate_move(board, col, channel=0)
                
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                
                alpha = max(alpha, eval_score)
                #Mais on arrête de chercher dans une branche qui nous donnera 
                #un moins bon coup que le coup actuel
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=1)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                # L'adversaire cherche le pire coup pour nous
                if beta <= alpha:
                    break
            return min_eval

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
        Evalue notre position dans la grille courante
        """
        
        player_channel = 0
        score = 0

        if self._check_win(board, player_channel):
            return 10000

        if self._check_win(board, 1 - player_channel):
            return -10000


        score += self._count_three_in_row(board, player_channel) * 5


        score += self._count_two_in_row(board, player_channel) * 2


        score += self._count_pieces_in_center(board, player_channel) * 3

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