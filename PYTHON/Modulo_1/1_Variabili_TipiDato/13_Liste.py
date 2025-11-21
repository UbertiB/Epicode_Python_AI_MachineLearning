
"""
le liste ci permettono di manipolare grandi quantita di dati
collezioni ordinate e modificabili
possono contenere elementi di qualunque tipo, anche misti
è un contenitore di elementi, che possiamo consultare, aggiornare, trasformare
creazione con nome=[]
accedo agli elementi con l'indice nome[indice]
anche indici negativi -1 ultimo elemento
le liste sono mutabili, cioè possono essere modificate, invece le stringhe (o anche le tuple) sono immutabili
lista.extend(seq): aggiunge elementi alla fine
lista.insert(indice, elemento): aggiunte elemento alla listas nella posizione indice
lista.remove(elemento): elimina la prima occorrenza di elemento trovata
lista.sort(): ordina gli elementi dla più piccolo al più grande
lista.reverse():inverto l'ordine degli elementi
lista.copy(): crea e restituisce una copia
lista.clear(): rimuove tutti gli elementi
lista.pop(): rimuove e ristituisce l'ultimo elemento

differenza tra liste e tuple, le tuple sono immutabile mentre le liste mutabili
la lunghezza delle tuple rimane fissa (perchè sono immutabili)
la lunghezza delle liste può cambiare (posso aggiungere/rimuovere elementi)
gli elementi della lista devono essere dello stesso tipo, perchè spesso le itero
paragone con la tabella di un database
ogni riga della tabella può essere una tupla, ha elementi diversi
ogni colonna della tabella può essere una lista
"""

#crea una lista di numeri interi
numeri=[0,1,2]
numeri.append(5)
print(numeri)

#crea una lista di stringhe ed inserisce alla posizione 2
stringa=["mela","pera","banana"]
stringa.insert(2,"kiwi")
print(stringa)

#crea una lista di numeri e cancella il secondo elemento
numeri=[0,1,2,3,4]
numeri.remove(2)
print(numeri)



