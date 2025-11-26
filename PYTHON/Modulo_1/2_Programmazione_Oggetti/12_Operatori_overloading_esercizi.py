"""
crea una classe Frazione che rappresenti una frazzione con numeratore e denominatore.
Implementa l'overloading degli operatori +,==,__str__
"""

class Frazione:
    def __init__(self, numeratore, denominatore):
        self.numeratore = numeratore
        self.denominatore = denominatore
    def __add__(self, altro):
        nuovo_numeratore = (self.numeratore * altro.denominatore) + (altro.numeratore * self.denominatore)
        nuovo_denominatore = self.denominatore * altro.denominatore
        return Frazione(nuovo_numeratore, nuovo_denominatore)   
    def __eq__(self, altro):
        return (self.numeratore * altro.denominatore) == (altro.numeratore * self.denominatore)
    def __str__(self):
        return f"{self.numeratore}/{self.denominatore}"
f1 = Frazione(1, 2)
f2 = Frazione(3, 4)
f3 = f1 + f2
print(f3)  # Output: 10/8
print(f1 == f2)  # Output: False
f4 = Frazione(2, 4)
print(f1 == f4)  # Output: True
