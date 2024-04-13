from plateau.plateau import Plateau
from joueur.joueur import JoueurHumain
from strategie.minmax import MinimaxStrategy
from strategie.evaluation import Evaluation
from colorama import Fore, Style, init

# Initialise Colorama pour permettre l'utilisation de couleurs dans la console
init(autoreset=True)
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_titre(titre):
    clear_screen()
    print(f"{'-' * 60}\n{titre.center(60)}\n{'-' * 60}")

def afficher_menu_principal():
    afficher_titre("Bienvenue dans le jeu de Gomoku!")
    print("[1] Jouer contre l'IA")
    print("[2] Règles du jeu")
    print("[3] Quitter")
    choix = input("\nVeuillez choisir une option: ")

    if choix == '1':
        debuter_partie()
    elif choix == '2':
        afficher_regles()
        afficher_menu_principal()  # Retour au menu après affichage des règles
    elif choix == '3':
        print("Merci d'avoir joué ! À bientôt.")
        exit()
    else:
        print("Choix invalide, veuillez réessayer.")
        afficher_menu_principal()


def afficher_regles():
    afficher_titre("Règles du jeu")
    print("Le Gomoku se joue sur un plateau de 15x15 cases.")
    print("Le but du jeu est d'aligner cinq pierres de sa couleur.")
    print("Les alignements peuvent être horizontaux, verticaux ou diagonaux.")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")
    afficher_menu_principal()
    print("Début de la partie : Vous êtes 'N', l'IA est 'B'.")
    difficulte = input("Choisissez la difficulté de l'IA (facile, moyen, difficile): ").lower()

    while difficulte not in ['facile', 'moyen', 'difficile']:
        print("Difficulté non reconnue. Veuillez choisir entre facile, moyen et difficile:")
        
        difficulte = input().lower()

def debuter_partie():
    clear_screen()
    joueur_couleur = 'N'  # Suppose que le joueur humain joue avec les blancs
    ia_couleur = 'B'      # L'IA joue avec les noirs

    print(f"\nDébut de la partie:")
    print(f"Vous êtes les pierres blanches {Fore.WHITE + '○' + Style.RESET_ALL}.")
    print(f"L'IA est les pierres noires {Fore.BLACK + '●' + Style.RESET_ALL}.\n")

    difficulte = input("Choisissez la difficulté de l'IA (facile, moyen, difficile): ").lower()
    print("\n")
    while difficulte not in ['facile', 'moyen', 'difficile']:
        print("Difficulté non reconnue. Veuillez choisir entre facile, moyen et difficile:")
        difficulte = input().lower()

    plateau_de_jeu = Plateau()
    joueur_n = JoueurHumain(joueur_couleur)  # Assurez-vous que JoueurHumain peut prendre une couleur
    joueur_b = MinimaxStrategy(plateau_de_jeu, ia_couleur, difficulte)  # L'IA prend la couleur noire
    strategie_ia = MinimaxStrategy(plateau_de_jeu, ia_couleur, difficulte)

    joueur_actuel = joueur_n

    while not plateau_de_jeu.est_jeu_termine():
        plateau_de_jeu.afficher_plateau()
        if isinstance(joueur_actuel, JoueurHumain):
            coup_valide = False
            while not coup_valide:
                try:
                    ligne, colonne = joueur_actuel.demander_coup()
                    coup_valide = plateau_de_jeu.placer_pierre(ligne, colonne, joueur_actuel.couleur)
                except ValueError as e:
                    print(e)
        else:
            print("\nL'IA réfléchit...")
            ligne, colonne = strategie_ia.choisir_coup()
            plateau_de_jeu.placer_pierre(ligne, colonne, joueur_actuel.couleur)
            print(f"L'IA a joué en ligne {ligne + 1}, colonne {colonne + 1}.")

        if plateau_de_jeu.verifier_victoire(ligne, colonne, joueur_actuel.couleur):
            plateau_de_jeu.afficher_plateau()
            gagnant = "Vous" if joueur_actuel == joueur_n else "l'IA"
            print(f"{gagnant} a gagné !")
            break
        joueur_actuel = joueur_b if joueur_actuel == joueur_n else joueur_n

    if not plateau_de_jeu.verifier_victoire(ligne, colonne, joueur_actuel.couleur):
        print("Match nul ! Le plateau est plein.")

if __name__ == "__main__":
    afficher_menu_principal()
    
