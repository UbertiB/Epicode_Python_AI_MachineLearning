"""
crea una classe studente con
* attributo di classe scuola ="liceo classico"
* attributo di istanza nome
* metodo di istanza presentati
* metodo di classe cambia_scuola
"""

class Studente:
    scuola="liceo classico"
    def __init__(self, nome):
        self.nome=nome
    def presentati(self):
        return f"Mi chiamo {self.nome} e frequento la scuola {self.scuola}"
    @classmethod
    def Cambia_scuola(cls, scuola):
        cls.scuola=scuola

s1=Studente("Mario")
s2=Studente("Maria")
print (s1.presentati())
print (s2.presentati())
Studente.Cambia_scuola("liceo lingustico")
print (s1.presentati())
print (s2.presentati())