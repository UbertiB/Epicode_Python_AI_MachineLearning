"""
crea una classe Studente con attributi nome ed eta
* istasnzia due studenti diversi e stampa i dati
1) aggiungi alla classe Studente un metodo presentati() che stampi un messaggio nome ed età
2) prova ad aggiungere un attributo "al volo" a uno studente
"""

class Studente:
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def presentati(self):
        return f"Mi chiamo {self.nome} ed ho {self.eta} anni."
    
Giorgio=Studente("Giorgio",20)
Anna=Studente("Anna",22)
print (Giorgio.presentati())
print (Anna.presentati()) 
#attributo al volo
Giorgio.scuola="matematica"  
print (f" {Giorgio.presentati()} frequenta il corso di: {Giorgio.scuola}")