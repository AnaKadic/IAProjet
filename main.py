from plateau.plateau import Plateau
from joueur.joueur import JoueurHumain
from strategie.minmax import MinimaxStrategy
#from strategie.evaluation import Evaluation
from tournoi.gestionnaire_tournoi import GestionnaireTournoi
from joueur.joueur_ia import JoueurIA
from colorama import Fore, Style, init
import os

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_titre(titre):
    clear_screen()

    taille_titre = len(titre) + 4  # Ajoute de l'espace autour du titre
    print(Style.BRIGHT + Fore.GREEN + '=' * taille_titre)
    print(Fore.GREEN + f"| {titre} |")
    print(Fore.GREEN + '=' * taille_titre + Style.RESET_ALL)
    

def afficher_menu_principal():
    afficher_titre("Bienvenue dans le jeu de Gomoku!")

    print(Fore.GREEN + "[1]" + Fore.LIGHTWHITE_EX + " Jouer contre l'IA")
    print(Fore.GREEN + "[2]" + Fore.LIGHTWHITE_EX + " Organiser un tournoi IA")
    print(Fore.GREEN + "[3]" + Fore.LIGHTWHITE_EX + " Règles du jeu")
    print(Fore.GREEN + "[4]" + Fore.LIGHTWHITE_EX + " Quitter")

    choix = input("Veuillez choisir une option: " + Style.RESET_ALL)

    if choix == '1':
        debuter_partie()
    elif choix == '2':
        organiser_tournoi()
    elif choix == '3':
        afficher_regles()
    elif choix == '4':
        print(Fore.RED + "Merci d'avoir joué ! À bientôt." + Style.RESET_ALL)
        exit()
    else:
        print(Fore.LIGHTRED_EX + "Choix invalide, veuillez réessayer." + Style.RESET_ALL)
        afficher_menu_principal()

def organiser_tournoi():
    plateau = Plateau()  # Créez un plateau de jeu unique pour tous les matchs si nécessaire
    joueurs = [
        JoueurIA('B', 'facile', plateau, 'IA Facile', est_ia=True),
        JoueurIA('N', 'moyen', plateau, 'IA Moyen', est_ia=True),
        JoueurIA('B', 'difficile', plateau, 'IA Difficile', est_ia=True)
    ]
    gestionnaire = GestionnaireTournoi(joueurs)
    gestionnaire.organiser_tournoi()
    gestionnaire.afficher_resultats()
    


def afficher_regles():
    afficher_titre("Règles du jeu Gomoku")

    # Utilisation de différentes couleurs pour chaque section
    print(Fore.YELLOW + "Objectif du jeu:" + Style.RESET_ALL)
    print("Le Gomoku, parfois appelé 'Five in a Row', se joue sur un plateau carré, habituellement de 19x19 lignes, mais parfois de 15x15 pour des parties plus rapides. L'objectif est d'aligner exactement cinq de ses pierres, horizontalement, verticalement ou diagonalement.")

    print(Fore.YELLOW + "\nDéroulement de la partie:" + Style.RESET_ALL)
    print("Les joueurs, l'un avec les pierres noires, l'autre avec les blanches, jouent alternativement, posant une pierre sur les intersections vides du plateau. Les noirs commencent.")

    print(Fore.YELLOW + "\nComment gagner:" + Style.RESET_ALL)
    print("Le premier joueur à aligner cinq de ses pierres sans interruption gagne. Les alignements de plus de cinq pierres ne comptent pas.")

    print(Fore.YELLOW + "\nFin de la partie:" + Style.RESET_ALL)
    print("La partie se termine lorsqu'un joueur aligne cinq pierres ou si le plateau est complètement rempli sans qu'aucun joueur n'ait gagné, auquel cas la partie est déclarée nulle.")

    input(Fore.CYAN + "\nAppuyez sur Entrée pour retourner au menu principal..." + Style.RESET_ALL)
    
def post_game_options():
    print("Options : ")
    print(Fore.CYAN + "Que souhaitez-vous faire ensuite ?")
    print(Fore.CYAN + "[1]" + Fore.WHITE + " Changer d'adversaire.")
    print(Fore.CYAN + "[2]" + Fore.WHITE + " Retourner au menu principal.")
    print(Fore.CYAN + "[3]" + Fore.WHITE + " Quitter le jeu.\n")
    
    choix = input(Fore.CYAN + "Entrez le numéro de votre choix : " + Style.RESET_ALL)
    
    while choix not in ['1', '2', '3']:
        print(Fore.RED + "Choix invalide. Veuillez choisir entre 1, 2, 3, ou 4 :")
        choix = input(Fore.CYAN + "Entrez le numéro de votre choix : " + Style.RESET_ALL)


    if choix == '1':
        debuter_partie()  # permet de choisir une nouvelle difficulté.
    elif choix == '2':
        afficher_menu_principal()
    elif choix == '3':
        print(Fore.RED + "Merci d'avoir joué ! À bientôt." + Style.RESET_ALL)
        exit()

def debuter_partie():
    clear_screen()
    afficher_titre("Début de la partie")
    print(Fore.CYAN + "Vous êtes les pierres blanches ( ○ ).")
    print(Fore.CYAN + "L'IA est les pierres noires ( ● ).\n")

    print(Fore.CYAN + "Choisissez la difficulté de l'IA :")
    print(Fore.CYAN + "[1]" + Fore.WHITE + " Facile - Idéal pour bien débuter :).")
    print(Fore.CYAN + "[2]" + Fore.WHITE + " Moyen - Un bon défi de niveau Moyen.")
    print(Fore.CYAN + "[3]" + Fore.WHITE + " Difficile - Préparez-vous à un vrai défi !.\n")
    print(Fore.CYAN + "[4]" + Fore.WHITE + " Retour au menu principal.\n")
    
    difficulte_options = {'1': 'facile', '2': 'moyen', '3': 'difficile', '4': 'menu'}
    choix = input(Fore.CYAN + "Entrez le numéro de votre choix : " + Style.RESET_ALL)
    
    while choix not in difficulte_options:
        print(Fore.RED + "Choix invalide. Veuillez choisir entre 1 (Facile), 2 (Moyen), et 3 (Difficile), ou 4 pour retourner au menu :")
        choix = input().lower()

    if difficulte_options[choix] == 'menu':
        afficher_menu_principal()
        return
    
    difficulte = difficulte_options[choix]
    plateau_de_jeu = Plateau()
    joueur_couleur = 'B'  # L'IA joue avec les noirs
    ia_couleur = 'N'      # Le joueur humain joue avec les blancs

    joueur_n = JoueurHumain(ia_couleur)  # Humain joue blanc
    strategie_ia = MinimaxStrategy(plateau_de_jeu, joueur_couleur, difficulte)  # L'IA prend la couleur noire

    joueur_actuel = joueur_n  # Le joueur humain commence

    while not plateau_de_jeu.est_jeu_termine():
        plateau_de_jeu.afficher_plateau()
        if isinstance(joueur_actuel, JoueurHumain):
            coup_valide = False
            while not coup_valide:
                try:
                    ligne, colonne = joueur_actuel.demander_coup()
                    if (ligne, colonne) == ('q', 'q'):  # Si le joueur entre 'q' pour quitter
                        afficher_menu_principal()
                        return
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
        joueur_actuel = strategie_ia if joueur_actuel == joueur_n else joueur_n

    if not plateau_de_jeu.verifier_victoire(ligne, colonne, joueur_actuel.couleur):
        print("Match nul ! Le plateau est plein.")
    
    post_game_options()

if __name__ == "__main__":
    afficher_menu_principal()
    
