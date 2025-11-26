from pettingzoo.classic import connect_four_v3


def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """

    for i in range(6):
        for j in range(7):
            if observation[i,j,0]==1:
                print('X',end="")
            elif observation[i,j,1]==1:
                print('O',end="")
            else:
                print('.',end="")
        print()
    pass


env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])


    env.step(3)
    if agent == env.agents[0]:
        break

env.close()