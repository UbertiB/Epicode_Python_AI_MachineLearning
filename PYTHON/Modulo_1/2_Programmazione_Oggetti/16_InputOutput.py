"""
INPUT/OUTPUT
per ricevere e restituire risultati.
Non si limitano alle funzione print() e input()
Gli oggetti stessi diventano responsabili dei loro input e dei loro output
nell'esempio l'oggetto studente chiede l'eta, quindi non è sempre il 
programma principale che chiede dati, ma anche le singole istanze
possono gestire da sole i loro input, idem per output
"""
#esempio input ed output incaspuolato nell'oggetto stesso
class Studente:
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def chiedi_eta(self):
        self.eta=int(input("Inserisci la tua eta: "))
    def presentati(self):
        print(f"Ciao, sono {self.nome} ed ho {self.eta} anni.")
    def __str__(self):

        return f"sono uno studente, mi chiamo {self.nome} ed ho {self.eta} anni."
    
s1=Studente("Barbara",18)    
print(s1)
s1.presentati()

"""
gli oggetti possono anche scrivere su file
"""
class Logger:
    def __init__(self, nome_file):
        self.nome_file=nome_file
    def scrivi(self,messaggio):
        with open(self.nome_file, 'a', encoding='utf-8') as f:
            f.write(messaggio + "\n")

"""
leggere da un file (esempio per inizializzare l'oggetto)
"""
class Configurazione:
    def __init__(self, nome_file):
        with open(nome_file,"r") as f:
            self.dati=f.read()

"""
input/output strutturato:
gli oggetti possono gestire dati in formati strutturati es JSON.
è un formato standard
"""
import json

class Studente:
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def salva(self, file):
        with open(file,"w") as f:
            json.dump(self.__dict__,f)

"""
JSON è molto utilizzato in informatica e scambiabile tra applicazioni.
è un formato strutturato
"""