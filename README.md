# Projet IA - Jeu de Gomoku

## Auteurs
KADIC Anaïs & Gravil Athenaïs

## Description du projet
Ce projet, réalisé en Licence 3 à l'Université Paris-Cité, vise à développer une intelligence artificielle capable de jouer au jeu de Gomoku contre un joueur humain. Le Gomoku est un jeu de stratégie où le but est d'aligner cinq pierres de sa couleur sur un plateau de jeu.

## Objectif 

## Objectifs du Projet

Le projet vise à développer et à tester une intelligence artificielle pour le jeu de Gomoku, en accomplissant les tâches suivantes :

- **Implémentation de la boucle de jeu pour deux joueurs humains** : Permettre à deux joueurs humains de jouer l'un contre l'autre sur le même ordinateur.

- **Implémentation de l'algorithme Minimax** :
  - Développer une version de base de l'algorithme Minimax pour permettre à l'IA de calculer les meilleurs coups.

- **Intégration de l'IA dans le jeu** :
  - Remplacer un joueur humain par l'ordinateur utilisant l'algorithme Minimax pour automatiser le processus de prise de décision.

- **Optimisation de l'algorithme Minimax** :
  - Implémenter et intégrer l'élagage α-β pour réduire le nombre de nœuds évalués dans l'arbre de jeu, améliorant ainsi l'efficacité de l'algorithme.

- **Différents niveaux de difficulté de l'IA** :
  - Proposer plusieurs profondeurs de recherche pour ajuster la difficulté de l'IA.
  - Utiliser différentes fonctions d'évaluation pour adapter le comportement stratégique de l'IA selon le niveau de difficulté choisi.

- **Organisation de tournois entre IAs** :
  - Réaliser des tournois de parties entre les IA de différentes difficultés pour évaluer leur performance relative, avec au moins 50 tests par couple d'IA.

## Structure du Projet

Le projet est organisé en plusieurs dossiers et fichiers clés :

- **main.py**: Script principal pour démarrer le jeu.

- **plateau/**: Contient la logique du plateau de jeu.

- **joueur/**: Gère les interactions et les décisions des joueurs humains et de l'IA.

- **strategie/**:
  - Implémente les algorithmes Minimax et Alpha-Bêta.
  - Contient la classe de **transposition** qui aide à mémoriser les états déjà évalués pour optimiser les calculs de l'IA.
  - Inclut une classe **d'évaluation** qui fournit différents niveaux d'évaluation stratégique selon la difficulté de l'IA choisie.

- **tournoi/**: Gère l'organisation de matchs et de tournois entre l'IA et les joueurs humains.

- **README.md**: Fournit des informations générales sur le projet, son utilisation et sa configuration.


## Fonctionnalités

Le jeu de Gomoku implémenté dans ce projet propose plusieurs fonctionnalités accessibles dès le lancement de l'application. Voici les principales options disponibles dans le menu initial :

- **Compétition IA contre IA** : Lance une série de matchs automatisés entre différentes configurations d'intelligence artificielle. Cela permet d'évaluer et de comparer les performances de diverses stratégies et niveaux de difficulté.

- **Jouer contre l'IA** : Permet à un joueur humain de défier l'IA dans une partie de Gomoku, offrant une interaction directe avec l'algorithme de jeu.

### Niveaux de Difficulté

Le jeu propose quatre niveaux de difficulté, permettant aux joueurs de toutes compétences de trouver un défi adapté à leur niveau :

- **Très Facile** : Niveau le plus bas, utilisant des décisions aléatoires simples. Idéal pour débutanter ou pour une partie rapide.

- **Facile** : Utilise des heuristiques de base et une profondeur de recherche limitée à 2, offrant un bon point de départ pour les nouveaux joueurs.

- **Moyen** : Augmente la profondeur de recherche à 3, introduisant une stratégie légèrement plus difficile.

- **Difficile** : Le niveau le plus dure avec une profondeur de recherche de 4, destiné aux joueurs expérimentés cherchant à tester leurs compétences contre une IA avancée et stratégique.

Chaque niveau de difficulté ajuste la profondeur de recherche et les fonctions d'évaluation utilisées par l'IA.

## Exécution

Pour démarrer le jeu, naviguez d'abord dans le dossier contenant le dossier GOMOKU. Vous pouvez ensuite lancer le jeu en utilisant la commande suivante dans votre terminal :

```bash
python3 main.py
