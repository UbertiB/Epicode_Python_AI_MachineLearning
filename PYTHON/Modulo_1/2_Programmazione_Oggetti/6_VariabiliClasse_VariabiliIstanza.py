"""
Le variabili di istanza appartengono ad un singolo oggetto (esempio Fido)
Le variabili di classe sono condivise tra tutte le istanza della stessa classe (esempio contatore)
La variabili di istanza: spesso passete al metodo init (almeno quelle obbligatorie per il funzionamento della classe).
    sono sempre precedute dal self, che rappresenta l'istanza stessa
    Dati unici per ogni istanza, identificano l'istanza stessa e la caratterizzano

Le variabili di classe sono sempre preceduta da cls, sono in comune a tutte le istanze dello stesso oggetto
    Condivise tra tutte le istanza della stessa classe. Definite al di fuori del costruttore init
    direttamente all'interno della classe.
    La modifica di una variabile di classe, utilizzando la classe, si ripropaga a tutti gli oggetti della classe
    La modifica di una variabile di classe, utilizzando l'oggetto specifico, non si ripropaga a tutti gli oggetti della classe, ma python crea un duplicato della variabile solo per quell'istanza
    La variabili di classe devono essere utilizzate per criterio, 
    esempio dati condivisi (esempio contatore), 
    costanti comuni (esempio taso di interesse), 
    impostazioni generali
"""

class Studenti:
    conteggio_studenti=0
    def __init__(self, nome):
        self.nome=nome
        Studenti.conteggio_studenti+=1
        