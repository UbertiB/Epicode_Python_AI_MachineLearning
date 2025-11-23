"""
sono metodo che inizia e finiscono con il doppio underscore __nome__
Ci permettono di personalizzare il comportamento dei nostri oggetti
I più utilizzati sono:
1) __init__: inizializza l'ggetto. Eseguito automaticamente ogni volta che si crea un nuovo oggetto da una classe
            inizializza i dati dell'istanza. in lui sono passati i parametri al momento della creazione.
            Init è importante perchè permette di creare oggetti con caratteristiche specifiche, e ci permette di avere dei minimo di dati necessari in ogni istanza (senza dimenticarci di importare attributi di istanza obbligatori)
2) __str__: per avere una rappresentazione testuale leggibili
            Quanto faccio oggetto.print python cerca un motodo str (di defaul), 
            se non lo trova stampa un riferimento tecnico all'oggetto, una stringa non molto leggibile.
3) __repr__: str è un metodo utilizzato per l'utente finale, repr per il programmatore
            Come str presenta l'oggetto ma in formato "tecnico"
4) __len__: definisce il comportamento della funzione len (comune a grand parte degli oggetti)
5) __eq__ : definisce il comportamento di confronto ugualianza con ==
6) __add__: comportamento dell'operatore +
7) __getitem: comportamento per accedere con le parentesi quadrate come fosse una lista o dizionario
"""

class Studente:
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def presentati(self):
        return f"Mi chiamo {self.nome} ed ho {self.eta} anni."
    def __str__(self):
        return f"ciao, mi chiamo {self.nome} ed ho {self.eta} anni."
    def __rept__(self):
        return f"Classe=Studente nome={self.nome} eta={self.eta}"
    
Giorgio=Studente("Giorgio",20)
Anna=Studente("Anna",22)
print (Giorgio.presentati())
print (Anna.presentati()) 