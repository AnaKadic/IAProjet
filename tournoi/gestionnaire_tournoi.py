from .simulateur_partie import SimulateurPartie
from plateau.plateau import Plateau


class GestionnaireTournoi:
    """
    Gère l'organisation et l'exécution d'un tournoi de jeux entre plusieurs joueurs.
    
    Attributs :
        joueurs (list): Liste des instances de JoueurIA participant au tournoi.
        nb_parties_par_match (int): Nombre de parties jouées entre chaque paire de joueurs lors d'un match.
        resultats (list): Liste des résultats des matchs.
        scores (dict): Dictionnaire des scores des joueurs.
    """

    def __init__(self, joueurs, nb_parties_par_match=3):
        """
        Initialise le gestionnaire du tournoi avec une liste de joueurs et le nombre de parties par match.
        Entrée:
            joueurs (list): Liste des instances de JoueurIA.
            nb_parties_par_match (int): Nombre de parties que chaque paire de joueurs jouera par match.
        """
        self.joueurs = joueurs
        self.nb_parties_par_match = nb_parties_par_match
        self.resultats = []
        # Initialisation du dictionnaire des scores
        self.scores = {joueur.nom: 0 for joueur in joueurs}

    def organiser_match(self, joueur1, joueur2):
        """
        Organise et exécute un match entre deux joueurs.

        Entrées :
            joueur1 (JoueurIA): Le premier joueur du match.
            joueur2 (JoueurIA): Le second joueur du match.

        Retourne:
            dict: Un dictionnaire contenant les résultats du match (nombre de victoires, nuls, etc.).
        """
        resultats_match = {'victoires_joueur1': 0, 'victoires_joueur2': 0, 'nuls': 0}
        for _ in range(self.nb_parties_par_match):
            plateau = Plateau()
            simulateur = SimulateurPartie(joueur1, joueur2, plateau)
            gagnant = simulateur.jouer_partie()
            if gagnant == joueur1.couleur:
                resultats_match['victoires_joueur1'] += 1
                self.scores[joueur1.nom] += 3
            elif gagnant == joueur2.couleur:
                resultats_match['victoires_joueur2'] += 1
                self.scores[joueur2.nom] += 3
            else:
                resultats_match['nuls'] += 1
                self.scores[joueur1.nom] += 1
                self.scores[joueur2.nom] += 1
        return resultats_match

    def organiser_tournoi(self):
        """
        Organise et exécute le tournoi complet entre tous les joueurs.
        """
        self.reinitialiser_resultats()
        for joueur1 in self.joueurs:
            for joueur2 in self.joueurs:
                if joueur1 != joueur2:
                    self.jouer_et_enregistrer_matchs(joueur1, joueur2)

    def jouer_et_enregistrer_matchs(self, joueur1, joueur2):
        """
        Joue et enregistre les résultats pour les matchs entre deux joueurs spécifiques.

        Entrée:
            joueur1 (JoueurIA): Le premier joueur.
            joueur2 (JoueurIA): Le second joueur.
        """
        for _ in range(100): # 50 matchs par paire, comme requis par les spécifications du projet.
            resultats = self.organiser_match(joueur1, joueur2)
            self.resultats.append((joueur1, joueur2, resultats))
            resultats = self.organiser_match(joueur2, joueur1)
            self.resultats.append((joueur2, joueur1, resultats))
    
    def afficher_resultats(self):
        """
        Affiche les résultats du tournoi et le classement des joueurs.
        """
        print("Résultats du tournoi:")
        for match in self.resultats:
            joueur1, joueur2, resultats = match
            print(f"{joueur1.nom} vs {joueur2.nom}: {resultats}")

        print("\nClassement final:")
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for place, (nom, score) in enumerate(sorted_scores, start=1):
            print(f"{place}. {nom} avec {score} points")

    def reinitialiser_resultats(self):
        """
        Réinitialise les résultats et les scores pour préparer un nouveau tournoi.
        """
        self.resultats = []
        self.scores = {joueur.nom: 0 for joueur in self.joueurs}