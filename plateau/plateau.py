import copy
from colorama import Fore, Style, init


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


    def afficher_plateau(self):
        """
        Affiche le plateau de jeu dans la console avec des couleurs et des symboles.
        """
        PIERRE_NOIRE = Fore.BLACK  + '●' + Style.RESET_ALL  # Noir pour les pierres noires
        PIERRE_BLANCHE = Fore.WHITE + '○' + Style.RESET_ALL  # Blanc pour les pierres blanches
        VIDE = Fore.BLACK + '.' + Style.RESET_ALL  # Rouge pour les vides

        # En-tête avec les numéros de colonne
        espacement_entre_colonnes = "  "
        header = Fore.BLUE + " " * 3  # Vert pour l'alignement de la première colonne
        header += espacement_entre_colonnes.join(Fore.BLUE + f"{i+1:2d}" + Style.RESET_ALL for i in range(self.taille))
        print(header)

        for idx, ligne in enumerate(self.plateau):
            # Ligne de séparation
            print(Fore.BLUE + "  +" + "---+" * self.taille + Style.RESET_ALL)

            # Affiche le numéro de la ligne à gauche du plateau et les barres verticales en vert
            row_display = Fore.BLUE + f"{idx+1:2d} |"  # Vert pour le numéro de la ligne
            row_display += " | ".join(
                PIERRE_NOIRE if cell == 'B' else PIERRE_BLANCHE if cell == 'N' else VIDE for cell in ligne
            ) + " |" + Style.RESET_ALL

            print(Fore.BLUE + row_display + Style.RESET_ALL)

        # Dernière ligne de séparation
        print(Fore.BLUE + " +" + "---+" * self.taille + Style.RESET_ALL)

        
    def placer_pierre(self, ligne, colonne, couleur):
        """
        Place une pierre de la couleur spécifiée à l'emplacement donné si la case est vide et si les indices sont valides.

        Entrée:
            ligne (int): L'indice de la ligne où placer la pierre.
            colonne (int): L'indice de la colonne où placer la pierre.
            couleur (str): La couleur de la pierre à placer.

        Retourne:
            bool: True si la pierre a été placée avec succès, sinon False.
        """
        if 0 <= ligne < self.taille and 0 <= colonne < self.taille:  # Vérifie si les indices sont dans les limites
            if self.plateau[ligne][colonne] == '.':
                self.plateau[ligne][colonne] = couleur
                return True
            else:
                print(Fore.RED + "Erreur: La case est déjà occupée.")
        else:
            print(Fore.RED + "Erreur: Les indices sont hors des limites du plateau.")
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
                return True  # Arrête la recherche dès qu'une victoire est détectée
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
        compteur = 1  # Compte la pierre initiale
        # Vérifie dans la direction positive
        for i in range(1, 5):
            x = ligne + i * delta_x
            y = colonne + i * delta_y
            if 0 <= x < self.taille and 0 <= y < self.taille and self.plateau[x][y] == couleur:
                compteur += 1
            else:
                break
        # Vérifie dans la direction négative
        for i in range(1, 5):
            x = ligne - i * delta_x
            y = colonne - i * delta_y
            if 0 <= x < self.taille and 0 <= y < self.taille and self.plateau[x][y] == couleur:
                compteur += 1
            else:
                break
        return compteur >= 5
    
    def est_jeu_termine(self):
        """
        Vérifie si le plateau est complet. Note : Cette méthode ne vérifie pas les conditions de victoire.
        Les conditions de victoire doivent être vérifiées séparément après chaque coup.

        Retourne :
            bool : True si le plateau est complet, False sinon.
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
        Utilise `deepcopy` pour une copie complète du plateau, permettant la manipulation sans affecter l'état original.

        Paramètres:
            coup (tuple): Tuple de (ligne, colonne) indiquant où la pierre est placée.
            couleur (str): La couleur de la pierre à placer.

        Retourne:
            Plateau: Une nouvelle instance de Plateau représentant l'état après le coup.
        """
        # Crée une copie profonde du plateau
        nouveau_plateau = copy.deepcopy(self.plateau)
        
        # Applique le coup sur la copie
        ligne, colonne = coup
        nouveau_plateau[ligne][colonne] = couleur
        
        # Crée une nouvelle instance de Plateau avec la copie modifiée
        plateau_temp = Plateau(self.taille)
        plateau_temp.plateau = nouveau_plateau
        
        return plateau_temp
    
   

    def est_plein(self):
        """Retourne True si toutes les cases du plateau sont remplies."""
        return all(cell != '.' for row in self.plateau for cell in row)

    def copier(self):
        # Create a new Plateau instance with the same size
        new_plateau = Plateau(self.taille)
        # Copy the game board
        new_plateau.plateau = [row[:] for row in self.plateau]
        return new_plateau
