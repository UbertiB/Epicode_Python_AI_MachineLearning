"""
Crea una classe Studente() con attributo eta.
se l'eta è negativa solleva EtaNonValidaError
crea una classe Magazzino() con metodo rimuovi_prodotto(nome, quantita)
se non ci sono abbastanza pezzi, sollega ProdototEsauritoError
Organizza le tue eccezioni sotto una classe base ErrorScuolao ErroreMagazzino
"""
class EtaNonValida_Error (Exception):
    pass
class Studente:
    def __init__(self,nome, eta):
        if eta<0:
            raise EtaNonValida_Error("Eta negativa")
        self.nome=nome
        self.eta=eta
try:
    s1=("Mario",55)
    s2=("Maria",-5)
except ValueError as e:
    print(e)

    

        
