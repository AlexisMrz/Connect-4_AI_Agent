import numpy as np
import sys
import os
import time
from tqdm import tqdm
from loguru import logger

"""Affrontement entre l'agent MCTS et l'agent Minimax combiné à Numba"""

logger.remove()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pettingzoo.classic import connect_four_v3
from minimax_agent import Agent as MCTSAgent2
from minimax_agent import MinimaxAgent as NumbaAgent


def run_numba_vs_mcts(num_games=20):
    env = connect_four_v3.env(render_mode=None)
    env.reset()

    t0 = time.time()
    agent_numba = NumbaAgent(env, player_name="Numba")

    agent_mcts = MCTSAgent2(env, player_name="MCTS")

    logger.info(f"\nDUEL : {agent_numba.player_name} vs {agent_mcts.player_name}")
    logger.info(f"Tours : {num_games}")
    logger.info("-" * 60)

    stats = {
        agent_numba.player_name: {"wins": 0, "total_time": 0, "moves": 0},
        agent_mcts.player_name: {"wins": 0, "total_time": 0, "moves": 0},
        "Draw": 0
    }

    pbar = tqdm(range(num_games), desc="Combats en cours", unit="match")
    #Barre de chargement des parties
    for i in pbar:
        env.reset()
        
        if i % 2 == 0:
            players = {"player_0": agent_numba, "player_1": agent_mcts}
        else:
            players = {"player_0": agent_mcts, "player_1": agent_numba}

        game_winner = None
        
        for agent_id in env.agent_iter():
            obs, reward, term, trunc, _ = env.last()

            if term or trunc:
                if reward == 1:
                    winner_obj = players[agent_id]
                    game_winner = winner_obj.player_name
                env.step(None)
            else:
                current_agent = players[agent_id]
                mask = obs["action_mask"]
                
                start = time.time()
                try:
                    action = current_agent.choose_action(obs, action_mask=mask)
                except Exception as e:
                    logger.error(f"Crash {current_agent.player_name}: {e}")
                    env.step(None)
                    continue
                
                duration = time.time() - start
                
                stats[current_agent.player_name]["total_time"] += duration
                stats[current_agent.player_name]["moves"] += 1
                
                env.step(action)

        if game_winner:
            stats[game_winner]["wins"] += 1
        else:
            stats["Draw"] += 1
            
        pbar.set_postfix({
            "Numba": stats[agent_numba.player_name]["wins"],
            "MCTS": stats[agent_mcts.player_name]["wins"]
        })

    logger.info("\n" + "="*60)
    logger.info(f"RÉSULTATS DU TOURNOI")
    logger.info("="*60)
    
    def print_stats(name):
        s = stats[name]
        wins = s["wins"]
        avg_time = s["total_time"] / s["moves"] if s["moves"] > 0 else 0
        logger.succes(f"{name:<18} : {wins} victoires")
        logger.info(f"   Temps moyen/coup : {avg_time*1000:.1f} ms")
        logger.info("-" * 30)

    print_stats(agent_numba.player_name)
    print_stats(agent_mcts.player_name)
    
    logger.info(f"Matchs Nuls : {stats['Draw']}")
    logger.info("="*60)

if __name__ == "__main__":
    run_numba_vs_mcts(20)