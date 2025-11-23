"""
Crea una classe automobile con 
- variabile di classe ruote=4
- variabile di istanza modello
crea due automobili con modelli diversi e stampa il numero di ruote e i modelli
"""

class Automobile:
    ruote=4
    def __init__(self, modello):
        self.modello=modello
        Automobile.ruote+=1
    def __str__(self):
        return f"Modello {self.modello} con {Automobile.ruote} ruote"
    
c1=Automobile("Fiat")
c2=Automobile("Volvo")
print(c1)