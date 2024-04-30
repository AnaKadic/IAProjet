from strategie.evaluation import Evaluation
from colorama import Fore, Style, init

init(autoreset=True)  


class SimulateurPartie:
    """
    Simule une partie entre deux joueurs sur un plateau de jeu.
    Attributs:
        joueur1 (JoueurIA): Le premier joueur de la partie.
        joueur2 (JoueurIA): Le deuxième joueur de la partie.
        plateau (Plateau): Le plateau de jeu sur lequel la partie est jouée.
        joueur_actuel (JoueurIA): Le joueur qui a le tour de jouer.
    """

    def __init__(self, joueur1, joueur2, plateau):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.plateau = plateau
        self.joueur_actuel = joueur1

        self.evaluation1 = Evaluation(plateau, joueur1.couleur, joueur1.difficulte)
        self.evaluation2 = Evaluation(plateau, joueur2.couleur, joueur2.difficulte)
        self.evaluation_actuelle = self.evaluation1  # Commence avec le joueur1

    def afficher_plateau(self):
        """
        Affiche le plateau de jeu.
        """
        PIERRE_NOIRE = Fore.LIGHTBLACK_EX + '●' + Style.RESET_ALL 
        PIERRE_BLANCHE = Fore.WHITE + '○' + Style.RESET_ALL 
        VIDE = Fore.RED + '.' + Style.RESET_ALL  

        espacement_entre_colonnes = "  "
        header = Fore.GREEN + " " * 3  
        header += espacement_entre_colonnes.join(Fore.GREEN + f"{i+1:2d}" for i in range(self.plateau.taille))
        print(header)

        
        print(Fore.GREEN + "  +" + "---+" * self.plateau.taille)

        for idx, ligne in enumerate(self.plateau.plateau):
        
            print(Fore.GREEN + "  +" + "---+" * self.plateau.taille)

        
            row_display = Fore.GREEN + f"{idx+1:2d} |"  
            row_display += " | ".join(
                PIERRE_NOIRE if cell == 'B' else PIERRE_BLANCHE if cell == 'N' else VIDE for cell in ligne
            ) + " |"
            print(row_display)

        print(Fore.GREEN + "  +" + "---+" * self.plateau.taille)

    def jouer_coup(self):
        """
        Choisi et joue le meilleur coup possible pour le joueur actuel basé sur l'évaluation de l'état du plateau après chaque coup potentiel.

        Retourne:
            tuple: Le meilleur coup trouvé sous la forme d'un tuple (x, y), où x et y sont les coordonnées du coup sur le plateau.
        """
        coups_possibles = self.generer_coups_possibles()
        meilleur_score = float('-inf')
        meilleur_coup = None

        for coup in coups_possibles:
            plateau_temp = self.plateau.copier()
            plateau_temp.placer_pierre(*coup, self.joueur_actuel.couleur)
            score = self.evaluation_actuelle.evaluer(plateau_temp)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup

        return meilleur_coup

    def generer_coups_possibles(self):
        """
        Génère une liste de tous les coups possibles sur le plateau de jeu actuel basés sur les cases vides disponibles.

        Retourne:
            list of tuples: Une liste de tuples, chaque tuple représentant les coordonnées (x, y) d'un coup possible.
        """
        return [(x, y) for x in range(self.plateau.taille) for y in range(self.plateau.taille) if self.plateau[x][y] == '.']

    def jouer_partie(self):
        """
        Exécute la séquence de jeu pour une partie complète jusqu'à ce qu'un joueur gagne ou que le plateau soit rempli sans vainqueur.

        Retourne:
            str: La couleur du gagnant ('B' ou 'N') si un joueur gagne, sinon None si la partie se termine par un match nul.
        """
        while not self.plateau.est_jeu_termine():
            self.afficher_plateau()
            coup = self.jouer_coup()
            if coup is not None and self.plateau.placer_pierre(*coup, self.joueur_actuel.couleur):
                print(f"{self.joueur_actuel.nom} ({self.joueur_actuel.couleur}) joue: {coup}")
                if self.plateau.verifier_victoire(*coup, self.joueur_actuel.couleur):
                    print(f"{self.joueur_actuel.nom} remporte la partie !")
                    self.afficher_plateau()
                    return self.joueur_actuel.couleur
            else:
                print(f"Coup invalide de {self.joueur_actuel.nom}: {coup}")
            self.changer_joueur()

    def changer_joueur(self):
        """
        Change le joueur actuel à l'autre joueur, alternant entre le joueur1 et le joueur2.

        Retourne:
            None
        """
        if self.joueur_actuel == self.joueur1:
            self.joueur_actuel = self.joueur2
            self.evaluation_actuelle = self.evaluation2
        else:
            self.joueur_actuel = self.joueur1
            self.evaluation_actuelle = self.evaluation1
        print(f"Changement de joueur, c'est maintenant au tour de {self.joueur_actuel.nom}")

