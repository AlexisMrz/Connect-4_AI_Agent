# Analyse de performance : SmartAgent

## 1. Taux de victoire
Sur 100000 parties contre un RandomAgent :
* **SmartAgent :** 99% de victoires.

* **Conclusion :** L'agent domine totalement le jeu aléatoire. Les seules défaites possibles viennent de situations très rares où le hasard aligne 4 pions avant que SmartAgent n'ait eu besoin de bloquer (ou un piège accidentel).

## 2. Efficacité de la stratégie
* **Règle 1 (Victoire) :** Se déclenche systématiquement pour finir la partie. 
* **Règle 2 (Blocage) :** Très fréquente en milieu de partie. Empêche toutes les victoires faciles de l'adversaire.
* **Règle 3 (Double Menace) :** Plus rare contre un agent aléatoire (car la partie finit vite), mais garantit la victoire au tour N+2.
* **Règle 4 (Centre) :** Fondamentale. En contrôlant la colonne 3 dès le début, l'agent se crée plus d'opportunités horizontales et diagonales.

## 3. Cas d'échec (Limites)
L'agent actuel ne regarde qu'à **1 coup à l'avance** (Profondeur 1).
* Il peut perdre contre un humain ou un Minimax qui préparerait un piège sur 3 tours (ex: "Si je bloque ici, il va jouer là, et gagner au tour d'après").
* Il ne détecte pas si son coup de "Blocage" donne immédiatement une victoire à l'adversaire juste au-dessus.

## 4. Améliorations possibles
* **Algorithme Minimax :** Pour regarder X tours à l'avance.
* **Évitement de piège (Bad Move) :** Vérifier "Si je joue colonne X, est-ce que je donne la victoire à l'adversaire en (row-1, X) ?".