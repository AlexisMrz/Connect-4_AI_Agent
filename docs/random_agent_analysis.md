# Analyse des performances de l'Agent Aléatoire

## Protocole de test
- **Nombre de parties jouées :** 100
- **Adversaires :** RandomAgent vs RandomAgent

## Résultats Statistiques

### 1. Distribution des victoires
- **Joueur 1 (Commence) :** ~55% de victoires.
- **Joueur 2 (Suit) :** ~45% de victoires.
- **Matchs Nuls :** ~0.5% (Très rare).

### 2. Analyse
Le joueur qui commence (Player 0) possède un avantage significatif (environ 10% de plus de victoires), même en jouant totalement au hasard. Cela confirme l'avantage structurel du premier coup ("First Mover Advantage") au Puissance 4 : il a toujours l'initiative et pose ses pions en premier.

### 3. Durée des parties
- **Moyenne :** 21 coups.
- **Minimum :** 7-8 coups (Victoire rapide par hasard).
- **Maximum :** 41-42 coups (Plateau quasi plein).