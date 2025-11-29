class Persona:
    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta  
    def saluta(self):
        return f"Ciao, mi chiamo {self.nome} e ho {self.eta} anni." 
    