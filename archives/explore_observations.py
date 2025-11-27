from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation['observation'].shape)
    print("Action mask:", observation['action_mask'])

    env.step(3)
    break

env.close()
"""
1. Le tableau est un tenseur de dimension (6,7,2).
2. Il y a 6 lignes, 7 colonnes et la dernière cordonnée indique si c'est la
grille de l'agent 0 ou de l'agent 1.
3.Les valeurs possibles dans le tableau sont 0 ou 1.
"""
