import numpy as np
import random
from strategie.evaluation import Evaluation  
from strategie.transposition_table import TableDeTransposition


class MinimaxStrategy:
    """
    Implémente la stratégie Minimax pour le jeu de plateau, en prenant en compte différentes profondeurs de recherche
    selon la difficulté choisie. Cette classe permet d'évaluer les meilleurs mouvements possibles en fonction de 
    l'état actuel du plateau et de la couleur des pièces jouées.

    Attributs:
        plateau (Plateau): L'objet représentant l'état actuel du jeu.
        couleur (str): Couleur des pièces de l'IA ('B' pour blanc, 'N' pour noir).
        couleur_adverse (str): Couleur des pièces de l'adversaire.
        profondeur (int): Niveau de profondeur de l'algorithme Minimax, déterminé par la difficulté du jeu.
        evaluation (Evaluation): Objet d'évaluation qui permet de calculer les scores des configurations de plateau.

    Méthodes:
        generer_coups_possibles(plateau): Génère tous les coups possibles à partir de la position actuelle des pièces.
        choisir_coup(): Sélectionne le meilleur coup possible en utilisant l'algorithme Minimax.
        minmax(plateau, profondeur, maximisant, alpha, beta): Implémentation récursive de l'algorithme Minimax avec élagage alpha-beta.
        choisir_coup_aleatoire(plateau): Choix d'un coup aléatoire si aucun coup optimal n'est trouvé ou pour diversifier le jeu.
    """
    
    def __init__(self, plateau, couleur, difficulte='moyen'):
        self.plateau = plateau
        self.couleur = couleur
        self.difficulte = difficulte
        self.couleur_adverse = 'N' if couleur == 'B' else 'B'
        if difficulte == 'difficile':
            self.profondeur = 4
        elif difficulte == 'moyen':
            self.profondeur = 3
        elif difficulte == 'facile':
            self.profondeur = 2
        elif difficulte == 'tres_facile':
            self.profondeur = 1
        else:
            raise ValueError(f"Difficulté non reconnue: {difficulte}")

        self.evaluation = Evaluation(plateau, couleur, difficulte)
        self.transposition_table = TableDeTransposition()

    def generer_coups_possibles(self, plateau):
        """
        Génère et retourne une liste des coups possibles en se basant sur les espaces vides autour des pierres déjà placées sur le plateau.
    
        Entrée:
            plateau (Plateau): L'objet représentant l'état actuel du jeu.

        Sortie:
            list: Liste des tuples (x, y) représentant les coordonnées des coups possibles.

        """
        coords = []
        try:
            for x in range(plateau.taille):
                for y in range(plateau.taille):
                    if plateau.plateau[x][y] != '.':
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille and plateau.plateau[nx][ny] == '.':
                                    coords.append((nx, ny))
        except IndexError as e:
            print(f"Erreur d'index hors limite : {e}")
        return list(set(coords))

    def choisir_coup(self):
        """
        Sélectionne le meilleur coup possible en utilisant l'algorithme Minimax avec élagage alpha-beta.
    
        Sortie:
            tuple: Coordonnées (x, y) du meilleur coup détecté, ou None si aucun coup n'est possible.
        """
        alpha, beta = float('-inf'), float('inf')
        meilleur_score = float('-inf')
        meilleur_coup = None

        # Retourne un coup aléatoire directement pour la difficulté très facile
        if self.difficulte == 'tres_facile':
            return self.choisir_coup_aleatoire(self.plateau)
        
        try:
            coups_possibles = self.generer_coups_possibles(self.plateau)

            for coup in coups_possibles:
                plateau_temp = self.plateau.simuler_coup(coup, self.couleur)
                score, _ = self.minmax(plateau_temp, self.profondeur - 1, False, alpha, beta)

                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = coup
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        except Exception as e:
            print(f"Erreur inattendue lors du choix du coup : {e}")
            meilleur_coup = self.choisir_coup_aleatoire(self.plateau) 
            if meilleur_coup is None:
                print("Aucun coup possible trouvé après erreur.")
                return None

        return meilleur_coup if meilleur_coup is not None else self.choisir_coup_aleatoire(self.plateau)

    def minmax(self, plateau, profondeur, maximisant, alpha, beta):
        """
        Fonction récursive de l'algorithme Minimax qui évalue les meilleurs coups possibles jusqu'à une certaine profondeur,
        avec l'élagage alpha-beta pour optimiser la recherche.

        Entrées:
            plateau (Plateau): L'état du plateau après un coup simulé.
            profondeur (int): La profondeur de recherche restante.
            maximisant (bool): Booléen indiquant si l'agent maximise ou minimise le score.
            alpha (float): La meilleure valeur maximale trouvée dans l'arbre au-dessus du nœud courant.
            beta (float): La meilleure valeur minimale trouvée dans l'arbre au-dessus du nœud courant.

        Sorties:
            float: La valeur du meilleur score trouvé.
            tuple: Coordonnées du meilleur coup associé à ce score, ou None si aucun coup n'est trouvé.
        """

        position_key = (str(plateau.plateau), profondeur, maximisant)
        try:
            result = self.transposition_table.rechercher(position_key)
            if result is not None:
                return result
        except KeyError as e:
            print(f"Erreur de clé dans la table de transposition: {e}")
        except Exception as e:
            print(f"Erreur inattendue lors de la recherche dans la table de transposition: {e}")

        if profondeur == 0 or plateau.est_jeu_termine():
            try:
                score = self.evaluation.evaluer(plateau)
            except ValueError as e:
                print(f"Erreur lors de l'évaluation du plateau: {e}")
                return float('-inf'), None  # Ou une autre valeur par défaut selon la logique du jeu
            self.transposition_table.sauvegarder(position_key, (score, None))
            return score, None


        if maximisant:
            meilleur_score = float('-inf')
            meilleur_coup = None
            for coup in self.generer_coups_possibles(plateau):
                plateau_temp = plateau.simuler_coup(coup, self.couleur)
                score, _ = self.minmax(plateau_temp, profondeur - 1, False, alpha, beta)
                score = score[0] if isinstance(score, tuple) else score  # Modification ici
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = coup
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            self.transposition_table.sauvegarder(position_key, (meilleur_score, meilleur_coup))
            return meilleur_score, meilleur_coup
        else:
            meilleur_score = float('inf')
            meilleur_coup = None
            for coup in self.generer_coups_possibles(plateau):
                plateau_temp = plateau.simuler_coup(coup, self.couleur_adverse)
                score, _ = self.minmax(plateau_temp, profondeur - 1, True, alpha, beta)
                score = score[0] if isinstance(score, tuple) else score  # Modification ici
                if score < meilleur_score:
                    meilleur_score = score
                    meilleur_coup = coup
                beta = min(beta, score)
                if alpha >= beta:
                    break
            self.transposition_table.sauvegarder(position_key, (meilleur_score, meilleur_coup))
            return meilleur_score, meilleur_coup


    def choisir_coup_aleatoire(self, plateau):
        """
        Sélectionne un coup aléatoire parmi les espaces vides disponibles sur le plateau. Utilisé comme fallback
        ou pour ajouter de la variabilité au jeu de l'IA.

        Entrée:
            plateau (Plateau): L'objet représentant l'état actuel du jeu.

        Sortie:
            tuple: Coordonnées (x, y) d'un coup aléatoire, ou None si aucun coup n'est disponible.
        """
        coups_possibles = [(x, y) for x in range(plateau.taille) for y in range(plateau.taille) if plateau.plateau[x][y] == '.']
        return random.choice(coups_possibles) if coups_possibles else None