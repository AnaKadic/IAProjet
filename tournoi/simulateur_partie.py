
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
        """
        Initialise le simulateur avec deux joueurs et un plateau.

        Entrées:
            joueur1 (JoueurIA): Le premier joueur.
            joueur2 (JoueurIA): Le deuxième joueur.
            plateau (Plateau): Le plateau de jeu utilisé.
        """
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.plateau = plateau
        self.joueur_actuel = joueur1

    def jouer_partie(self):
        """
        Exécute la logique de la partie, alternant les tours entre les joueurs jusqu'à ce que la partie soit terminée.

        Sortie:
            str: La couleur du joueur gagnant, ou None si la partie se termine autrement.
        """
        while not self.plateau.est_jeu_termine():
            coup_valide = False
            while not coup_valide:
                coup = self.joueur_actuel.jouer_coup(self.plateau)
                if coup is not None and self.plateau.placer_pierre(*coup, self.joueur_actuel.couleur):
                    print(f"{self.joueur_actuel.nom} ({self.joueur_actuel.couleur}) joue: {coup}")
                    coup_valide = True
                    if self.plateau.verifier_victoire(*coup, self.joueur_actuel.couleur):
                        print(f"{self.joueur_actuel.nom} remporte la partie !")
                        return self.joueur_actuel.couleur
                else:
                    print(f"Coup invalide de {self.joueur_actuel.nom}: {coup}")
                    if not self.joueur_actuel.est_ia:
                        print("Veuillez choisir un autre coup.")
            if coup_valide:
                self.changer_joueur()

    def changer_joueur(self):
        """
        Change le joueur actuel à l'autre joueur.
        """
        self.joueur_actuel = self.joueur2 if self.joueur_actuel == self.joueur1 else self.joueur1
        print(f"Changement de joueur, c'est maintenant au tour de {self.joueur_actuel.nom}")
