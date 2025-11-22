"""
esercizi 
"""

#ordina una lista di tuple per secodo elemento delle tuple
lista=[(1,3),(2,1),(5,0)]
print(lista)
lista_ordinata=sorted(lista,key=lambda x:x[1])
print("Ordinata:", lista_ordinata)

#crea un tupla con numeri pari partendo da un altra tupla
t=(1,2,3,4,5,6)
t_pari=tuple([x for x in t if x%2==0])
print(f"numeri pari: {t_pari}.")

#inverti una tupla
t=[1,2,3,4]
t_invetita=tuple(reversed(t))
print(f"Stringa invertita: {t_invetita}.")

#converti una stringa in tupla di caratteri unici
stringa="programmazione"
t=tuple(set(stringa))
print(t)

#zippa (unisci) due liste in una lista di tuple
a=[1,2,3]
b=["a","b","c"]
zipped=list(zip(a,b))
print(zipped)

#differenza di 2 set (la differenza restituisce gli elementi di un insieme che non appartengo all'altro)
a={1,2,3}
b={3,4,5}
c={5,6}
differenza=a^b^c
print(f"differenza simmestria: {differenza}")

#filtra le parole uniche
frase="ciao come stai ciao tutto bene"
uniche=set(frase.split())
print(f"parole uniche: {uniche}")

#unione di set da lista di liste
liste=[(1,2,3),(3,4,5),(6,7)]
unione=set().union(*map(set,liste))
print(unione)

