import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smart_agent import SmartAgent
import time
import tracemalloc

class TestEnv:
    """Initialisation d'un environnement pour les tests"""
    def __init__(self): 
        self.agents = ["player_0", "player_1"]

    def action_space(self, agent):
        return None

def smart_agent():
    return SmartAgent(env=TestEnv())

def test_forced_move():
    """Teste si l'agent joue bien un coup valide si presque
    toutes les colonnes sont pleines"""
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    actions=[0,0,0,0,0,1,0]
    assert Agent.choose_action(board,action_mask=actions)==5
    actions=actions=[0,1,0,0,0,0,0]
    assert Agent.choose_action(board,action_mask=actions)==1

def test_win():
    """Teste si l'agent remarque une opportunité de victoire immédiate"""
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    board[5,0,0]=1
    board[5,1,0]=1
    board[5,2,0]=1
    actions=[1,1,1,1,1,1,1]
    action=Agent.choose_action(board,action_mask=actions)
    assert action==3

def test_central():
    """Teste si l'agent favorise bien les colonnes du milieu,
    s'il n'y a pas d'autres coups intéressants à jouer"""
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    actions=[1,1,1,1,1,1,1]
    assert Agent.choose_action(board,action_mask=actions)==3
    actions=actions=[1,1,1,0,1,1,1]
    assert Agent.choose_action(board,action_mask=actions) in [2,4]

def test_time():
    """Teste si l'agent met moins de 0.3 secondes à jouer"""
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    """Remplissage de certaines cases du tableau pour que l'agent
    ait à réfléchir un peu"""
    for r in range(6): 
        for c in range(7):
            if (r+c) % 2 == 0: board[r, c, 0] = 1
            else: board[r, c, 1] = 1
    actions=[1,1,1,1,1,1,1]
    start_time=time.time()
    Agent.choose_action(board,action_mask=actions)
    end_time=time.time()
    assert (end_time-start_time)<0.3

def test_memory_leak_full_game():
    """Teste si le pic de mémoire utilisée n'excède pas 10MB"""
    Agent=smart_agent()
    tracemalloc.start()
    board = np.zeros((6, 7, 2), dtype=int)
    mask = [1, 1, 1, 1, 1, 1, 1]
    for i in range(50):
        col = i % 7
        row = i % 6
        board[row, col, 0] = 1
        Agent.choose_action(board, action_mask=mask)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / 1024 / 1024 #On transforme les octets en méga-octets
    """variable contenant le pic de mémoire utilisée"""   
    assert peak_mb<10

def test_block_move():
    """Teste si l'agent bloque bien une menance évidente de l'adversaire"""
    Agent=smart_agent()
    board= np.zeros((6, 7, 2), dtype=int)
    for i in range(3,6):
        board[i,0,1]=1
    actions=[1, 1, 1, 1, 1, 1, 1]
    assert Agent.choose_action(board,action_mask=actions)==0