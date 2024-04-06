from joueur.joueur import Joueur

class IA(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
        self.profondeur = 3 

    def evaluer_plateau(self, plateau):
        """
        Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu avec toutes les pierres placées.

         Sortie :
            score (int): Le score évalué du plateau, positif si favorable au joueur, négatif si défavorable.

        Retourne :
            Le score total évalué pour le plateau de jeu donné.
        """
        score = 0
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == self.couleur:
                    score += self.evaluer_alignement(plateau, ligne, colonne, self.couleur)
                elif plateau.plateau[ligne][colonne] != '.':
                    score -= self.evaluer_alignement(plateau, ligne, colonne, plateau.plateau[ligne][colonne])
        return score

    def evaluer_alignement(self, plateau, ligne, colonne, couleur):
        """
         Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu.
            ligne (int): La ligne de la case à évaluer.
            colonne (int): La colonne de la case à évaluer.
            couleur (str): La couleur de la pierre du joueur.

        Sortie :
            score (int): Le score évalué basé sur les alignements de la pierre.

        Retourne :
            Le score évalué pour les alignements de la case spécifiée.
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

    def minmax(self, plateau, profondeur, maximisant, alpha=float('-inf'), beta=float('inf')):
        """
        Implémente l'algorithme MinMax avec élagage alpha-bêta pour optimiser le choix du coup à jouer.
        
        Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu.
            profondeur (int): Niveau de profondeur actuel de l'arbre de recherche.
            maximisant (bool): Indique si l'IA est en train de maximiser ou minimiser le score.
            alpha (float): La valeur alpha pour l'élagage alpha-bêta.
            beta (float): La valeur bêta pour l'élagage alpha-bêta.

        Sortie :
            Tuple (valeur_max ou valeur_min, meilleur_coup): La meilleure valeur de coup évaluée et le coup correspondant.

        Retourne :
            La meilleure valeur de score et le coup associé à cette valeur.
        """
        if profondeur == 0 or plateau.est_jeu_termine():
            return self.evaluer_plateau(plateau), None
        meilleur_coup = None
        if maximisant:
            valeur_max = float('-inf')
            for coup in self.generer_coups_possibles(plateau):
                plateau_temp = plateau.simuler_coup(coup, self.couleur)
                valeur = self.minmax(plateau_temp, profondeur-1, False, alpha, beta)[0]
                if valeur > valeur_max:
                    valeur_max = valeur
                    meilleur_coup = coup
                alpha = max(alpha, valeur)
                if beta <= alpha:
                    break
            return valeur_max, meilleur_coup
        else:
            valeur_min = float('inf')
            for coup in self.generer_coups_possibles(plateau):
                plateau_temp = plateau.simuler_coup(coup, 'N' if self.couleur == 'B' else 'B')
                valeur = self.minmax(plateau_temp, profondeur-1, True, alpha, beta)[0]
                if valeur < valeur_min:
                    valeur_min = valeur
                    meilleur_coup = coup
                beta = min(beta, valeur)
                if beta <= alpha:
                    break
            return valeur_min, meilleur_coup

    def generer_coups_possibles(self, plateau):
        """
        Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie :
            coups (list): Une liste de tuples représentant tous les coups possibles (ligne, colonne).

        Retourne :
            Une liste de tous les coups valides qui peuvent être joués.
        """
        coups = []
        for ligne in range(plateau.taille):
            for colonne in range(plateau.taille):
                if plateau.plateau[ligne][colonne] == '.':
                    coups.append((ligne, colonne))
        return coups

    def choisir_coup(self, plateau):
        """
        Entrée :
            plateau (Plateau): L'état actuel du plateau de jeu.

        Sortie :
            coup (tuple): Les coordonnées du meilleur coup trouvé (ligne, colonne).

        Retourne :
            Les coordonnées du coup choisi par l'IA.
        """
        _, coup = self.minmax(plateau, self.profondeur, True)
        return coup