from plateau.plateau import Plateau
from joueur.joueur import JoueurHumain  
from strategie.ia import IA

def afficher_menu():
    print("""
    Bienvenue dans le jeu GOMOKU!
    1. Jouer
    2. Règles du jeu
    3. Quitter
    """)

def afficher_regles():
    print("""
    REGLE DE GOMOKU :
    Le Gomoku se joue sur un plateau de 15x15 cases.
    Le but du jeu est d'aligner 5 pierres de sa couleur horizontalement, verticalement, ou diagonalement.
    Le joueur 'N' commence le jeu.
    """)

def main():
    while True:
        afficher_menu()
        choix = input("Entrez votre choix (1, 2, 3): ")
        
        if choix == '1':
            print("\nVous êtes le joueur 'N', et l'IA est le joueur 'B'. Bonne chance !")
            input("Appuyez sur Entrée pour commencer...")

            plateau_de_jeu = Plateau()
            joueur_n = JoueurHumain('N')
            joueur_b = IA('B')
            joueur_actuel = joueur_n

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
                    print("\nL'IA réfléchit...")
                    ligne, colonne = joueur_actuel.choisir_coup(plateau_de_jeu)
                    plateau_de_jeu.placer_pierre(ligne, colonne, joueur_actuel.couleur)
                    print(f"L'IA a joué en ligne {ligne + 1}, colonne {colonne + 1}.")

                if plateau_de_jeu.verifier_victoire(ligne, colonne, joueur_actuel.couleur):
                    plateau_de_jeu.afficher_plateau()
                    gagnant = "Le joueur" if joueur_actuel == joueur_n else "L'IA"
                    print(f"{gagnant} a gagné !")
                    break

                joueur_actuel = joueur_b if joueur_actuel == joueur_n else joueur_n

            if plateau_de_jeu.est_jeu_termine():
                print("Match nul ! Le plateau est plein.")
            break
        elif choix == '2':
            afficher_regles()
        elif choix == '3':
            print("Merci d'avoir joué à Gomoku. À bientôt !")
            break
        else:
            print("Choix non valide, veuillez réessayer.")

if __name__ == "__main__":
    main()
