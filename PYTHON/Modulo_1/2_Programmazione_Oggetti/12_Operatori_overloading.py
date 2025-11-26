"""
Sovracarico degli operatore.
Dietro le quinti ogni operatore in python è associato a un metodo speciale.
Con l'operatore overloading possiamo ridefinire il comportamento di questi operatori per le nostre classi personalizzate.
In modo che funzionino in modo intuitivo con gli oggetti delle nostre classi.

- Aumenta la leggibilità del codice (esempio p1+p2, rispetto a p1.somma(p2))
- Permette di utilizzare i nostri oggetti in modo simile ai tipi built-in di Python (esempio liste, stringhe)
- Rende possibile scrivere codice matemtico
- Espressività

"""

class Punto:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self, altro):  #operatore  + 
        return Punto(self.x + altro.x, self.y + altro.y)
    def __sub__(self, altro):  #operatore -
        return Punto(self.x - altro.x, self.y - altro.y)
    def __repr__(self):  #rappresentazione stringa
        return f"Punto({self.x}, {self.y})"
p1 = Punto(2, 3)
p2 = Punto(5, 7)
p3 = p1 + p2
print(p3)  # Output: Punto(7, 10)
p4 = p2 - p1
print(p4)  # Output: Punto(3, 4)

# + add
# - sub
# * mult
# == ef
# != ne
# < lt
# <= le
# > gt
# >= ge
# str str
# repr repr


 # overloading di __str__
class Libro:
    def __init__(self, titolo, autore):
        self.titolo = titolo
        self.autore = autore
    def __str__(self):
        return f"'{self.titolo}' di {self.autore}"
libro = Libro("1984", "George Orwell")
print(libro)  # Output: '1984' di George Orwell


