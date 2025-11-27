"""
Quando si scrive codice, gli errori sono inevitabili
Quello che fa la diferenza è come andiamo a gestire gli errori.
In Python gli errori sono rappresentati da oggetti speciali, chiamati eccezioni
Vediamo come creare eccezzioni, come valorizzarle ed utilizzarle.
Non è solo un messaggio di errorei, è un oggetto che descrive il problema.
Se non è gestita, l'eccezione interrompe l'esecuzione.
Ogni errore ha un nome, e dietro c'è una classe che lo rappresenta.
try:
except
utilizzato per gestire l'errore, il codice a rischio è da mettere all'interno di try
il codice per gestire l'errore all'interno di except
"""

try:
    x=int("abc")
except:
    print("Errore: non è un numero valido")
else: #se non c'è stata eccezione, se non ho errori
    pass
finally: #sempre eseguito con o senza errori
    pass

"""
un blocco try può generare piùdi un errore, si può avere più di un excep, ognuno
si occupa di un'eccezione specifica.
ValueErrore se scrivo una stringa non numerica
ZeroDivisionErrore, quando divido per zero.

"""

class Calcolatrice:
    def dividi(self,a,b):
        try:
            return a/b
        except:
            return "Errore: divisione per zero"
        
"""
Excep cattura l'errore, il problema è incapsulato dentro l'oggetto e 
non si propaga in modo incontrollato. Favorisce classi più robuste.
A volte non basta catturare errori, ma dobbiamo sollevarne di nuovi.
Esempio se imposto un'età minore di zero
"""
class Studente:
    def __init__(self,nome,eta):
        if eta<0:
            raise ValueError("l'eta deve essere un numero positivo")
        self.nome=nome
        self.eta=eta

try:
    p1 = Studente("Carlo", 19)
    print("Persona creata:", p1.nome, p1.eta)
    p2 = Studente("Maria", -8)  # Solleva ValueError
except ValueError as e:
    print("Errore:", e)