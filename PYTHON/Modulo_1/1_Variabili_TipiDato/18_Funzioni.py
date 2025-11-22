
"""
le funzioni servono per evitare di ripetere lo stesso codice più volte
servono per dividere in blocchi logici
servono per rendere i programma più leggibili
nelle funzioni posso ricevere dei dati dall'esterno (parametri/argomenti)
la funzione può restituire un risultato con return
Gli argomenti possono essere posizionali (passati in ordine), con nome (indicando il nome) o con valori di default
possono avere numero argomenti variabili utilizzando *args
**kwargs raccogliamigli argomenti in un dizionario
un buon programmatore documento la sua funzione con le docstring (utilizzando triple virgolette)

esistono delle funzioni "anonime" funzioni veloce utilizzate una sola volta (funzioni lambda)
lambda argomenti:espressione
"""

#crea una funzione che restituisce il quadrato di un numero
def quadrato(n):
    return n*n
print(quadrato(2))
print(quadrato(4))

#crea una funzione con parametri di default
def saluti(nome, saluto="ciao"):
    return((f"{saluto} {nome}"))
print(saluti("Barbara"))
print(saluti("","Ettore"))
print(saluti(""))

#crea una funzione con +argomenti variabili
def somma(*args):
    return sum(args)
print(f"somma dei numeri 1,2,3 = {somma(1,2,3)}")
print(f"somma dei numeri 4,5,6 = {somma(4,5,6)}")