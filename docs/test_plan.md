# Tâche 4.1 : Concevoir le plan de test  

## 1.1 : Que tester  

**1** Tests fonctionnels:  
-On regarde si l'agent joue un coup autorisé en regardant le masque d'action.  
-On regarde si l'agent joue une opportunité immédiate de victoire.  
-On regarde sur un plateau vide si l'agent joue bien sur les colonnes centrales.  

**2** Tests de performance:  
-On regarde si l'agent prend pour chaque coup toujours moins de 3 secondes à jouer.  
-On vérifie qu'au maximum, 348 MB de RAM est utilisé par coup.  

**3** Tests stratégiques:  
-On vérifie que l'agent intelligent gagne au moins 90% de ses parties contre l'agent aléatoire.  
-On vérifie que l'agent bloque une menace de victoire de l'adversaire.  

## Tâche 1.2 : Comment tester 

**1** Pour vérifier les tests fonctionnels:  
-On simule une grille presque pleine et vérifie que l'agent joue bien une colonne autorisée.  
-On simule une grille où l'agent a 3 pions alignées et s'il trouve la victoire immédiatement.  
-On simule une grille vide et on vérifie que l'agent joue bien au centre.  

**2** Pour les tests de performance:  
-On crée une variable qui comptera le temps que prend l'agent pour jouer et vérifiera que pour chaque coup il prend moins de 3 secondes.  
-On regarde la RAM utilisée par le programme.  

**3** Pour les tests stratégiques:  
-On simule 1000 parties et on regarde le pourcentage de victoire.  
-On simule un plateau où l'adversaire a une menace évidente de victoire et vérifie si l'agent bloque bien celle-ci.  

L'agent réussit les tests si :  
-Il gagne au moins 95% des parties contre l'agent aléatoire.  
-Il prend moins de 0.3 secondes par coup pour jouer.  
-Il utilise moins de 50MB de RAM 

