from colorama import Fore, Style, init

# Initialisation de Colorama pour s'assurer qu'il réinitialise correctement les couleurs
init(autoreset=True)

class Plateau:

    """
    Représente le plateau de jeu pour un jeu de plateau du GOMOKU
    Gère le stockage des pièces sur le plateau et effectue des opérations telles que placer des pierres et vérifier les conditions de victoire.

    Attributs:
        taille (int): La taille du plateau, typiquement 15 pour un jeu de Gomoku.
        plateau (list): Une matrice 2D représentant l'état actuel du plateau avec des pierres placées.
    """



    def __init__(self, taille=15):
        """
        Initialise un nouveau plateau de jeu de taille spécifiée, généralement 15x15 pour le Gomoku.

        Entrée:
            taille (int): La taille du plateau de jeu, définissant les dimensions du tableau.
        """
        self.taille = taille
        self.plateau = self.initialiser_plateau()

    def __getitem__(self, idx):
        """
        Permet l'accès indexé au plateau, facilitant l'accès direct aux lignes du plateau.

        Entrée:
            idx (int): L'index de la ligne à accéder.

        Retourne:
            list: La ligne du plateau à l'index spécifié.
        """
        return self.plateau[idx]
    
    def initialiser_plateau(self):
        """
        Initialise le plateau de jeu avec des cases vides.

        Retourne:
            list: Une matrice 2D remplie de '.' représentant un plateau vide.
        """
        return [['.' for _ in range(self.taille)] for _ in range(self.taille)]
    
    """
    def afficher_plateau(self):

         # En-tête avec les numéros de colonne alignés correctement
        espacement_entre_colonnes = "  "
        header = " " * 3  # Espacement pour l'alignement de la première colonne
        header += espacement_entre_colonnes.join(f"{i+1:2d}" for i in range(self.taille))
        print(header)

        # Bordure supérieure du plateau
        print(" +" + "---+" * self.taille)

        for idx, ligne in enumerate(self.plateau):
            # Ligne de séparation
            print(" +" + "---+" * self.taille)

            # Affiche le numéro de la ligne à gauche du plateau
            print(f"{idx+1:2}|" + "|".join(f" {cell} " for cell in ligne) + "|")
        
        # Dernière ligne de séparation
        print(" +" + "---+" * self.taille)
    """

    # Vous pouvez définir des constantes pour les caractères de pierre


    def afficher_plateau(self):
        """
        Affiche le plateau de jeu dans la console avec des couleurs et des symboles.
        """
        PIERRE_NOIRE = Fore.BLACK + '●' + Style.RESET_ALL
        PIERRE_BLANCHE = Fore.WHITE + '○' + Style.RESET_ALL
        VIDE = "."

        # En-tête avec les numéros de colonne alignés
        espacement_entre_colonnes = "  "
        header = " " * 3  # Espacement pour aligner la première colonne
        header += espacement_entre_colonnes.join(f"{i+1:2d}" for i in range(self.taille))
        print(header)

        # Bordure supérieure du plateau
        print(" +" + "---+" * self.taille)

        for idx, ligne in enumerate(self.plateau):
            # Ligne de séparation
            print(" +" + "---+" * self.taille)

            # Affiche le numéro de la ligne à gauche du plateau
            row_display = f"{idx+1:2d}| " + " | ".join(
                PIERRE_NOIRE if cell == 'B' else PIERRE_BLANCHE if cell == 'N' else VIDE for cell in ligne
            ) + " |"

            print(row_display)
        
        # Dernière ligne de séparation
        print(" +" + "---+" * self.taille)


        
    def placer_pierre(self, ligne, colonne, couleur):
        """
        Place une pierre de la couleur spécifiée à l'emplacement donné si la case est vide.

        Entrée:
            ligne (int): L'indice de la ligne où placer la pierre.
            colonne (int): L'indice de la colonne où placer la pierre.
            couleur (str): La couleur de la pierre à placer.

        Retourne:
            bool: True si la pierre a été placée avec succès, sinon False.
        """
        if self.plateau[ligne][colonne] == '.':
            self.plateau[ligne][colonne] = couleur
            return True
        return False

    def verifier_victoire(self, ligne, colonne, couleur):
        """
        Vérifie si placer une pierre à l'emplacement donné entraîne une victoire pour le joueur de cette couleur.

        Entrée:
            ligne (int): L'indice de la ligne où la pierre a été placée.
            colonne (int): L'indice de la colonne où la pierre a été placée.
            couleur (str): La couleur de la pierre placée.

        Retourne:
            bool: True si le coup est gagnant, sinon False.
        """
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)] 
        for delta_x, delta_y in directions:
            if self.verifier_direction(ligne, colonne, couleur, delta_x, delta_y):
                return True
        return False


    def verifier_direction(self, ligne, colonne, couleur, delta_x, delta_y):
        """
        Vérifie une ligne de pierres dans une direction donnée pour voir si elle forme une ligne de 5 pierres de la même couleur.

        Entrée:
            ligne (int): Ligne de départ pour la vérification.
            colonne (int): Colonne de départ pour la vérification.
            couleur (str): Couleur des pierres à vérifier.
            delta_x (int): Incrément horizontal pour la vérification.
            delta_y (int): Incrément vertical pour la vérification.

        Retourne:
            bool: True si une ligne de cinq pierres de même couleur est formée, sinon False.
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
        Vérifie si le plateau est complet. Note : Cette méthode ne vérifie pas les conditions de victoire.
        Les conditions de victoire doivent être vérifiées séparément après chaque coup.

        Retourne :
            True si le plateau est complet, False sinon.
        """
        for ligne in self.plateau:
            if '.' in ligne:
                return False  # Le jeu continue s'il reste des espaces vides
        return True  # Le jeu est terminé si le plateau est complet

    def generer_coups_possibles(self):
        """
        Génère une liste de tous les coups possibles sur le plateau où aucune pierre n'est placée.

        Retourne:
            list: Liste de tuples représentant les coordonnées (ligne, colonne) des cases vides où une pierre peut être placée.
        """
        coups = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.plateau[i][j] == '.':
                    coups.append((i, j))
        return coups
    
    def simuler_coup(self, coup, couleur):
        """
        Simule un coup sur le plateau sans modifier l'état actuel du plateau.
        Crée une nouvelle instance de Plateau avec le coup appliqué pour évaluation ou autres besoins sans affecter le plateau principal.

        Paramètres:
            coup (tuple): Tuple de (ligne, colonne) indiquant où la pierre est placée.
            couleur (str): La couleur de la pierre à placer.

        Retourne:
            Plateau: Une nouvelle instance de Plateau représentant l'état après le coup.
        """
        # Crée une copie du plateau
        nouveau_plateau = [ligne[:] for ligne in self.plateau]
        
        # Applique le coup sur la copie
        ligne, colonne = coup
        nouveau_plateau[ligne][colonne] = couleur
        
        # Crée une nouvelle instance de Plateau avec la copie modifiée
        plateau_temp = Plateau(self.taille)
        plateau_temp.plateau = nouveau_plateau
        
        return plateau_temp
    
    def evaluer_plateau(self, plateau):
        """
        Évalue le plateau actuel selon un ensemble de configurations prédéfinies pour déterminer le score.
        Cette méthode est un squelette et doit être complétée avec des règles d'évaluation spécifiques pour être fonctionnelle.

        Paramètres:
            plateau (list): Une matrice 2D représentant l'état actuel du plateau à évaluer.

        Retourne:
            int: Le score évalué du plateau basé sur les configurations prédéfinies.
        """
        score = 0
        configurations = {
            'xxxxx': 100000,
            'xxxxo': 10000,
            'xxxox': 1000,

        }

        return score
