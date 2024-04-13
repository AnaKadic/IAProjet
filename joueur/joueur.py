class Joueur:

    """
    Classe de base pour un joueur dans le jeu. Gère les interactions de base d'un joueur avec le plateau de jeu.

    Attributs:
        couleur (str): La couleur des pierres du joueur, utilisée pour identifier le joueur sur le plateau.
    """

    def __init__(self, couleur):
        """
        Initialise un nouveau joueur avec une couleur spécifiée.

        Entrée:
            couleur (str): La couleur attribuée au joueur.
        """
        self.couleur = couleur

    def placer_pierre(self, plateau, ligne, colonne):
        """
        Tente de placer une pierre sur le plateau à la position spécifiée.

        Entrée:
            plateau (Plateau): L'objet plateau sur lequel le joueur place une pierre.
            ligne (int): L'indice de la ligne où placer la pierre.
            colonne (int): L'indice de la colonne où placer la pierre.

        Sortie:
            bool: True si la pierre a été placée avec succès, False autrement (par exemple, si la case est déjà occupée).
        """
        return plateau.placer_pierre(ligne, colonne, self.couleur)


class JoueurHumain(Joueur):
    """
    Classe représentant un joueur humain dans le jeu. Gère la saisie des coups par l'humain.

    Hérite de:
        Joueur: Classe de base pour les joueurs.
    """
    def demander_coup(self):
        """
        Demande au joueur humain de saisir les coordonnées de son coup via l'entrée standard.

        Retourne:
            tuple: Un tuple (ligne, colonne) représentant les coordonnées du coup.
        """
        ligne = int(input("\n Entrez votre ligne : ")) -1
        colonne = int(input("Entrez votre colonne : ")) -1
        return ligne, colonne
