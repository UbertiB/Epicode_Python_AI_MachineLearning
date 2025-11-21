
import math

"""
* chiedi all'utente quanti euro ha
* chiede il prezzo di un singolo prodotot
* usa // per calcolare quante unità può comprare
* use% per calcolare quanti euro restano
"""

euro=input("Quanti euro hai? ")
prezzo=input("Quel'è il prezzo per ogni prodotot: ")
print(f"Puoi compare {euro/1936.27} per valore componente {prezzo//euro}")
print(f"puoi acquistare {euro//prezzo}")