"""
polimorfismo significa molte forme, cioè la capacità di utilzzare lo stesso metodo (o operatore)
su oggetti differenti, ottenendo comportamenti specifici per ciascun tipo di oggetto.
Questo permette di scrivere codice più flessibile e ridurre la complessità (perchè non serve conoscere bene l'oggetto che stiamo utilizzando)
Esempio il tasto ON del telecomando fa la stessa cosa per tutti i dispositivi.
Il polimorfismo semplifica il codice.
"""
class Animale:
    def verso(self):
        pass
class Cane(Animale):
    def verso(self):
        print("Bau")
    def fai_verso(animale):
        animale.verso()
class Gatto(Animale):
    def verso(self):
        print("Miao")
    def fai_verso(animale):
        animale.verso
c=Cane()
g=Gatto()
c.fai_verso()
g.fai_verso()

"""
Polimorfismo con ereditarietà
Questo è un esempio di polimorfismo, il metodo Verso() è presente nella 
classe generale Animale ma anche in ogni classe derivata.
Il programmatore non si deve preoccupare del verso di un tipo di animale rispetto
all'altro, è la classe che si comporta in modo opportuno pur richiamando lo stesso metodo.
Gli oggetti di una classe derivata devono poter sostituire gli oggetti della classe base.
La classe base definisce un metodo generico
Le classi derivate lo ridefiniscono per comportamenti specifici
Si può lavorare con qualsiasi oggetto derivato senza conoscerne i dettagli.
Polimorfismo senza ereditarietà
due classi hanno metodi con lo stesso nome, anche questo è polimorfismo
"""

class Uccello:
    def verso(serf):
        print("cip")
class Pesco:
    def verso(self):
        print("  ")

"""
il polimorfismo non riguarda solo i metodo ma anche gli operatori
esempio:
"""
print(5+3) #8
print("a"+"b") #abb
print([1],[2]) #[1,2]
"""
i metodi speciali definisco i comportamento degli operatori
__add__
__len__
__str__
, ecc
"""
class Punto:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,altro):
        return Punto(self.x+altro.x,self.y+altro.y)
    def __str__(self):
        return f"Punto({self.x}, {self.y})"
p1=Punto(2,3)
p2=Punto(4,5)
p3=(p1+p2)
print(p3)
