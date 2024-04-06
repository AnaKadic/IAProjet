from constant import CHANGEMENT_LIGNE, CHANGEMENT_COLONNE, Joueur, TAILLE_PLATEAU
from strategie import Strategie

INFINI = int(7e12)
PROFONDEUR = 4

class StrategieMinmax(Strategie) :
    """
    Stratégie utilisant l'algorithme Minmax avec élagage alpha-bêta pour calculer le prochain coup.
    """
    # Scores utilisés pour évaluer un plateau donné
    SCORES_HEURISTIQUES = {
        "-----": -1000000000000,
        "+++++": 1000000000000,
        " ---- ": -50000000000,
        " ++++ ": 10000000000,
        "-++++ ": 100000000,
        " ++++-": 100000000,
        " ----+": -500000000,
        "+---- ": -500000000,
        " +++ ": 1000,
        " +++-": 150,
        " ---+": -50,
        " --- ": -5000,
        " ++ ": 10,
        " -- ": -50
    }

    def faire_un_coup(self, plateau, couleur_joueur):
        """
        Calcule et exécute le meilleur coup possible en utilisant l'algorithme MinMax avec élagage alpha-bêta.

        Entrée :
            plateau (Plateau): L'état actuel du jeu où le coup sera effectué.
            couleur_joueur (str): La couleur du joueur actuel ('N' pour Noir ou 'B' pour Blanc).

        Sortie :
            meilleur_coup (tuple): Les coordonnées du meilleur coup trouvé sous la forme (ligne, colonne).

        Retourne :
            Le meilleur coup à jouer sous forme de tuple (ligne, colonne). Si aucun coup n'est possible, 
            retourne None.

        Affiche également le coup calculé avec son score évalué.
        """
         
        possibilites_initiales = plateau.generer_coups_possibles()
        meilleur_score, meilleur_coup = float('-inf'), None

        for coup in possibilites_initiales:
            plateau_temp = plateau.simuler_coup(coup, couleur_joueur)
            score = self.minmax(plateau_temp, self.profondeur, False)[0]  
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup

        if meilleur_coup is not None:
            plateau.placer_pierre(*meilleur_coup, couleur_joueur)
            print(f'Coup calculé : {meilleur_coup} avec un score de : {meilleur_score}')
            return meilleur_coup
        else:
            return None

    def minmax(self, plateau, profondeur, est_maximisant, alpha, beta, cases_importantes, couleur_joueur, coups_effectues):

        if profondeur == 0 or plateau.est_jeu_termine():
            # Évaluation du plateau à la profondeur maximale ou si jeu terminé
            return self.evaluer_plateau(plateau, couleur_joueur, coups_effectues), None

        couleur_adverse = 'N' if couleur_joueur == 'B' else 'B'
        if est_maximisant:
            valeur_max = float('-inf')
            meilleur_coup = None
            for coup in plateau.generer_coups_possibles():
                plateau.simuler_coup(coup, couleur_joueur)
                valeur = self.minmax(plateau, profondeur - 1, False, alpha, beta, cases_importantes, couleur_adverse, coups_effectues + [coup])[0]
                plateau.annuler_coup(coup)
                if valeur > valeur_max:
                    valeur_max = valeur
                    meilleur_coup = coup
                alpha = max(alpha, valeur)
                if beta <= alpha:
                    break
            return valeur_max, meilleur_coup
        else:
            valeur_min = float('inf')
            pire_coup = None
            for coup in plateau.generer_coups_possibles():
                plateau.simuler_coup(coup, couleur_adverse)
                valeur = self.minmax(plateau, profondeur - 1, True, alpha, beta, cases_importantes, couleur_joueur, coups_effectues + [coup])[0]
                plateau.annuler_coup(coup)
                if valeur < valeur_min:
                    valeur_min = valeur
                    pire_coup = coup
                beta = min(beta, valeur)
                if beta <= alpha:
                    break
            return valeur_min, pire_coup

    def obtenir_cases_possibles(self, plateau, cases_importantes, coups_effectues):
        """
        Génère un ensemble de cases potentiellement avantageuses pour le prochain coup.

        Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu.
            cases_importantes (list): Une liste de cases qui sont jugées importantes pour l'évaluation.
            coups_effectues (list): Une liste de tuples (ligne, colonne) représentant les coups déjà joués.

        Sortie :
            liste_cases_possibles (list): Une liste de tuples (ligne, colonne) des cases possibles pour le prochain coup.

        Retourne :
            La liste des cases possibles triées par importance, déterminée par une fonction heuristique.
        """
        cases_possibles = set(cases_importantes)  # Utilise un set pour éviter les duplicatas

        # Ajoute les cases adjacentes aux derniers coups à l'ensemble des cases possibles
        for ligne, colonne in coups_effectues:
            for dx, dy in [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]:
                nouvelle_ligne, nouvelle_colonne = ligne + dx, colonne + dy
                if 0 <= nouvelle_ligne < plateau.taille and 0 <= nouvelle_colonne < plateau.taille:
                    if plateau.plateau[nouvelle_ligne][nouvelle_colonne] == '.':
                        cases_possibles.add((nouvelle_ligne, nouvelle_colonne))

        # Convertit l'ensemble des cases possibles en liste pour pouvoir la trier
        liste_cases_possibles = list(cases_possibles)

        # (Optionnel) Trier les cases possibles par une certaine heuristique, par exemple par proximité aux coups récents
        liste_cases_possibles.sort(key=lambda case: self.heuristique_case(case, plateau, coups_effectues))

        return liste_cases_possibles

    def heuristique_case(self, case, plateau, coups_effectues):
        """
        Calcule une valeur heuristique pour une case donnée, basée sur des critères comme la proximité aux coups récents.

        Entrée :
            case (tuple): La case pour laquelle calculer la valeur heuristique, donnée sous forme de tuple (ligne, colonne).
            plateau (Plateau): L'état actuel du plateau de jeu.
            coups_effectues (list): Une liste de tuples (ligne, colonne) représentant les coups déjà joués.

        Sortie :
            distance (int): La valeur heuristique de la case, basée sur la proximité au dernier coup joué.

        Retourne :
            Une valeur heuristique représentant l'importance stratégique de la case dans le contexte actuel du jeu.
        """
        dernier_coup = coups_effectues[-1] if coups_effectues else None
        if dernier_coup:
            distance = abs(case[0] - dernier_coup[0]) + abs(case[1] - dernier_coup[1])
            return distance
        else:
            # Aucun coup joué, toutes les cases ont la même priorité
            return 0

    def evaluer_plateau(self, plateau, couleur_joueur, coups_effectues):
        """
        Évalue la force de la position sur le plateau pour un joueur spécifique.

        Entrée :
            plateau (Plateau) : L'état actuel du plateau de jeu.
            couleur_joueur (str) : La couleur des pierres du joueur ('B' pour Noir, 'N' pour Blanc).
            coups_effectues (list) : Liste des coups précédemment joués.

        Sortie :
            score (int) : Le score évalué du plateau, positif pour des positions favorables au joueur, négatif pour des positions défavorables.

        Retourne :
            Un score heuristique basé sur les alignements actuels des pierres du joueur et de son adversaire sur le plateau.
        """
        score = 0
        # Identifie la couleur adverse pour l'évaluation
        couleur_adverse = 'N' if couleur_joueur == 'B' else 'B'

        # boucle à travers toutes les cases du plateau
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == couleur_joueur:
                    # Pour chaque pierre du joueur, augmenter le score basé sur des alignements potentiels
                    score += self.evaluer_alignement(plateau, ligne, colonne, couleur_joueur)
                elif plateau.plateau[ligne][colonne] == couleur_adverse:
                    # Pour chaque pierre de l'adversaire, diminuer le score basé sur ses alignements potentiels
                    score -= self.evaluer_alignement(plateau, ligne, colonne, couleur_adverse)

        return score

    def evaluer_alignement(self, plateau, ligne, colonne, couleur):
        """
        Évalue l'importance d'un alignement potentiel de pierres à partir d'une case spécifique.

        Entrée :
            plateau (Plateau) : L'état actuel du plateau de jeu.
            ligne (int) : L'indice de la ligne de la case à évaluer.
            colonne (int) : L'indice de la colonne de la case à évaluer.
            couleur (str) : La couleur de la pierre à évaluer.

        Sortie :
            score (int) : Le score basé sur l'alignement des pierres autour de la case spécifiée.

        Retourne :
            Un score représentant la valeur de l'alignement potentiel des pierres, qui s'incremente exponentiellement avec chaque pierre alignée consécutivement.
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        for dx, dy in directions:
            alignement_temp = 1  # Compte la pierre courante
            # Vérifie devant
            for i in range(1, 5):
                x, y = ligne + dx * i, colonne + dy * i
                if 0 <= x < plateau.taille and 0 <= y < plateau.taille and plateau.plateau[x][y] == couleur:
                    alignement_temp += 1
                else:
                    break
            # Vérifie derrière
            for i in range(1, 5):
                x, y = ligne - dx * i, colonne - dy * i
                if 0 <= x < plateau.taille and 0 <= y < plateau.taille and plateau.plateau[x][y] == couleur:
                    alignement_temp += 1
                else:
                    break
            # Augmenter le score basé sur le nombre de pierres alignées
            score += 10 ** alignement_temp

        return score


    @staticmethod
    def obtenir_importance_case(plateau, ligne, colonne):
        """
        Calcule l'importance d'une case vide sur le plateau en se basant sur sa proximité avec des pierres existantes.

        Entrée :
            plateau (Plateau) : L'état actuel du plateau de jeu.
            ligne (int) : L'indice de la ligne de la case à évaluer.
            colonne (int) : L'indice de la colonne de la case à évaluer.

        Sortie :
            importance (int) : Le score d'importance de la case, basé sur la proximité aux pierres existantes.

        Retourne :
        Un score d'importance où une case adjacente à une pierre existante reçoit une valeur plus élevée, indiquant une plus grande pertinence stratégique pour les mouvements futurs.
        """
        if plateau[ligne][colonne] != '.':
            # Case déjà occupée
            return 0

        importance = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
    
        for dx, dy in directions:
            for dist in range(1, 5):  # Vérifier jusqu'à 4 cases loin dans chaque direction
                x, y = ligne + dx * dist, colonne + dy * dist
                if 0 <= x < plateau.taille and 0 <= y < plateau.taille:
                    if plateau[x][y] != '.':
                        # Case à proximité d'une pierre existante augmente son importance
                        importance += 1
                        break  # Une pierre trouvée dans cette direction suffit
                else:
                    break  # Sortie du plateau

        return importance