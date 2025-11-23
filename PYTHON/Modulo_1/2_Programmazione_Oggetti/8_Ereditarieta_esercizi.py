"""
crea una classe Animale con attributo nome e metodo verso()
poi crea due classi derivate
- cane verso stampa bau
- gatto verso stampa miao
"""

class Animale:
    def __init__(self, tipo, nome):
        self.tipo=tipo
        self.nome=nome
    def verso(self):
        return f"verso "
class Cane(Animale):
    suono="bau"
    def __init__(self, nome):
        Animale.__init__(self, "cane", nome)
    def verso(self):
        return super().verso() + f" {Cane.suono}"
    
c1=Cane("Fido")
print(c1.verso())
        