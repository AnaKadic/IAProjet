from plateau.plateau import Plateau
from joueur.joueur import JoueurHumain
from strategie.minmax import MinimaxStrategy
from strategie.evaluation import Evaluation
from colorama import Fore, Style, init
import os


init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_titre(titre):
    clear_screen()
    print( Fore.LIGHTBLACK_EX +f"{'-' * 60}\n{titre.center(60)}\n{'-' * 60}")
    taille_titre = len(titre) + 4  # Ajoute de l'espace autour du titre
    print(Style.BRIGHT + Fore.GREEN + '=' * taille_titre)
    print(Fore.GREEN + f"| {titre} |")
    print(Fore.GREEN + '=' * taille_titre + Style.RESET_ALL)

    

def afficher_menu_principal():
    # Affiche le titre en gris anthracite
    afficher_titre(Fore.LIGHTBLACK_EX + "Bienvenue dans le jeu de Gomoku!" + Style.RESET_ALL)

    # Options du menu en vert pour les numéros et gris pour le texte
    print(Fore.GREEN + "[1]" + Fore.LIGHTBLACK_EX + " Jouer contre l'IA" + Style.RESET_ALL)
    print(Fore.GREEN + "[2]" + Fore.LIGHTBLACK_EX + " Règles du jeu" + Style.RESET_ALL)
    print(Fore.GREEN + "[3]" + Fore.LIGHTBLACK_EX + " Quitter" + Style.RESET_ALL)

    # Invite de commande en gris anthracite
    choix = input(Fore.GREEN  + "Veuillez choisir une option: " + Style.RESET_ALL)

    if choix == '1':
        debuter_partie()
    elif choix == '2':
        afficher_regles()
        afficher_menu_principal()  # Retour au menu après affichage des règles
    elif choix == '3':
        print(Fore.LIGHTBLACK_EX + "Merci d'avoir joué ! À bientôt." + Style.RESET_ALL)
        exit()
    else:
        print(Fore.LIGHTRED_EX + "Choix invalide, veuillez réessayer." + Style.RESET_ALL)
        afficher_menu_principal()

def afficher_regles():
    afficher_titre("Règles du jeu Gomoku")

    print(Fore.YELLOW + "\nObjectif du jeu:" + Style.RESET_ALL)
    print("Le but est d'aligner exactement cinq de ses pierres, horizontalement, verticalement ou diagonalement.")

    print(Fore.YELLOW + "\nDéroulement de la partie:" + Style.RESET_ALL)
    print("Les joueurs placent à tour de rôle une pierre sur une intersection vide du plateau. Les noirs débutent toujours.")

    print(Fore.YELLOW + "\nComment gagner:" + Style.RESET_ALL)
    print("Aligner cinq de ses pierres sans interruption. Les alignements de plus de cinq pierres ne comptent pas.")

    print(Fore.YELLOW + "\nFin de la partie:" + Style.RESET_ALL)
    print("Lorsqu'un joueur gagne par un alignement de cinq ou si le plateau est plein, la partie est nulle si aucun joueur n'a gagné.")

    print(Fore.LIGHTBLUE_EX + "\nPour débuter une partie, choisissez la difficulté de l'IA:" + Style.RESET_ALL)
    print("facile, moyen ou difficile (tapez le mot correspondant).")

    input(Fore.CYAN + "\nAppuyez sur Entrée pour retourner au menu principal..." + Style.RESET_ALL)




def debuter_partie():
    clear_screen()
    joueur_couleur = 'N'  # Suppose que le joueur humain joue avec les blancs
    ia_couleur = 'B'      # L'IA joue avec les noirs

    print(Fore.LIGHTBLACK_EX + "\nDébut de la partie:")
    print(Fore.LIGHTBLACK_EX + "Vous êtes les pierres blanches {Fore.WHITE + '○' + Style.RESET_ALL}.")
    print(Fore.LIGHTBLACK_EX + "L'IA est les pierres noires {Fore.BLACK + '●' + Style.RESET_ALL}.\n")

    difficulte = input(Fore.LIGHTBLACK_EX + "Choisissez la difficulté de l'IA (facile, moyen, difficile): ").lower()
    print("\n")
    while difficulte not in ['facile', 'moyen', 'difficile']:
        print("Difficulté non reconnue. Veuillez choisir entre facile, moyen et difficile:")
        difficulte = input().lower()

    plateau_de_jeu = Plateau()
    joueur_n = JoueurHumain(joueur_couleur)  
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
    
