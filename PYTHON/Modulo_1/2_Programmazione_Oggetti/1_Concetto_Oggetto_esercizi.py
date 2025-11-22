"""
Scrivi una classe studente con attributi nome e corso e un metodo presentati 
che stampa una frase di presentazione
"""

class Studente:
    def __init__(self, nome:str, corso:str):
        self.nome=nome
        self.corso=corso
    def presentati(self):
        print (f"Mi chiamo: {self.nome} e frequento il corso di {self.corso}.")

s1=Studente("Mario","matematica")
s1.presentati()
