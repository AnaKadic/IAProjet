# strategies.py
from plateau.plateau import Plateau
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
        self.profondeur = 3 if difficulte == 'difficile' else 2 if difficulte == 'moyen' else 1
        self.evaluer = getattr(self, f'evaluer_{difficulte}')

    # POUR UN NIVEAU FACILE
    def evaluer_facile(self, plateau):
        """
        Évalue le plateau de manière simple en comptant les pierres alignées directement pour la couleur spécifiée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score basé sur le nombre de pierres alignées directement.

       """
        score = 0
        nb_coups_joues = len([p for row in plateau for p in row if p != '.'])  # Compte les coups déjà joués

        # Évaluation défensive
        score_defensif = self.evaluer_defense_simple(plateau, self.couleur_adverse)
        if nb_coups_joues > 6 and score_defensif < 0:  # Ne commence à bloquer qu'après les premiers échanges
            score += score_defensif  # Applique un score défensif s'il y a des menaces

        # Évaluation offensive, activée particulièrement s'il n'y a pas de menaces immédiates
        if score_defensif >= 0 or nb_coups_joues <= 6:  # Plus agressif si le jeu est au début ou pas de menace
            score += self.evaluer_attaques_potentielles(plateau, self.couleur)

        return score # Défendre si la menace est plus critique

    def evaluer_defense_simple(self, plateau, couleur_adverse):
        """
        Évalue défensivement pour bloquer les menaces adverses de victoir.

        Entree:
            plateau (Plateau): Le plateau de jeu actuel.
            couleur_adverse (str): Couleur des pièces adverses.

        Sortie:
            int: Score basé sur les menaces bloquées.
        """
        score_defensif = 0
        for dx, dy in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            for x in range(plateau.taille):
                for y in range(plateau.taille):
                    if self.detecter_menace(plateau, x, y, dx, dy, couleur_adverse, 3):
                        score_defensif -= 50
                    if self.detecter_menace(plateau, x, y, dx, dy, couleur_adverse, 4):
                        score_defensif -= 100
        return score_defensif

    def detecter_menace(self, plateau, x, y, dx, dy, couleur, longueur):
        """
        Détecte les menaces d'alignements gagnants de l'adversaire.

        Entrée:
            plateau (Plateau): Le plateau de jeu actuel.
            x (int): Coordonnée x du début de la vérification.
            y (int): Coordonnée y du début de la vérification.
            dx (int): Incrément x pour la direction de vérification.
            dy (int): Incrément y pour la direction de vérification.
            couleur (str): Couleur des pièces à vérifier.
            longueur (int): Nombre de pièces consécutives nécessaires pour constituer une menace.

        Sortie:
            bool: True si une menace est détectée, False sinon.
        """
        alignement = 0
        espaces_vides = 0
        for i in range(-longueur + 1, longueur):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille:
                if plateau[nx][ny] == couleur:
                    alignement += 1
                elif plateau[nx][ny] == '.':
                    espaces_vides += 1
                else:
                    break
            else:
                break
        if alignement >= longueur and espaces_vides > 0:
            return True
        return False

    
    def evaluer_attaques_potentielles(self, plateau, couleur):
        """
        Évalue et calcule le score basé sur les meilleures opportunités d'attaques potentielles sur le plateau.

        Entrée:
            plateau (Plateau): Le plateau de jeu actuel.
            couleur (str): La couleur des pierres pour lesquelles l'évaluation est faite.

        Retourne:
            int: Score total obtenu en sommant les trois meilleurs scores potentiels d'attaque.
        """
        score_attaque = 0
        potential_scores = []  # Liste pour stocker les scores de toutes les cases vides
        for x in range(plateau.taille):
            for y in range(plateau.taille):
                if plateau[x][y] == '.':
                    score_potentiel = self.evaluer_attaque_potentielle(plateau, x, y, couleur)
                    potential_scores.append(score_potentiel)
        if potential_scores:
            score_attaque = sum(sorted(potential_scores)[-3:])  # Somme des trois meilleurs scores pour les menaces
        return score_attaque
    
    def evaluer_attaque_potentielle(self, plateau, x, y, couleur):
        """
        Calcule un score potentiel pour une attaque à partir d'une position donnée sur le plateau.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            x (int): Coordonnée x de la case à évaluer.
            y (int): Coordonnée y de la case à évaluer.
            couleur (str): Couleur des pierres à évaluer.

        Sortie:
            int: Score calculé basé sur le potentiel d'alignement à partir de cette position.
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in directions:
            alignement, potentiel = self.compter_potentiel(plateau, x, y, dx, dy, couleur)
            if alignement > 2:  # Augmente la pondération si un alignement gagnant est possible
                score += (alignement ** 2) + potentiel 
            else:
                score += alignement + potentiel  # Pondération normale pour les alignements courts
        return score
    
    def compter_potentiel(self, plateau, x, y, dx, dy, couleur):
        """
        Compte le nombre de pierres alignées et le potentiel d'extension d'une ligne.

        Entrée:
            plateau (Plateau): Le plateau de jeu actuel.
            x (int): Coordonnée x du début du comptage.
            y (int): Coordonnée y du début du comptage.
            dx (int): Direction x pour le comptage.
            dy (int): Direction y pour le comptage.
            couleur (str): Couleur des pierres à compter.

        Sortie:
            tuple: (alignement, potentiel) où 'alignement' est le nombre de pierres alignées et 'potentiel' est les espaces disponibles pour prolonger l'alignement.
        """
        alignement = 1 # Inclut la pierre potentielle à cette position.
        potentiel = 0
        for d in [1, -1]:  # Examine dans les deux directions.
            for i in range(1, 5):  
                nx, ny = x + i * dx * d, y + i * dy * d
                if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille:
                    if plateau[nx][ny] == couleur:
                        alignement += 1
                    elif plateau[nx][ny] == '.':
                        potentiel += 1
                    else:
                        break
                else:
                    break
        return alignement, potentiel
    

    # POUR UN NIVEAU MOYEN
    def evaluer_moyen(self, plateau):
        """
        Évalue le plateau en utilisant une logique d'évaluation modérée.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            score (int): Score calculé en fonction de diverses configurations de pierres sur le plateau.

        """
        return self.evaluer_plateau(plateau)
    
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
    

    # POUR UN NIVEAU DIFFICILE
    def evaluer_difficile(self, plateau):
        """
        Évalue le plateau pour une stratégie difficile en intégrant des menaces multiples et en optimisant les configurations offensives.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie:
            int: Score global basé sur la détection des menaces adverses et l'optimisation des configurations offensives.
        """
        score = 0
        menaces_potentielles = self.analyser_menaces_multiples(plateau, self.couleur_adverse)
        if menaces_potentielles:
            # Applique une pénalité sévère si des menaces adverses sont détectées.
            score -= 1000 * len(menaces_potentielles)

        # Parcourt chaque case du plateau pour calculer le score basé sur les positions actuelles.
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == self.couleur:
                    score += self.evaluer_alignement_potentiel(plateau, ligne, colonne, self.couleur)
                elif plateau.plateau[ligne][colonne] == self.couleur_adverse:
                    score -= self.evaluer_alignement_potentiel(plateau, ligne, colonne, self.couleur_adverse)

        # Ajoute des points pour les configurations offensives qui permettent des extensions multiples.
        score += self.evaluer_formations_ouvertes(plateau, self.couleur)
        return score

    def analyser_menaces_multiples(self, plateau, couleur):
        """
        Identifie toutes les menaces potentielles sur le plateau qui peuvent aboutir à une victoire adverse.

        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            couleur (str): Couleur des pierres adverses à surveiller.

        Sortie:
            list: Liste des coordonnées où des menaces potentielles sont détectées.
        """
        menaces = []
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Définir les directions ici
        for x in range(plateau.taille):
            for y in range(plateau.taille):
                if plateau.plateau[x][y] == '.':
                    for dx, dy in directions:  # Ajouter cette boucle pour vérifier chaque direction
                        if self.detecter_menace(plateau, x, y, dx, dy, couleur, 4):
                            menaces.append((x, y))
        return menaces

    def evaluer_alignement_potentiel(self, plateau, ligne, colonne, couleur):
        """
        Évalue le potentiel offensif d'un alignement à partir d'une position donnée sur le plateau.

        Entrée:
            plateau (Plateau): Le plateau de jeu actuel.
            ligne (int): Coordonnée de la ligne de la pierre évaluée.
            colonne (int): Coordonnée de la colonne de la pierre évaluée.
            couleur (str): Couleur des pierres à évaluer.

        Sortie:
            int: Score basé sur le potentiel d'alignement à partir de cette position.
        """
        score = 0
        # Évaluation basée sur les alignements potentiels à partir de cette position
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in directions:
            alignement = 1  # Compte la pierre courante
            for i in range(1, 5):  # Regarde jusqu'à quatre espaces de chaque côté
                nx, ny = ligne + i * dx, colonne + i * dy
                if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille and plateau.plateau[nx][ny] == couleur:
                    alignement += 1
                else:
                    break
            score += 10 ** alignement  # Applique un poids exponentiel pour favoriser les alignements longs
        return score

    def evaluer_formations_ouvertes(self, plateau, couleur):
        score = 0
        # Évaluation des formations qui permettent des extensions dans plusieurs directions
        for x in range(plateau.taille):
            for y in range(plateau.taille):
                if plateau.plateau[x][y] == couleur:
                    score += self.compter_formations_ouvertes(plateau, x, y, couleur)
        return score
    
    def compter_formations_ouvertes(self, plateau, x, y, couleur):
        """
        Entrée:
            plateau (Plateau): L'état actuel du plateau de jeu.
            x (int): La coordonnée x de la pierre évaluée.
            y (int): La coordonnée y de la pierre évaluée.
            couleur (str): La couleur des pierres à évaluer.

        Sortie:
            int: Score basé sur le nombre et la qualité des formations ouvertes.
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
        ouvertures = {}

        for dx, dy in directions:
            open_ends = 0
            ligne = []
            for i in range(-4, 5):  # Examine jusqu'à quatre cases dans chaque direction à partir de la pierre
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille:
                    if plateau.plateau[nx][ny] == couleur:
                        ligne.append((nx, ny))
                    elif plateau.plateau[nx][ny] == '.':
                        open_ends += 1
                        break  # Sort dès qu'un espace ouvert est trouvé
                    else:
                        break  # Bloqué par une pierre adverse
                else:
                    break  # Hors des limites du plateau

            # Une formation ouverte est plus puissante si elle a des extrémités ouvertes des deux côtés
            if len(ligne) >= 2 and open_ends > 0:
                ouverture_key = tuple(sorted(ligne))
                if ouverture_key not in ouvertures:
                    ouvertures[ouverture_key] = open_ends
                else:
                    ouvertures[ouverture_key] = max(ouvertures[ouverture_key], open_ends)

        # Calculer le score en fonction du nombre d'ouvertures et de leur potentiel
        for key, value in ouvertures.items():
            if len(key) >= 3:
                score += 50 * value  # Plus la ligne est longue, plus elle est valorisée
            elif len(key) == 2:
                score += 20 * value

        return score
