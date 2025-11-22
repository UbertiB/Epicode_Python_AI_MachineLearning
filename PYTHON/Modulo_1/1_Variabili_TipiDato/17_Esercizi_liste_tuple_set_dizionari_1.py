
"""
esercizi
"""

#somma dei numeri pari all'interno di una lista
numeri=[12,7,9,18,24,5,2]
print(f"la {type(numeri)} ha i seguenti valori: {numeri}.")

#somma i numeri pari
somma_pari=sum([n for n in numeri if n % 2 == 0])
print(f"Somma dei numeri pari: {somma_pari}.")

#crea un lista senza duplicati mantenendo ordine
lista=[1,2,2,3,4,4,5]
lista_senzaduplicati=[]
for x in lista:
    if x not in lista_senzaduplicati:
        lista_senzaduplicati.append(x)
print (f"Lista senza duplicati: {lista_senzaduplicati}")

#ruota a destra di k posizioni
lista=[1,2,3,4,5]
k=2
lista_ruotata=lista[-k:]+lista[:-k]
print(f"lista ruotata: {lista_ruotata}")


#fai insersezione di due liste (senza usare set)
a=[1,2,3,4] # lista[]
b=[3,4,5,6]
intersezione=([x for x in a if x in b ])
print(intersezione)

#conversione lista di tuple in dizonario
coppie=[("a",1),("b",3),("c",3)] # lista [] di dizionario ()
dict=dict(coppie)
print(dict)

#somma di tuple
tuples=[(1,2),(3,4),(5,6)]  # lista [] di tuple ()
somma= sum([sum(x) for x in tuples])
print(somma)

#tupla con massimo e minimo di una lista
numeri=[12,3,45,7,9]
risultato=(min(numeri),max(numeri))
print(risultato)


