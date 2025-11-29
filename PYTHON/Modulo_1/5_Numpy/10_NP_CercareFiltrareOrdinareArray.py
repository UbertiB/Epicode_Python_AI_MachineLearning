import numpy as np

"""
CERCARE, FILTRARE, ORDINARE, 
Importante sapere interrogare i dati in un array, 
quindi cercare valori specifici,
filtrare secondo condizioni, 
ordinare per analisi più chiare
Per trasformare un insieme grezzo di numeri in informazioni utilizzabili
"""

a=np.array([10, 25, 30, 45, 60, 75, 80, 95, 100, 20])
# NP.WHERE con valore fisso
print(np.where(a==25))  #ricerca elemento presente
print(np.where(a==100))  #ricerca elemento presente
print(np.where(a==50))  #ricerca elemento non presente
# NP.WHERE con condizioni logiche
print(np.where(a>50))  #ricerca elementi maggiori di 50
print(np.where(a%2==0))  #ricerca elementi pari 

print("**********************")
print("Filtrare array con condizione")
b=a[a>50]
print(a)
print(b)
filtro=a>15  #maschera booleana, si trasforma una condizione logica in un array di booleani
print(a[filtro])

print("**********************")
print("Ordinare array")
print(np.sort(b))  #ordina gli elementi in ordine crescente, è un nuovo array, lascindo intatto l'originale
c=np.array([3,2,1],[6,5,4])
print(np.sort(c,axis=1)) #ordina per riga