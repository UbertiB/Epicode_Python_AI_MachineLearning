""""
I decoratori sono uno strumento potente in Python che permette di modificare il comportamento di una funzione o di una classe senza modificarne il codice sorgente. Un decoratore è fondamentalmente una funzione che prende un'altra funzione come argomento, ne estende o modifica il comportamento e restituisce una nuova funzione.
senza alterare il suo codice interno.
L'oggetto originale rimane intatto, ma possiamo aggiungere funzionalità extra intorno ad esso.
Utilizzato per gestire motodi speciale, controllare accesso agli attrubiti (property), mantenere codice + pulito. 
Ci sono decoratori già predefiniti
i principali sono: 
- staticmethod: legato alla classe, non riceve self, definisce metodi che non dipendono dall'oggetto o dalla classe. Non può accedere a dati di istanza o di classe.
- classmethod: legato alla classe, riceve cls, definisce metodo che dipendono dalla classe. Ha accesso alla classe stessa ma non ai dati di istanza (singolo oggetto).
- property: lavora a livello di istanza, permette di trattare un metodo come fosse un attributo. Utili per incapsulare l'accesso agli attributi di un oggetto in modo controllato.  
- nome.setter: lavora a livello di istanza, permette di controllare come un attributo viene modificato. Esempio per validare i dati prima di assegnarli o eseguire azioni aggiuntive quando un attributo viene modificato.
Si può impedire che un valore venga impostato con un valore non valido.

"""

#
#statichemethod, utile per le funzioni di utilità che non dipendono dalla classe o dall'istanza, non accede ai dati della classe o dell'oggetto
#

#Organizzato all'interno di una classe per motivi di ordine.
class Matematica:
    @staticmethod
    def add(a, b):
        return a + b    
print(Matematica.add(5, 3))  # Output: 8

#
#classmethod, utile per creare metodi che operano sulla classe (ricevo come parametro cls).
#

# Utile per creae dei costruttori alternativi, o per avere un contatore a livello di oggetto.
class Persona:
    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta

    @classmethod
    def from_string(cls, data_str):
        nome, eta = data_str.split('-')
        return cls(nome, int(eta))
persona1 = Persona.from_string("Mario-30")
print(persona1.nome)  # Output: Mario

class Contatore:
    conteggio = 0

    def __init__(self):
        Contatore.conteggio += 1

    @classmethod
    def get_conteggio(cls):
        return cls.conteggio
print(Contatore.get_conteggio())  # Output: 0

#
#property, utile per gestire l'accesso agli attributi di un oggetto in modo controllato.
#
class Rettangolo:
    def __init__(self, larghezza, altezza):
        self._larghezza = larghezza
        self._altezza = altezza

    @property
    def area(self):
        return self._larghezza * self._altezza

    @property
    def larghezza(self):
        return self._larghezza

    @larghezza.setter
    def larghezza(self, valore):
        if valore <= 0:
            raise ValueError("La larghezza deve essere positiva.")
        self._larghezza = valore
    
rettangolo = Rettangolo(4, 5)
print(rettangolo.area)  # Output: 20


#
# Esempio combinato
#
class ContoBancario:
    def __init__(self, saldo):
        self._saldo=saldo
    @staticmethod  #non accede ai dati della classe e dell'instanza
    def valuta_importo(importo):
        if importo < 0:
            raise ValueError("L'importo non può essere negativo.")
        return importo
    @classmethod #accedo solo ai dati della classe
    def da_stringa(cls,s):
        return cls(float(s))
    @property #accede ai dati dell'istanza, come fosse il get di un attributo
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valore): #controllo l'assegnazione del valore
        if valore < 0:
            raise ValueError("Il saldo non può essere negativo.")
        self._saldo = valore

conto = ContoBancario.da_stringa("1000.50")
print(conto.saldo)  # Output: 1000.5
conto.saldo = 1500.75
print(conto.saldo)  # Output: 1500.75
try:
    conto.saldo = -500  # Questo solleverà un ValueError
except ValueError as e:
    print(e)  # Output: Il saldo non può essere negativo.
    