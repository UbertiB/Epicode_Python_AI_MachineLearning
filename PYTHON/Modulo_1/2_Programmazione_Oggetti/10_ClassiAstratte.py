"""
classi astratte: sono classi che non possono essere istanziate direttamente
Servono come modelli per altri classi, stabilendo quali metodi devono essere implementati dalle sottoclassi.
Tutte le classi che ereditano la classe astratta devonoi fornire la propria implementazione di metodi 
Evitano la creazione di oggetti incompleti
Forniscono una struttura comune
Facilitano la manutenzione e la coerenza del codice
Rendono chiaro il programma, quali metodo una classe derivata deve obbligatoriamente implemetare
In python le classi astratte si realizzano con il modulo abc
"""
from abc import ABC,abstractclassmethod

class Animale (ABC):
    @abstractclassmethod
    def verso(self):
        pass
    @abstractclassmethod
    def cammina(self):
        pass
class Cane(Animale):
    def verso(self):
        print("Bau")
    def cammina(self):
        print("un passo")
class Gatto(Animale):
    def verso(self):
        print("Miao")
    def cammina(self):
        print("salta")
c=Cane()
g=Gatto()
g.verso()
c.verso()
c.cammina()
g.cammina()
"""
garantisco che tutte le classi animale abbiano il metodo verso
"""
    