# Partie 1 : Planifier votre stratégie  

## Tâche 3.1 : Conception de la stratégie 

**1** Les règles doivent être vérifiées dans l'ordre suivant :  
-Est-ce possible de gagner immédiatement, si oui jouer le coup gagnant si non:  
-Est-ce qu'au prochain coup, l'adversaire à un coup qui lui permet de gagner, si oui le bloquer si non :  
-Chercher un coup au milieu dans les colonnes centrales.

**2** Les 3 règles les plus importantes :  
-Regarder si un coup permet de gagner immédiatement.  
-Regarder si un coup permet d'empêcher l'adversaire de gagner à son prochain coup.  
-Jouer au centre en particulier la colonne centrale si possible.  

**3** Règles additionnelles:  
-Prévoir s'il est possible de gagner dans 2 coups et donc chercher à aligner 3 pions à ce tour puis un prochain pion au prochain tour pour gagner.  
-Bloquer l'adversaire si celui ci au prochain tour pourra jouer un coup qui entraînera sa victoire au tour d'après quoi qu'il arrive (Ex: l'adversaire parvient à aligner 3 pions et a une case à gauche libre et une case à droite libre, je ne pourrais bloquer ces 2 cases donc il gagnera, par conséquent avant qu'il aligne ses 3 pions je l'en empêche).  

