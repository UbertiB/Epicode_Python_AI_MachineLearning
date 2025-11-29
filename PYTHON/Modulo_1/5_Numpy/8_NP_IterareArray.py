import numpy as np

#ITERARE GLI ARRAY NUMPY

"""
ITERARE MONODIMENSIONE
come iterare un np array (scorrere elemento per elemento)
si deve scegliere se è meglio iterare o utilizzare le operazioni vettoriali
Se l'array è monodimensionale è sufficiente iterare con una solo for
ITERARE BIDIMENSIONALE
Con un array bidimensionale non è sufficnete iterare con un solo ciclo for. 
con il primo ciclo for ottengo le righe, con il secondo cicli for gli elementi della riga (valori) 
Con un array tridimensionale ho bisogno di 3 for per arrivare fino ai valori
e così via per le altre dimensioni 
ITERARE CON NDITER
oppure posso utilizzare nditer
nditer per evitare di scrivere tanti cicli quante sono le dimensioni di un array
nditer ci permette di iterare sugli elementi dell'array come fosse piatto
ITERAZIONE CON INDICE
se oltre ad iterare devo conoscere l'indice
for idx,x in np.ndenumerate(b)
    print(idx,x)
in questo modo sappiamo esattamente in che posizione si trova il valore.

L'iterazione è un'operazione costosa e lenta, rispetto alle operazioni vettoriali
Pertanto, quando possibile, utilizzare operazione vettoriali, solo successivamente se non 
presente l'alternativa, utilizzare l'iterazione
ha senso per esempio quando ho bisogno di applicare una logica particolare a singoli elementi
oppure quando stiamo facendo dei controlli
oppure quando ci serve sapere sia il vettore che l'indice
"""

ar=np.array([10,20,30,40,50])
print("**********************")
print("Iterare su un array 1D (tramite for i in array)")
print("**********************")
for i in ar:
    print(i)

print("**********************")
print("Iterare su un array 2D (con il primo for itero le righe, con il secondo gli elementi delle righe)")
print("**********************")
br=np.array([[1,2,3],[4,5,6],[7,8,9]])
print("iterare scorrendo sulle righe")
for row in br:
    print(row)
print("per iterare su tutti gli elementi bisogna fare un ciclo annidato sulle righe e sulle colonne")
for row in br:  #itero le righe
    print("riga")
    for elem in row: #per accedere ai singoli valori della riga
        print(elem) 
print("**********************")
print("Iterare su un array 3D")
print("**********************")
cr=np.array([[[1,2],[3,4]],[[5,6],[7,8]]])
for matrix in cr:
    print("matrice")
    for row in matrix:
        print("riga")
        for elem in row:
            print(elem)
print("**********************")
print("Usare nditer per iterare su array multidimensionali")
print("**********************")
dr=np.array([[1,2,3],[4,5,6],[7,8,9]])
for x in np.nditer(dr):
    print(x)
print("**********************")
print("Iterare con indici")
print("**********************")
er=np.array([10,20,30,40,50])
for i in range(len(er)):
    print(f"Elemento all'indice {i} : {er[i]}") 
print("**********************")
print("Iterare con indici e conoscere la posizione in array multidimensionali")
print("**********************")
aa=np.array([[1,2,3],[4,5,6],[7,8,9]])
for idx,x in np.ndenumerate(aa):
    print(f"Elemento all'indice {idx} : {x}")       