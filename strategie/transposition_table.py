# table_de_transposition.py

#L'utilisation de la table de transposition réduit le nombre de positions à évaluer, et accelere l'exécution de l'algorithme

class TableDeTransposition:
    def __init__(self):
        self.table = {}

    def sauvegarder(self, cle, valeur):
        """
        Sauvegarde une valeur avec une clé spécifique dans la table de transposition.
        
        Entrées:
            cle (hashable): La clé sous laquelle la valeur doit être sauvegardée.
            valeur (any): La valeur à sauvegarder.
        """
        self.table[cle] = valeur

    def rechercher(self, cle):
        """
        Cherche et retourne la valeur associée à une clé spécifique si elle existe dans la table.
        
        Entrée:
            cle (hashable): La clé dont la valeur associée doit être recherchée.

        Retourne:
            La valeur associée à la clé ou None si la clé n'est pas trouvée.
        """
        return self.table.get(cle, None)
