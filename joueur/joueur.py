class Joueur:
    def __init__(self, couleur):
        self.couleur = couleur

    def placer_pierre(self, plateau, ligne, colonne):
        """
        Tente de placer une pierre de la couleur du joueur sur le plateau à la position spécifiée.

        Entrée :
            plateau (Plateau): Le plateau de jeu sur lequel placer la pierre.
            ligne (int): L'indice de la ligne pour placer la pierre.
            colonne (int): L'indice de la colonne pour placer la pierre.

        Retourne :
            bool: True si la pierre a été placée avec succès, False sinon.
        """
        return plateau.placer_pierre(ligne, colonne, self.couleur)


class JoueurHumain(Joueur):
    def demander_coup(self):
        """
        Demande au joueur humain de saisir les coordonnées de son prochain coup.

        Retourne :
            tuple: Un tuple (ligne, colonne) indiquant la position où le joueur souhaite placer sa pierre.
        """
        ligne = int(input("Entrez votre ligne : "))
        colonne = int(input("Entrez votre colonne : "))
        return ligne, colonne