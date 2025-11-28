import numpy as np
import random
import math
import time


class MCTSNode:
    """
    Noeud dans l'arbre de décisions
    """

    def __init__(self, board, player, parent=None, move=None):
        self.board = board        
        self.player = player      
        self.parent = parent      
        self.move = move          
        self.children = []        
        self.visits = 0           
        self.wins = 0             

    def is_fully_expanded(self):
        """Regarde si tous les enfants ont été ajoutés"""
        valid_moves = self._get_valid_moves()
        return len(self.children) == len(valid_moves)

    def best_child(self, c=1.41):
        """
        Sélectionne le meilleur enfant à explorer
        """
        best_score = float('-inf')
        best_child = None
        for child in self.children:
            if child.visits==0:
                return child
            exploit = child.wins / child.visits
            explore = c * math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + explore

            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def _get_valid_moves(self):
        """liste de colonnes valides"""
        valid_moves = []
        cols = self.board.shape[1]
        # On parcourt les colonnes (0 à 6)
        for col in range(cols):
            # Si la case du haut (row 0) est vide pour les deux joueurs, la colonne est valide
            if self.board[0, col, 0] == 0 and self.board[0, col, 1] == 0:
                valid_moves.append(col)
        return valid_moves


class MCTSAgent:
    

    def __init__(self, env, time_limit=0.95, player_name=None):
        """
        Initialise un agent MCTS
        """
        self.env = env
        self.time_limit = time_limit
        self.player_name = player_name or "MCTS"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choisit le meilleur coup selon MCTS
        """
        
        if isinstance(observation, dict) and "observation" in observation:
            board = observation["observation"]
        else:
            board = observation
        #Crée le noeud de départ (la racine)
        root = MCTSNode(board, player=0)

        start_time = time.time()

        #Utilise le maximum de temps disponible
        simulations = 0
        while time.time() - start_time < self.time_limit:
            # Sélection de l'enfant
            node = self._select(root)

            # Expansion
            if not self._is_terminal(node):
                node = self._expand(node)

            # Simulation
            result = self._simulate(node)

            # Backpropagation
            self._backpropagate(node, result)

            simulations += 1

        # Choisit le meilleur coup
        best_child = root.best_child(c=0)
        return best_child.move

    def _select(self, node):
        """
        Sélectionne un noeud prometteur à explorer
        """

        while node.is_fully_expanded() and not self._is_terminal(node):
            if not node.children:
                break
            node=node.best_child()
        return node

    def _expand(self, node):
        """
        Ajoute un nouvel enfant au noeud
        """
        valid_moves = node._get_valid_moves()
        tried_moves = [child.move for child in node.children]
        
        untried_moves = [m for m in valid_moves if m not in tried_moves]
        
        if not untried_moves:
            return node 
            
        move = random.choice(untried_moves)
        

        new_board = node.board.copy()
        rows = new_board.shape[0]
        for r in range(rows - 1, -1, -1):
            if new_board[r, move, 0] == 0 and new_board[r, move, 1] == 0:
                new_board[r, move, node.player] = 1
                break
     
        new_player = 1 - node.player
        child = MCTSNode(new_board, player=new_player, parent=node, move=move)
        node.children.append(child)
        
        return child

    def _simulate(self, node):
        """
        Joue aléatoirement à partir du noeud
        """
        current_board = node.board.copy()
        current_player = node.player
        

        while True:

            prev_player = 1 - current_player
            rows, cols = current_board.shape[0], current_board.shape[1]
            winner = None
            
   
            for r in range(rows):
                for c in range(cols - 3):
                    if np.all(current_board[r, c:c+4, prev_player] == 1): winner = prev_player
            if winner is None:
                for r in range(rows - 3):
                    for c in range(cols):
                        if np.all(current_board[r:r+4, c, prev_player] == 1): winner = prev_player
            if winner is None:
                for r in range(rows - 3):
                    for c in range(cols - 3):
                        if all(current_board[r+i, c+i, prev_player] == 1 for i in range(4)): winner = prev_player
                        if all(current_board[r+3-i, c+i, prev_player] == 1 for i in range(4)): winner = prev_player
            
            if winner is not None:
                return winner 

            valid_moves = []
            for c in range(cols):
                if current_board[0, c, 0] == 0 and current_board[0, c, 1] == 0:
                    valid_moves.append(c)
            
            if not valid_moves:
                return 0.5 
            
            move = random.choice(valid_moves)
 
            for r in range(rows - 1, -1, -1):
                if current_board[r, move, 0] == 0 and current_board[r, move, 1] == 0:
                    current_board[r, move, current_player] = 1
                    break


            current_player = 1 - current_player



    def _backpropagate(self, node, result):
        """
        Ajuste les statistiques
        """

        while node !=None:
            node.visits+=1
            if result == 0.5:
                node.wins += 0.5
            elif node.parent is not None:
                
                if result == node.parent.player:
                    node.wins += 1
            
            node = node.parent




    def _is_terminal(self, node):
        """Indique si la partie est finie ou non"""

        board = node.board
        rows, cols = board.shape[0], board.shape[1]

        check_player = 1 - node.player

        for r in range(rows):
            for c in range(cols - 3):
                if np.all(board[r, c:c+4, check_player] == 1): return True
        for r in range(rows - 3):
            for c in range(cols):
                if np.all(board[r:r+4, c, check_player] == 1): return True
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r+i, c+i, check_player] == 1 for i in range(4)): return True
                if all(board[r+3-i, c+i, check_player] == 1 for i in range(4)): return True
  
        valid = False
        for c in range(cols):
            if board[0, c, 0] == 0 and board[0, c, 1] == 0:
                valid = True
                break
        
        return not valid