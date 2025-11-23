"""
crea una classe Lirbo con attributi titolo e autore
* __init__ inizializza i valori
* __str__ restituisci la presentazione del libro
"""

class Libro:
    def __init__(self, titolo, autore):
        self.titolo=titolo
        self.autore=autore
    def __str__(self):
        return f"Titolo: {self.titolo}, autore: {self.autore}"
    
l1=Libro("Libro 1", "Autore 1")
l2=Libro("Libro 2", "Autore 2")
print(l1)
