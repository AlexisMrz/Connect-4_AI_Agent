import random


class RandomAgent:


    def __init__(self, env, player_name=None):
        """Initialise un agent aléatoire """
 
        self.env=env
        self.player_name=player_name
        

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """Utilise la méthode .sample() de PettingZoo"""
        if terminated or truncated:
            action=None
        else:
            
            action=self.env.action_space(self.player_name).sample(action_mask)
            
        return action 

    def choose_action_manual(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """Méthode manuelle avec random"""
        valid_actions = []  
        for index,is_valid in enumerate(action_mask):
            if is_valid==1:
                valid_actions.append(index)  

  
        if not valid_actions:
            return None
        
        action=random.choice(valid_actions)

        return action  