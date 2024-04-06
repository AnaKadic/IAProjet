class Plateau:
    def __init__(self, taille=15):
        self.taille = taille
        self.plateau = self.initialiser_plateau()

    def initialiser_plateau(self):
        """
        Initialise le plateau de jeu avec des cases vides.

        Retourne :
            Une grille 2D remplie de '.' représentant les cases vides du plateau.
        """
        return [['.' for _ in range(self.taille)] for _ in range(self.taille)]

    def afficher_plateau(self):
        """
        Affiche l'état actuel du plateau de jeu dans la console.
        """
        for ligne in self.plateau:
            print(' '.join(ligne))
        print()  # Ligne vide pour une meilleure séparation

    def placer_pierre(self, ligne, colonne, couleur):
        """
        Place une pierre de la couleur donnée à la position spécifiée sur le plateau.

        Entrées :
            ligne (int) : L'indice de la ligne où placer la pierre.
            colonne (int) : L'indice de la colonne où placer la pierre.
            couleur (str) : La couleur de la pierre ('B' pour noir ou 'N' pour blanc).

        Retourne :
            True si la pierre a été placée avec succès, False si la case est déjà occupée.
        """

        if self.plateau[ligne][colonne] == '.':
            self.plateau[ligne][colonne] = couleur
            return True
        return False

    def verifier_victoire(self, ligne, colonne, couleur):
        """
        Vérifie si un coup à une position donnée conduit à une victoire.

        Entrées :
            ligne (int) : L'indice de la ligne du dernier coup joué.
            colonne (int) : L'indice de la colonne du dernier coup joué.
            couleur (str) : La couleur du joueur qui a effectué le dernier coup.

        Retourne :
            True si le coup conduit à une victoire, sinon False.
        """
        # Vérifie dans toutes les directions principales
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, Vertical, et deux diagonales
        for delta_x, delta_y in directions:
            if self.verifier_direction(ligne, colonne, couleur, delta_x, delta_y):
                return True
        return False


    def verifier_direction(self, ligne, colonne, couleur, delta_x, delta_y):
        """
        Vérifie si cinq pierres de la même couleur sont alignées dans une direction donnée.

        Entrées :
            ligne (int) : L'indice de la ligne de départ pour la vérification.
            colonne (int) : L'indice de la colonne de départ pour la vérification.
            couleur (str) : La couleur des pierres à vérifier.
            delta_x (int) : Le changement en x pour la direction à vérifier.
            delta_y (int) : Le changement en y pour la direction à vérifier.

        Retourne :
            True si cinq pierres consécutives de la même couleur sont trouvées, sinon False.
        """
        compteur = 0
        for i in range(-4, 5):
            x = ligne + i * delta_x
            y = colonne + i * delta_y
            if 0 <= x < self.taille and 0 <= y < self.taille and self.plateau[x][y] == couleur:
                compteur += 1
                if compteur == 5:
                    return True
            else:
                compteur = 0
        return False
    
    def est_jeu_termine(self):
        """
        Vérifie si le jeu est terminé, soit parce que le plateau est entièrement rempli, soit parce qu'une condition de victoire a été atteinte.

        Retourne :
            True si le jeu est terminé, False sinon.
        """
        for ligne in self.plateau:
            if '.' in ligne:
                return False  # Le jeu continue s'il reste des espaces vides
        return True  # Le jeu est terminé si le plateau est complet

    def generer_coups_possibles(self):
        """
        Génère une liste de tous les coups possibles (cases vides) sur le plateau actuel.

        Retourne :
            Une liste de tuples (ligne, colonne) représentant chaque coup possible.
        """
        coups = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.plateau[i][j] == '.':
                    coups.append((i, j))
        return coups
    
    def simuler_coup(self, coup, couleur):
        """
        Simule un coup sur le plateau sans modifier l'état actuel, créant un nouveau plateau avec le coup appliqué.

        Entrées :
            coup (tuple) : Le coup à simuler, sous forme de tuple (ligne, colonne).
            couleur (str) : La couleur de la pierre à placer.

        Retourne :
            Une nouvelle instance de Plateau avec le coup appliqué.
        """
        # Crée une copie profonde du plateau
        nouveau_plateau = [ligne[:] for ligne in self.plateau]
        
        ligne, colonne = coup
        nouveau_plateau[ligne][colonne] = couleur
        
        # Crée une nouvelle instance de Plateau avec la copie modifiée
        plateau_temp = Plateau(self.taille)
        plateau_temp.plateau = nouveau_plateau
        
        return plateau_temp
    
    def evaluer_plateau(self, plateau):
        """
        Évalue le plateau actuel en fonction d'une série de configurations prédéfinies pour déterminer son score.

        Entrées :
            plateau (Plateau) : Le plateau à évaluer.

        Retourne :
            Le score évalué du plateau en fonction des configurations des pierres.
        """
        score = 0
        configurations = {
            'xxxxx': 100000,
            'xxxxo': 10000,
            'xxxox': 1000,
        }

        return score