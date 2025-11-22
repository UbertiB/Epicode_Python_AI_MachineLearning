
"""
- crea una classe Persona con attributo nome e metodo presentati()
- crea una sottoclasse studente che aggiunge l'attributo corso()
  e lo include nella presentazione
- rendo l'attributo nome privato e permetti di leggerlo solo tramite un metodo dedicato
"""

class Persona:
    def __init__(self,nome):
        self._nome=nome
    def presentati(self):
        return f"Mi chiamo {self.nome}"
class Studente(Persona):
    def __init__(self, persona:Persona, corso:str):
        super().__init__(persona)
    def presentati(self):
        return super().presentati() + f" e frequento il corso: {self.corso}"
    
p=Persona("Barbara")    
s=Studente(p,"Matematica")
print(p.presentati)
    
