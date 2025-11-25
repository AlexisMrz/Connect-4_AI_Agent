import numpy as np
import pytest
from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent
from random_agent import RandomAgent
from loguru import logger
import time
class TestEnv:
    def __init__(self):#Initialisation d'un environnement pour les tests
        self.agents = ["player_0", "player_1"]

    def action_space(self, agent):
        return None

def test_get_valid_actions(): #Test de la méthode _get_valid_actions
    agent = SmartAgent(TestEnv())
    mask = [1, 1, 1, 0, 1, 0, 1]
    assert agent._get_valid_actions(mask) == [0, 1, 2, 4, 6]

def test_get_next_row(): 
    agent = SmartAgent(TestEnv())
    board = np.zeros((6, 7, 2), dtype=int)
    assert agent._get_next_row(board, 0) == 5
    board[5, 0, 0] = 1
    assert agent._get_next_row(board, 0) == 4
    for r in range(6):
        board[r, 1, 0] = 1
    assert agent._get_next_row(board, 1) is None

def test_check_win_horizontal():
    agent = SmartAgent(TestEnv())
    board = np.zeros((6, 7, 2), dtype=int)
    board[5, 0, 0] = 1
    board[5, 1, 0] = 1
    board[5, 2, 0] = 1
    assert agent._check_win_from_position(board, 5, 3, channel=0) == True
    assert agent._check_win_from_position(board, 4, 3, channel=0) == False

def test_find_winning_move():
    agent = SmartAgent(env=TestEnv())
    board = np.zeros((6, 7, 2), dtype=int)
    board[5, 0, 0] = 1
    board[5, 1, 0] = 1
    board[5, 3, 0] = 1
    valid_actions = [0, 1, 2, 3, 4, 5, 6]
    assert agent._find_winning_move(board, valid_actions, channel=0) == 2

def test_smart_beats_random():
    env = connect_four_v3.env(render_mode=None)
    env.reset() 
    smart = SmartAgent(env, "Smart")
    random_bot = RandomAgent(env, "Random")
    wins = 0
    games = 50
    for i in range(games):
        env.reset()
        winner = None 
        for agent_id in env.agent_iter():
            obs, reward, term, trunc, _ = env.last()
            
            if term or trunc:
                if reward == 1:
                    winner = agent_id
                
                env.step(None)
            else:
                mask = obs["action_mask"]
                if agent_id == "player_0":
                    action = smart.choose_action(obs, action_mask=mask)
                else:
                    action = random_bot.choose_action_manual(obs, action_mask=mask)
                env.step(action)
        
        
        if winner == "player_0":
            wins += 1

    assert wins >= 40


def stat_games(num_games=100):#Statistiques avec maintenant l'agent
    #intelligent pour num_games parties
    logger.remove() #Pour éviter qu'à chaques parties la fonction affiche tous
    #les log ce qui est visuellement très lourd 
    env = connect_four_v3.env(render_mode=None) #render_mode non visuel pour accéler le processus
    env.reset()
    Length_game=[]
    Smart_Agent_0=SmartAgent(env,"player_0")
    dumb_player_1=RandomAgent(env,"player_1")

    mapping_agents={"player_0":Smart_Agent_0,"player_1":dumb_player_1}
 
    player0_win_count=0
    player1_win_count=0
    
    mean_moves=0
    num_draw=0
    for i in range(num_games):
        moves_count=0
        env.reset()

        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
                if reward == 1:
                    
                    if agent=="player_0":
                        player0_win_count+=1
                    elif agent=="player_1":
                        player1_win_count+=1
                elif reward == 0:
                    
                    num_draw+=1
            else:
                current_player=mapping_agents[agent]
                mask = observation["action_mask"]
          
                action = current_player.choose_action(observation,reward,termination,truncation,info,mask)
                moves_count+=1
            env.step(action)
        Length_game.append(moves_count)
        mean_moves+=moves_count/num_games

    env.close()
    return player0_win_count,player1_win_count,int(mean_moves),min(Length_game),max(Length_game),num_draw
           #On retourne les statistiques



