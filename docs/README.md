# Partie 1 : Règles du Puissance 4
## Tâche 1.1 : Analyse des règles du jeu
**1** La dimension d'un plateau de Puissance 4 est de 6 lignes et 7 colonnes.  

**2** Un joueur gagne la partie s'il réalise en premier l'alignement(horizontal, vertical ou diagonal) consécutif d'au moins quatre pions de sa couleur.  

**3** Si le plateau est complètement rempli sans gagnant, il y a match nul. 

**4** Il n'est pas possible de placer un pion dans une colonne qui est déjà pleine, c'est un coup non autorisé.   

**5** Il y a 3 issues possibles pour une partie: le joueur 1 gagne, le joueur 2 gagne, il y a match nul.    


## Tâche 1.2 : Analyse des conditions de victoire
**1**
```Python
[[0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [1. 1. 1. 1. 0. 0. 0.]]
``` 
Pions alignés horizontalement
```Python
[[0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]]
``` 
Pions alignés verticalement
```Python
[[0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]
 [0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 1. 0. 0. 0. 0.]
 [0. 0. 0. 1. 0. 0. 0.]]
 ```
Pions en diagonale descendante
 ```Python
[[0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 1. 0. 0. 0.]
 [0. 0. 1. 0. 0. 0. 0.]
 [0. 1. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0.]]
 ```
Pions en diagonale montante  

**2** Pour une position donnée, il y a 4 axes (ou lignes) à vérifier : Horizontal, Vertical, et les deux Diagonales.  

**3** L'algorithme consiste, pour chaque axe, à compter les pions consécutifs identiques de part et d'autre du pion posé.  

On initialise un compteur nul:  

On part du pion posé (compteur+=1)

On se déplace dans une direction tant qu'on trouve le même pion (on incrémente le compteur).

On revient au centre et on se déplace dans la direction opposée (ex: droite) tant qu'on trouve le même pion (on incrémente).

Si le compteur final est >= 4, c'est gagné.  

# Partie 2 : Comprendre PettingZoo  

## Tâche 2.1 : Lire la documentation  

**1** Les 2 agents sont: 'player_0' et 'player_1'.    

**2** La variable action désigne le numéro de colonne dans lequel le joueur qui joue place son pion: c'est un entier variant de 0 à 6 bornes inclues.     

**3** env.agent_iter() est un itérateur qui désigne le joueur qui doit jouer, tour à tour.  
env.step(action) exécute le coup du joueur qui devait jouer et passe au joueur suivant.  

**4** env.last() retourne l'observation (soit l'état de la grille et les coups permis au moment où l'agent joue), la récompense (soit si le coup est bon mauvais ou neutre), la termination et troncation pour savoir si la pertie est terminée et infos.  

**5** La structure de l'observation est dictionnaire contenant la grille (un tenseur de 3 dimensions (6,7,2)) et 'action_mask'. 

**6** action_mask est un vecteur de booléens désignant si le coup dans chaque colonne est autorisé (1) ou non (0) avec l'index du vecteur égal à l'index de action.  

# Partie 3: Décomposition du problème  

## Tâche 3.1: Décomposer l'implémentation de l'agent  

**1** L'agent reçoit la grille actuelle ainsi que 'action_mask' lui indiquant les coups autorisés, donc un dictionnaire contenant 'observation' et 'action_mask'.  

**2** Pour cela on regarde 'action_mask'. Pour chaque index pour lequel 'action_mask' contient un 1, cela correspond à un numéro de colonne où un coup est autorisé, sinon le coup est interdit.  

**3** L'agent évalue les colonnes valides et en fonction de l'algorithme appliqué, il joue dans la colonne la plus propice de le mener à la victoire (déterminée par l'algorithme de recherche).  

**4** L'agent renvoie un entier qui correspond à la colonne où il a placé son pion.  

## Tâche 3.2 : Conception d'algorithme - Progression  

**1** Niveau 0: L'agent joue dans une colonne aléatoire même si celle-ci est pleine.  

**2** Niveau 1: L'agent joue aussi dans une colonne aléatoire mais que si son coup est valide (évite donc les colonnes pleines). 

**3** Niveau 2: L'agent remarque s'il a un coup immédiat qui lui permet de gagner et le joue.  

**4** Niveau 3: L'agent remarque si le prochain coup de l'autre agent lui permettra de gagner immédiatement et bloque son coup.  

**5** Niveau 4: L'agent joue la colonne centrale, essaye d'aligner plusieurs pions.  

**6** Niveau 5: Algorithmes avancés pour jouer plusieurs coups à l'avance.  

## Tâche 3.3 : Définir l'interface de l'agent  

```Python
class Agent:
    #Un constructeur initialisant le nom de l'agent
    def __init__(self,nom):
        self.nom=nom
    def action(self,observation,action_mask):
        #Prend en argument l'état de la grille et choisit un coup valide
        #Renvoie un entier correspondant au numéro de colonne dans laquelle
        #le coup a été joué
```
# Bonus : Ajout d'un agent Minimax combiné à Numba pour augmenter la profondeur de l'algorithme Minimax, mais non déployable sur ML-Arena où l'utilisation du package Numba n'est pas autorisée 











