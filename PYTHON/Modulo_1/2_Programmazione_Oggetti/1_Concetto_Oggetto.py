
"""
combina dati e comportamenti che può compiere
i dati lo caratterizzano
in python tutto è un oggetto (anche numeri, stringhe, ecc)
ogni oggetto è un'istanza di una classe

"""
class Cane:
    pass
fido=Cane()

""""
la classe è cane, l'oggetto è fido
1) identita: lo distingue da tutti gli altri oggetti
2) stato: dati che lo rappresentano in questo momento
3) comportamento: sono i metodi
Gli attributi sono le variabili legate ad un oggetto e ne descrivono le caratteristiche
I metodo sono delle funzioni definite in una classe e descrivono le azioni possibili
I metodo collegano dati e comportamenti allo stesso oggetto
La classe è il concetto (es Cane), è il modello, l'oggetto è l'istanza concreta (es Fido)
Non serve sempre creare nuovi oggeetti, esempio l'oggetto numero, testo, ecc
Questi oggetti hanno metodi ed attributi già predefiniti
Il vantaggio di definire nuove classi per modellare oggetti non previsti in python
"""
# Un oggetto può contenere al suo interno altri oggetti (es. classe motore, classe automobile che utilizza la classe motore)
class Motore:
    def __init__(self,cavalli):
        self.cavalli=cavalli
class Automobile:
    def __init__(self,marca,motore):
        self.marca=marca
        self.motore=motore
m=Motore(150)
auto=Automobile("Fiata",m)
print(auto.motore.cavalli) #150
