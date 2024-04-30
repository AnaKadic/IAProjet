from strategie.minmax import MinimaxStrategy

class JoueurIA:
    """
    Représente un joueur IA dans le jeu.
    """
    def __init__(self, couleur, difficulte, plateau, nom, est_ia=True):
        """
        Initialise une nouvelle instance de JoueurIA.

        Entrées:
            couleur (str): Couleur des pièces du joueur.
            difficulte (str): Niveau de difficulté de l'IA.
            plateau (Plateau): Plateau de jeu sur lequel l'IA jouera.
            nom (str): Nom du joueur.
            est_ia (bool, optionnel): Spécifie si le joueur est une IA. Default à True.
        """
        self.couleur = couleur
        self.difficulte = difficulte
        self.nom = nom
        self.plateau = plateau  
        self.strategie = MinimaxStrategy(plateau, couleur, difficulte)
        self.est_ia = est_ia

    def jouer_coup(self, plateau):
        """
        Détermine et joue le coup suivant basé sur la stratégie Minimax.

        Entrée:
            plateau (Plateau): Le plateau de jeu actuel où le coup sera joué.

        Sortie:
            tuple: Les coordonnées du coup choisi par l'IA.
        """
        return self.strategie.choisir_coup()

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'instance de JoueurIA.

        Sortie:
            str: Représentation sous forme de chaîne du joueur.
        """
        return f"{self.nom} ({self.couleur} - {self.difficulte})"
