from enum import Enum

TAILLE_PLATEAU = 11

BLANC = "#FFFFFF"
NOIR = "#000000"
GRIS = "#222222"

changement_ligne = [-1, -1, 0, 1, 1, 1, 0, -1]
changement_colonne = [0, 1, 1, 1, 0, -1, -1, -1]


class Joueur(Enum):
    AUCUN = 0
    NOIR = 1
    BLANC = 2
