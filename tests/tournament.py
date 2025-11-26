import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smart_agent import SmartAgent
from random_agent import RandomAgent
from pettingzoo.classic import connect_four_v3
from loguru import logger



def run_tournament(num_games=100):

    env=connect_four_v3.env(render_mode=None)
    env.reset()
    Brillant_Agent=SmartAgent(env,player_name="player_0")
    Dumb_Agent=RandomAgent(env,player_name="player_1")

    logger.info(f"Début du tournoi entre {Brillant_Agent} et {Dumb_Agent} en {num_games} rounds")
    wins = {Brillant_Agent.player_name: 0, Dumb_Agent.player_name: 0, "Draw": 0}
    for i in range(num_games):
        env.reset()
        if i%2==0:
            mapping_agents={"player_0":Brillant_Agent,"player_1":Dumb_Agent}
        else:
            mapping_agents={"player_0":Dumb_Agent,"player_1":Brillant_Agent}
        game_winner=None
        for agent_id in env.agent_iter():
            obs, reward, term, trunc, _ = env.last()
            
            if term or trunc:
                if reward == 1:
                    
                    winner_obj = mapping_agents[agent_id]
                    game_winner = winner_obj.player_name
                elif reward == 0:
                    pass
                env.step(None)
            else:
                current_bot = mapping_agents[agent_id]
                mask = obs["action_mask"]
                
                action = current_bot.choose_action(obs, action_mask=mask)
          
                env.step(action)
            
        if game_winner:
            wins[game_winner] += 1
        else:
            wins["Draw"] += 1

    logger.info(f"number of wins player_0: {wins['player_0']}, number of wins player_1: {wins['player_1']}, number of draws: {wins['Draw']} ")
 











