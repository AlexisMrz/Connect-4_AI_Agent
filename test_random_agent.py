from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent
from random_agent import WeightedRandomAgent
from loguru import logger
import time


def run_demo_game(): #Test visuel d'une partie entre 2 agents de la classe RandomAgent
    env = connect_four_v3.env(render_mode="human") 
    env.reset(seed=42)

    dumb_player_0 = RandomAgent(env, "player_0")
    dumb_player_1 = RandomAgent(env, "player_1")
    mapping_agents = {"player_0": dumb_player_0, "player_1": dumb_player_1}
    #On associe player_0 l'agent 0 de PettingZoo à notre agent de la
    #classe RandomAgent et idem pour player_1
    start_time = time.time() #Pour mesurer le temps d'une partie

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
            if reward == 1:
                logger.info(f"Victoire de {agent} !") 
            elif reward == 0:
                logger.info("Match Nul !")
        else:
            current_player = mapping_agents[agent]
            mask = observation["action_mask"]
            action = current_player.choose_action(observation, reward, termination, truncation, info, mask)
            #Méthode de la classe RandomAgent avec le module Random
            logger.info(f"{current_player.player_name} ({agent}) joue colonne {action}")

        env.step(action)

    end_time = time.time()
    env.close()
    logger.info(f"Durée : {end_time-start_time:.2f} secondes\n")


def stat_games(num_games=100):#Statistiques pour num_games parties
    env = connect_four_v3.env(render_mode=None) #render_mode non visuel pour accéler le processus
    
    Length_game=[]
    dumb_player_0=RandomAgent(env,"player_0")
    dumb_player_1=RandomAgent(env,"player_1")

    mapping_agents={"player_0":dumb_player_0,"player_1":dumb_player_1}
 
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
