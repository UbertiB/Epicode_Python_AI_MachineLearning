"""
Incapsulmaneto insieme ad eriditarieta ed polimorfismo sono i 3 pilastri della programmazione ad oggetti
l'incapsulmaento nasconde dettagli e fornire all'esterno solo quello che serve.
Utile per proteggere i dati per evitare modifiche errate.
Chi usa l'oggetto deve avere a disposizione solo ciò che serve
senza toccare i dettagli interni.
pubblico: variabile - accessibile ovunque
protetto:_variabile - suggerisce che è per uso interno, non toccare (anche se non è veramente privata)
privato: __variabile - reso meno accessibile con name mangling, anche se non è impossibile accedere dall'esterno.
Se vogliamo lavorare con metodi privato bisogna utilizzare metodi di accesso (getter e setter=)
getter e setter permettono accesso controllato ai dati
"""

#variabile protetta (nessun errore nell'utilizzo)
class Persona:
    def __init__(self, nome, eta):
        self.nome=nome
        self._eta=eta
p1=Persona("Giorgio", 30)
print (p1.nome)
print (p1._eta)  #questo non va in errore, perchè la variabile protetta è solo un avviso per i programmatori, non da alcun vincolo

#variabile privata (errore nell'utilizzo)
class Studente:
    def __init__(self, nome, eta):
        self.nome=nome
        self.__eta=eta
p1=Studente("Giorgio", 30)
print (p1.nome)
#print (p1.__eta)  #questo va in errore  

#variabile privata (metodo getter e seetter)
class Macchina:
    def __init__(self, nome, anno):
        self.nome=nome
        self.__anno=anno
    def get_anno(self):
        return self.__anno
    def set_anno(self,nuovo_anno):
        self.__anno=nuovo_anno
p1=Macchina("Giorgio", 30)
print (p1.nome)
print (p1.get_anno())  #non va in errore perchè c'+ getter  
p1.set_anno(31) #è un metodo quindi mettere il valore tra parentesi non dopo il simbolo = (come per le variabili)
print (p1.get_anno())  #non va in errore perchè c'+ getter  

