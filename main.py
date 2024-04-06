from plateau.plateau import Plateau
from joueur.joueur import JoueurHumain  
from strategie.ia import IA

def main():
    print("Début de la partie : Vous êtes 'N', l'IA est 'B'.", flush=True)

    # Créer une instance du plateau de jeu
    plateau_de_jeu = Plateau()
    
    # Initialise les joueurs
    joueur_n = JoueurHumain('N')  # Le joueur humain
    joueur_b = IA('B')  # Initialise l'IA avec une profondeur de recherche

    joueur_actuel = joueur_n  # Le joueur humain commence

    # Boucle de jeu principale
    while not plateau_de_jeu.est_jeu_termine():
        plateau_de_jeu.afficher_plateau()
        coup_valide = False

        if isinstance(joueur_actuel, JoueurHumain):
            while not coup_valide:
                ligne, colonne = joueur_actuel.demander_coup()
                coup_valide = plateau_de_jeu.placer_pierre(ligne, colonne, joueur_actuel.couleur)
                if not coup_valide:
                    print("Mouvement invalide, réessayez.")
        else:
            print("L'IA réfléchit...")
            ligne, colonne = joueur_actuel.choisir_coup(plateau_de_jeu)  # Assurez-vous que cette méthode retourne les bons indices
            plateau_de_jeu.placer_pierre(ligne, colonne, joueur_actuel.couleur)
            print(f"L'IA a joué en ligne {ligne + 1}, colonne {colonne + 1}.")  # +1 pour correspondre à l'affichage humain (commence par 1)
            coup_valide = True

        # Vérifie la victoire après chaque coup
        if plateau_de_jeu.verifier_victoire(ligne, colonne, joueur_actuel.couleur):
            plateau_de_jeu.afficher_plateau()
            gagnant = "le joueur" if joueur_actuel == joueur_n else "l'IA"
            print(f"{gagnant} a gagné !")
            return  # Fin du jeu en cas de victoire

        # Changer de joueur après un coup valide
        joueur_actuel = joueur_b if joueur_actuel == joueur_n else joueur_n

    print("Match nul ! Le plateau est plein.")

if __name__ == "__main__":
    main()