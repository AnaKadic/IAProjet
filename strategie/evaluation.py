# strategies.py

import numpy as np

class Evaluation:
    """
    Classe d'évaluation pour une stratégie de jeu.
    Permet d'évaluer les positions sur le plateau en fonction de la couleur des pièces,
    et ajuste les évaluations selon la difficulté spécifiée ('facile', 'moyen', 'difficile').

    Attribues:
        plateau (object): Instance de la classe Plateau représentant l'état actuel du jeu.
        couleur (str): Couleur des pièces pour lesquelles l'évaluation est réalisée.
        couleur_adverse (str): Couleur des pièces adverses.
        difficulte (str): Niveau de difficulté de l'évaluation ('facile', 'moyen', 'difficile').
        profondeur (int): Profondeur de l'évaluation, ajustée selon la difficulté.
        evaluer (function): Fonction d'évaluation active, déterminée par la difficulté.
    """

    def __init__(self, plateau, couleur, difficulte='moyen'):
        self.plateau = plateau
        self.couleur = couleur
        self.couleur_adverse = 'N' if couleur == 'B' else 'B'
        self.set_difficulte(difficulte)

    def set_difficulte(self, difficulte):
        """
        Définit le niveau de difficulté de l'évaluation et ajuste les paramètres liés.

        Entrée:
            difficulte (str): Niveau de difficulté ('facile', 'moyen', 'difficile').

        """
        valid_difficulties = ['facile', 'moyen', 'difficile']
        if difficulte not in valid_difficulties:
            raise ValueError(f"Difficulté '{difficulte}' non reconnue. Choix valides: {valid_difficulties}")
        self.difficulte = difficulte
        self.profondeur = 4 if difficulte == 'difficile' else 2 if difficulte == 'moyen' else 1
        self.evaluer = getattr(self, f'evaluer_{difficulte}')

    def evaluer_facile(self, plateau):
        """
        Évalue le plateau de manière simple en comptant les pierres alignées directement pour la couleur spécifiée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score basé sur le nombre de pierres alignées directement.

       """
        return self.compter_pierres_alignees(plateau, self.couleur)

    def evaluer_moyen(self, plateau):
        """
        Évalue le plateau en utilisant une logique d'évaluation modérée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score calculé en fonction de diverses configurations de pierres sur le plateau.

        """
        return self.evaluer_plateau(plateau)

    def evaluer_difficile(self, plateau):
        """
        Effectue une évaluation difficile du plateau en utilisant des stratégies avancées.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score calculé en utilisant des stratégies d'évaluation.


        """
        return self.evaluation_complexe(plateau, self.couleur)

    def compter_pierres_alignees(self, plateau, couleur):
        """
        Calcule le nombre de pierres alignées directement en quatre directions (horizontal, vertical et deux diagonales),
        augmentant le score pour chaque alignement trouvé.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            couleur (str): Couleur des pierres à évaluer.

        Sortie:
            score (int): Total des pierres alignées pour la couleur spécifiée.
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, Vertical et deux Diagonales
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == couleur:
                    for dx, dy in directions:
                        alignement = 1
                        for i in range(1, 5):
                            x, y = ligne + dx * i, colonne + dy * i
                            if 0 <= x < plateau.taille and 0 <= y < plateau.taille and plateau.plateau[x][y] == couleur:
                                alignement += 1
                            else:
                                break
                        score += alignement
        return score

    def evaluer_plateau(self, plateau):
        """
        Évalue le plateau en calculant un score basé sur les alignements offensifs des pierres de la couleur spécifiée,
        tout en pénalisant les configurations avantageuses pour l'adversaire.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score total basé sur l'évaluation des configurations des pierres sur le plateau.
        """
        score = 0
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == self.couleur:
                    score += self.evaluer_alignement(plateau, ligne, colonne, self.couleur)
                elif plateau.plateau[ligne][colonne] != '.':
                    score -= self.evaluer_alignement(plateau, ligne, colonne, plateau.plateau[ligne][colonne])
        
        # Ajout d'une évaluation défensive
        score += self.evaluer_besoins_defensifs(plateau, self.couleur)

        return score

    def evaluer_besoins_defensifs(self, plateau, couleur):
        """
        Évalue les besoins défensifs sur le plateau en identifiant les menaces potentielles de l'adversaire.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            couleur (str): Couleur des pierres pour lesquelles les défenses sont évaluées.

        Sortie:
            score_defensif (int): Score défensif basé sur les configurations menaçantes de l'adversaire.
        """
        score_defensif = 0
        couleur_adverse = 'N' if couleur == 'B' else 'B'
        threat_multiplier = -100  
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == couleur_adverse:
                    for dx, dy in directions:
                        alignement, espaces = 0, 0
                        for i in range(1, 5):
                            x, y = ligne + dx * i, colonne + dy * i
                            if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                                if plateau.plateau[x][y] == couleur_adverse:
                                    alignement += 1
                                elif plateau.plateau[x][y] == '.':
                                    espaces += 1
                                else:
                                    break
                            else:
                                break
                        if alignement + espaces >= 4:
                            score_defensif += threat_multiplier * (alignement ** 2)
    
        return score_defensif


    def verifier_menace(self, plateau, ligne, colonne, dx, dy, couleur_adverse):
        """
        Vérifie si une menace sérieuse est présente à partir d'une position donnée dans une direction spécifiée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            ligne (int): Ligne de départ pour la vérification.
            colonne (int): Colonne de départ pour la vérification.
            dx (int): Déplacement en x pour la direction de vérification.
            dy (int): Déplacement en y pour la direction de vérification.
            couleur_adverse (str): Couleur des pierres adverses à vérifier.

        Sortie:
            bool: Retourne True si une menace sérieuse est détectée, sinon False.
        """
        alignement = 1
        for i in range(1, 5):
            x, y = ligne + dx * i, colonne + dy * i
            if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                if plateau.plateau[x][y] == couleur_adverse:
                    alignement += 1
                else:
                    break
            else:
                break
        return alignement >= 4  # Vérifie s'il y a une menace sérieuse


    def evaluer_difficile(self, plateau):
        """
        Évalue le plateau avec des critères plus complexes pour une stratégie avancée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score total basé sur des critères avancés d'évaluation.
        """
        score = 0
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == self.couleur:
                    score += 20  # Score chaque pierre présente
                    score += self.evaluer_alignement(plateau, ligne, colonne, self.couleur)  # Alignements existants
                elif plateau.plateau[ligne][colonne] != '.':
                    score -= 10  # Pénalise les pierres adverses

        score += self.evaluer_menaces_avancees(plateau, self.couleur)  # Menaces potentielles et double menaces
        score += self.evaluer_potentiel_defensif(plateau, self.couleur)  # Besoins défensifs
        return score

    def evaluer_menaces_avancees(self, plateau, couleur):
        """
        Évalue les configurations avancées pour détecter des doubles menaces potentielles.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            couleur (str): Couleur des pierres évaluées.

        Sortie:
            score (int): Score basé sur le potentiel de menaces doubles.

        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == couleur:
                    for dx, dy in directions:
                        alignement, ouverts = 1, 0
                        for i in range(1, 5):
                            x, y = ligne + dx * i, colonne + dy * i
                            if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                                if plateau.plateau[x][y] == couleur:
                                    alignement += 1
                                elif plateau.plateau[x][y] == '.':
                                    ouverts += 1
                                if alignement + ouverts >= 5:
                                    score += 100 * alignement  # Incitatif pour double menace
                                break
        return score


    def evaluer_potentiel_defensif(self, plateau, couleur):
        """
        Évalue les configurations défensives sur le plateau en identifiant les potentielles menaces adverses et en anticipant les configurations futures.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            couleur (str): La couleur pour laquelle les défenses sont évaluées.

        Sortie:
            score_defensif (int): Score total basé sur les configurations défensives potentielles.

       """
        score_defensif = 0
        couleur_adverse = 'N' if couleur == 'B' else 'B'
        malus_defensif = -200  # Pénalité pour configurations menaçantes de l'adversaire
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == '.':
                    for dx, dy in directions:
                        alignement, espaces = 0, 0
                        for i in range(-4, 5):  # Étendre la recherche pour anticiper les menaces futures
                            x, y = ligne + dx * i, colonne + dy * i
                            if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                                if plateau.plateau[x][y] == couleur_adverse:
                                    alignement += 1
                                elif plateau.plateau[x][y] == '.':
                                    espaces += 1
                            else:
                                break

                        if alignement >= 3 and espaces + alignement >= 5:
                            score_defensif += malus_defensif * (alignement ** 2)  # Renforce la pénalité basée sur l'alignement

    
        return score_defensif
    
    def check_menace_imminente(self, plateau, ligne, colonne, dx, dy, couleur_adverse):
        """
        Vérifie la présence d'une menace imminente en ligne dans une direction donnée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            ligne (int): Ligne de départ pour la vérification.
            colonne (int): Colonne de départ pour la vérification.
            dx (int): Déplacement en x pour la direction de vérification.
            dy (int): Déplacement en y pour la direction de vérification.
            couleur_adverse (str): Couleur des pierres adverses à vérifier.

        Sortie:
            bool: True si une menace de victoire imminente est détectée, False sinon.
        """
        alignement = 0
        for i in range(1, 5):
            x, y = ligne + dx * i, colonne + dy * i
            if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                if plateau.plateau[x][y] == couleur_adverse:
                    alignement += 1
                elif plateau.plateau[x][y] != '.':
                    break
            else:
                break
        return alignement >= 3
 
    
    def evaluer_alignement(self, plateau, ligne, colonne, couleur):
        """
        Calcule le score basé sur l'alignement des pierres à partir d'une position spécifique sur le plateau.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            ligne (int): Ligne de la pierre à évaluer.
            colonne (int): Colonne de la pierre à évaluer.
            couleur (str): Couleur des pierres à évaluer.

        Sortie:
            score (int): Score calculé basé sur l'alignement des pierres.
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in directions:
            alignement = 1
            for i in range(1, 5):
                x, y = ligne + dx * i, colonne + dy * i
                if 0 <= x < plateau.taille and 0 <= y < plateau.taille and plateau.plateau[x][y] == couleur:
                    alignement += 1
                else:
                    break
            score += 10 ** alignement
        return score
    
 