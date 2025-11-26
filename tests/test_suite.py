import numpy as np
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smart_agent import SmartAgent
import time
import tracemalloc

class TestEnv:
    def __init__(self): #Initialisation d'un environnement pour les tests
        self.agents = ["player_0", "player_1"]

    def action_space(self, agent):
        return None

def smart_agent():
    return SmartAgent(env=TestEnv())

def create_mock_observation(board_matrix, mask=None):
 
    if mask is None:
        mask = np.ones(7, dtype=np.int8)
    return {
        "observation": board_matrix,
        "action_mask": mask
    }

def test_forced_move():
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    actions=[0,0,0,0,0,1,0]
    action=Agent.choose_action(board,action_mask=actions)
    assert action==5

def test_win():
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    board[5,0,0]=1
    board[5,1,0]=1
    board[5,2,0]=1
    actions=[1,1,1,1,1,1,1]
    action=Agent.choose_action(board,action_mask=actions)
    assert action==3

def test_central():
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    actions=[1,1,1,1,1,1,1]
    assert Agent.choose_action(board,action_mask=actions)==3
    actions=actions=[1,1,1,0,1,1,1]
    assert Agent.choose_action(board,action_mask=actions) in [2,4]


def test_time():
    Agent=smart_agent()
    board=np.zeros((6,7,2))
    for r in range(6): #Remplissage de certaines cases du tableau
        for c in range(7):
            if (r+c) % 2 == 0: board[r, c, 0] = 1
            else: board[r, c, 1] = 1
    actions=[1,1,1,1,1,1,1]
    start_time=time.time()
    Agent.choose_action(board,action_mask=actions)
    end_time=time.time()
    assert (end_time-start_time)<0.3

def test_memory_leak_full_game():
    Agent=smart_agent()
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    board = np.zeros((6, 7, 2), dtype=int)
    mask = [1, 1, 1, 1, 1, 1, 1]
    for i in range(50):
        col = i % 7
        row = i % 6
        board[row, col, 0] = 1
        Agent.choose_action(board, action_mask=mask)
    snapshot2 = tracemalloc.take_snapshot()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / 1024 / 1024    
    assert peak_mb<10

def test_block_move():
    Agent=smart_agent()
    board= np.zeros((6, 7, 2), dtype=int)
    for i in range(3,6):
        board[i,0,1]=1
    actions=[1, 1, 1, 1, 1, 1, 1]
    assert Agent.choose_action(board,action_mask=actions)==0