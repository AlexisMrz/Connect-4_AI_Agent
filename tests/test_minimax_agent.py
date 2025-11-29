import numpy as np
import time
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from minimax_agent import MinimaxAgent
import tracemalloc


class MockEnv:
    def __init__(self):
        self.agents = ["player_0", "player_1"]
    def action_space(self, agent):
        return None

def create_empty_board():
    return np.zeros((6, 7, 2), dtype=np.int8)

def set_piece(board, row, col, player):
    """Place une pièce sur le plateau (0=Nous, 1=Adversaire)"""
    board[row, col, player] = 1

def get_mask(board):
    """
    Génère le masque d'actions valides pour un plateau donné.
    Une colonne est valide (1) si la ligne du haut (index 0) est vide.
    """
    mask = np.zeros(7, dtype=np.int8)
    for c in range(7):
        # Si la case du haut est vide pour les deux joueurs
        if board[0, c, 0] == 0 and board[0, c, 1] == 0:
            mask[c] = 1
    return mask

def print_board(board):
    """Affiche le plateau pour le debug visuel"""
    print("\n  0 1 2 3 4 5 6")
    for r in range(6):
        row_str = "|"
        for c in range(7):
            if board[r, c, 0] == 1: row_str += "X|" # Nous
            elif board[r, c, 1] == 1: row_str += "O|" # Eux
            else: row_str += " |"
        print(row_str)
    print("-" * 15)

@pytest.fixture
def agent():
    return MinimaxAgent(env=MockEnv())

# --- LES 10 SCÉNARIOS DE TEST ---

def test_01_vertical_threat(agent):
    """
    SCÉNARIO 1 : Menace Verticale Simple
    L'adversaire (O) a empilé 3 pions colonne 0. Il va gagner au prochain coup.
    """
    board = create_empty_board()
    # Adversaire joue 3 fois en col 0
    set_piece(board, 5, 0, 1)
    set_piece(board, 4, 0, 1)
    set_piece(board, 3, 0, 1)
    
    print("\n[TEST 1] Menace Verticale Col 0")
    
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 0, f"ÉCHEC: Doit bloquer en 0, a joué {action}"

def test_02_horizontal_threat_right(agent):
    """
    SCÉNARIO 2 : Menace Horizontale (Côté Droit ouvert)
    Adversaire: [O O O .] en bas à gauche.
    """
    board = create_empty_board()
    set_piece(board, 5, 0, 1)
    set_piece(board, 5, 1, 1)
    set_piece(board, 5, 2, 1)
    
    print("\n[TEST 2] Menace Horizontale (Bloquer à droite)")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 3, f"ÉCHEC: Doit bloquer en 3, a joué {action}"

def test_03_horizontal_threat_left(agent):
    """
    SCÉNARIO 3 : Menace Horizontale (Côté Gauche ouvert)
    Adversaire: [. O O O] colonne 2,3,4.
    """
    board = create_empty_board()
    set_piece(board, 5, 2, 1)
    set_piece(board, 5, 3, 1)
    set_piece(board, 5, 4, 1)
    
    print("\n[TEST 3] Menace Horizontale (Bloquer à gauche ou droite)")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    # Peut bloquer en 1 ou 5
    assert action in [1, 5], f"ÉCHEC: Doit bloquer en 1 ou 5, a joué {action}"

def test_04_diagonal_threat_positive(agent):
    """
    SCÉNARIO 4 : Menace Diagonale Montante (/)
    Nécessite des pions de support pour que la case de menace soit jouable.
    """
    board = create_empty_board()
    # Supports (pions "morts" pour faire monter la diagonale)
    set_piece(board, 5, 1, 0) # Support col 1
    set_piece(board, 5, 2, 0) # Support col 2
    set_piece(board, 4, 2, 0) 
    set_piece(board, 5, 3, 0) # Support col 3
    set_piece(board, 4, 3, 0) 
    set_piece(board, 3, 3, 0) 

    # Menace Adverse (O)
    set_piece(board, 5, 0, 1) # (5,0)
    set_piece(board, 4, 1, 1) # (4,1)
    set_piece(board, 3, 2, 1) # (3,2)
    # La case gagnante est (2,3) -> Colonne 3
    
    print("\n[TEST 4] Menace Diagonale /")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 3, f"ÉCHEC: Doit bloquer la diagonale en 3, a joué {action}"

def test_05_win_over_block(agent):
    """
    SCÉNARIO 5 : Gagner > Bloquer
    L'adversaire a une menace de victoire, MAIS nous pouvons gagner tout de suite.
    L'agent ne doit pas avoir peur, il doit tuer.
    """
    board = create_empty_board()
    # Menace Adverse en Col 0
    set_piece(board, 5, 0, 1)
    set_piece(board, 4, 0, 1)
    set_piece(board, 3, 0, 1) # Il gagne au prochain tour !

    # Notre Opportunité en Col 6
    set_piece(board, 5, 6, 0)
    set_piece(board, 4, 6, 0)
    set_piece(board, 3, 6, 0) # On gagne MAINTENANT !

    print("\n[TEST 5] Priorité Victoire")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 6, f"ÉCHEC: Aurait dû gagner en 6, a paniqué et joué {action}"

def test_06_split_threat(agent):
    """
    SCÉNARIO 6 : Menace Écartelée (O . O O)
    L'adversaire a des pions en 0, 2, 3. Il gagne s'il joue en 1.
    """
    board = create_empty_board()
    set_piece(board, 5, 0, 1)
    # Trou en 1
    set_piece(board, 5, 2, 1)
    set_piece(board, 5, 3, 1)

    print("\n[TEST 6] Menace à trou (O . O O)")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 1, f"ÉCHEC: Doit combler le trou en 1, a joué {action}"

def test_07_prevent_setup(agent):
    """
    SCÉNARIO 7 : Prévention (2 pions alignés)
    L'adversaire a 2 pions. Minimax doit-il bloquer ? 
    Pas forcément obligatoire si depth=4, mais avec notre heuristique défensive (-10),
    il devrait préférer bloquer si rien d'autre à faire.
    """
    board = create_empty_board()
    set_piece(board, 5, 3, 1)
    set_piece(board, 4, 3, 1) # Adversaire au centre, vertical

    print("\n[TEST 7] Gêne préventive (Centre)")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    # Minimax devrait essayer de contester la colonne 3
    assert action == 3, f"ÉCHEC: Devrait bloquer la construction verticale en 3, a joué {action}"

def test_08_full_board_mess(agent):
    """
    SCÉNARIO 8 : Plateau Presque Plein (Complexité)
    On remplit tout sauf la colonne 0 (Gagnante pour nous) et 1 (Neutre).
    """
    board = np.ones((6, 7, 2), dtype=np.int8)
    # On vide les colonnes 0 et 1 pour qu'elles soient jouables
    board[:, 0, :] = 0
    board[:, 1, :] = 0
    
    # On reconstruit un scénario simple pour éviter de gérer les conflits du board.ones
    board = create_empty_board()
    # On remplit les colonnes 2 à 6
    for c in range(2, 7):
        for r in range(6):
            set_piece(board, r, c, 1) # Rempli de pions adverses "morts"
    
    # Notre setup en 0
    set_piece(board, 5, 0, 0)
    set_piece(board, 4, 0, 0)
    set_piece(board, 3, 0, 0)
    
    print("\n[TEST 8] Plateau encombré")
    # Mask sera [1, 1, 0, 0, 0, 0, 0]
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 0, f"ÉCHEC: A raté la victoire évidente en 0 dans le bruit, a joué {action}"


def test_10_double_threat_block(agent):
    """
    SCÉNARIO 10 : Double Menace (Le 7)
    L'adversaire menace horizontalement ET en diagonale en même temps.
    Minimax doit voir la défaite inévitable (score très bas) mais jouer le "moins pire" (bloquer au moins une).
    Ici on teste s'il détecte au moins une menace.
    """
    board = create_empty_board()
    # Horizontale en bas : O O . O (Menace en 2)
    set_piece(board, 5, 0, 1)
    set_piece(board, 5, 1, 1)
    set_piece(board, 5, 3, 1)
    
    print("\n[TEST 10] Blocage critique")
    mask = get_mask(board)
    action = agent.choose_action(board, action_mask=mask)
    assert action == 2, f"ÉCHEC: Doit bloquer en 2, a joué {action}"

if __name__ == "__main__":
    # Exécution manuelle
    t = MinimaxAgent(env=MockEnv())
    try:
        test_01_vertical_threat(t)
        test_02_horizontal_threat_right(t)
        test_03_horizontal_threat_left(t)
        test_04_diagonal_threat_positive(t)
        test_05_win_over_block(t)
        test_06_split_threat(t)
        test_07_prevent_setup(t)
        test_08_full_board_mess(t)

        test_10_double_threat_block(t)
        print("\n✅ TOUS LES TESTS SONT PASSÉS ! (Votre Agent est un Roc)")
    except AssertionError as e:
        print(f"\n❌ {e}")