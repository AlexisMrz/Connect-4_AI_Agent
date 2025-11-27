import numpy as np
import time
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from minimax_agent import MinimaxAgent
import tracemalloc


class TestEnv:
    def __init__(self):
        self.agents = ["player_0", "player_1"]
    
    def action_space(self, agent):
        return None 

def agent():
    return MinimaxAgent(env=TestEnv(), depth=4)


def test_performance_time(): #Test de performance
    Agent=agent()
    board = np.zeros((6, 7, 2))
    

    for r in range(3, 6): 
        for c in range(7):
            if (r + c) % 2 == 0:
                board[r, c, 0] = 1 
            else:
                board[r, c, 1] = 1 

    actions_mask = np.ones(7)

    
    start_time = time.time()
    
    
    action = Agent.choose_action(board, action_mask=actions_mask)
    
    end_time = time.time()
    duration = end_time - start_time
    
    
    assert duration < 0.3

def test_memory_peak():#Test de mémoire
    Agent=agent()
    board = np.zeros((6, 7, 2), dtype=np.int8)
    
    for r in range(3, 6): 
        for c in range(7):
            if (r + c) % 2 == 0:
                board[r, c, 0] = 1
            else:
                board[r, c, 1] = 1
                
    actions_mask = np.ones(7)

    tracemalloc.start()

    action = Agent.choose_action(board, action_mask=actions_mask)

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    peak_mb = peak / 1024 / 1024

    assert peak_mb < 384