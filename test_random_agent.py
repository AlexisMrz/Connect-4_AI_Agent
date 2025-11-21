from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent
import time
import math

env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)
#Initialisation des 2 agents "bêtes" de la classe RandomAgent
dumb_player_0=RandomAgent(env,"lvl_0_Alpha")
dumb_player_1=RandomAgent(env,"lvl_0_Beta")

mapping_agents={"player_0":dumb_player_0,"player_1":dumb_player_1}
#On attribue un nom de joueur de PettingZoo à chaque agent

debut=time.time()
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        current_player=mapping_agents[agent]
        mask = observation["action_mask"]
        #On a le choix entre les 2 méthodes ici: la méthode random avec le 
        #module random de Python ou la méthode aléatoire utilisant
        #.sample() de PettingZoo
        action = current_player.choose_action_manual(observation,reward,termination,truncation,info,mask)
        print(f"{agent} plays column {action}")

    env.step(action)
fin=time.time()

env.close()
print(f"{fin-debut:.2f}")

def stat_games(num_games=100):
    env = connect_four_v3.env(render_mode=None) 
    
    Length_game=[]
    dumb_player_0=RandomAgent(env,"lvl_0_Alpha")
    dumb_player_1=RandomAgent(env,"lvl_0_Beta")

    mapping_agents={"player_0":dumb_player_0,"player_1":dumb_player_1}
    average_time=0
    player0_win_count=0
    player1_win_count=0
    
    mean_moves=0
    num_draw=0
    for i in range(num_games):
        moves_count=0
        env.reset()
        start_time=time.time()
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
          
                action = current_player.choose_action_manual(observation,reward,termination,truncation,info,mask)
                moves_count+=1
            env.step(action)
        Length_game.append(moves_count)
        mean_moves+=moves_count/num_games
            

            
        end_time=time.time()
        average_time+=(end_time-start_time)/num_games

    env.close()
    return player0_win_count,player1_win_count,mean_moves,min(Length_game),max(Length_game),num_draw
print(stat_games(100))