# Défi 1 : Algorithme Minimax  

## Tâche 5.1 : Comprendre l'algorithme  

**1** On alterne entre max et min car chaque joueur joue chacun son tour, 
et on suppose que l'adversaire joue de manière optimale donc cherche à 
minimiser les gains de notre agent, tandis que nous cherchons à optimiser les 
gains de notre agent à chaque tour.  

**2** La profondeur (Depth) contrôle le nombre de coups à l'avance que l'IA va anticiper.  
Depth=1 signifie que l'IA anticipe 1 coup à l'avance.  
Depth=4 signifie que l'IA anticipe 4 coups à l'avance.  

**3** Si la profondeur est trop grande, l'IA va devoir explorer beaucoup trop de possibilités, ce nombre évoluant de manière exponentielle et le temps inférieur à 3 secondes obligatoire pour chaque coup ne cera pas respecté.  

**4** L'élagage alpha-betâ attribue à des branches (donc des coups) une étiquette "inutile" car aura déjà trouvé un autre coup maximisant les gains du joueur. Entre autre s'il remarque qu'une branche mène à un gain faible alors qu'une autre mène déjà à un gain élevé, il arrête d'explorer celle-ci.


