"""
crea una classe Forma con metodo area()
creau due classi derivate
- rettangolo: area=base*altezza
- cerchio: area=pigreco * raggio al quadrato
crea una lista di forme e stampa l'are di ciascuna usando lo stesso metodo area()
"""

class Forma:
    def __init__(self):
        pass
    def area(self):
        pass
class Rettangolo(Forma):
    def __init__(self, base, altezza):
        self.base=base
        self.altezza=altezza
    def area(self):
        return self.base*self.altezza
class Cerchio(Forma):
    def __init__(self,raggio):
        self.raggio=raggio
    def area(self):
        return 3.14159*(self.raggio **2)
    
r1=Rettangolo(3,4)
r2=Rettangolo(5,1)
r3=Rettangolo(6,2)
c1=Cerchio(6)
c2=Cerchio(5)
c3=Cerchio(6)
lista=[r1,r2,r3,c1,c2,c3]
for l in lista:
    print (l.area())
