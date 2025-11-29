import numpy as np

"""
SHAPE è la forma di un array, cioè quante righe e quante colonne ha, definisce le sue dimensioni
RESHAPE possibilità di cambiare la forma di un array
con reshape è una view sull'array originale, pertanto fanno riferimento alla stessa memoria
Alcune volte np crea una copia quando non è possibile fare riferimento alla stessa memoria.
quandi è necessario verificare con .base
Conoscere lo shape è importante:
- verificare la struttura dei dasti
- evitare gli errori quando si fanno operazioni sugli array
- per organizzare i dati all'interno degli array per l'elaborazioni numeriche o il machine learning
- facilita il reshape senza perdere i dati o generare errori
"""

a=np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(a)
print (f"visualizzo size [[1, 2, 3, 4], [5, 6, 7, 8]]): {a.size}")
b = a.reshape((4,2)) 
print(f"Array originale: a.shape = {a.shape}, array reshape(4,2)= {b.shape}")
print(b)

ar=np.arange(12)
print(f"Array originale ar con shape {ar.shape} : {ar}")    
br=ar.reshape((3,4))
print(f"Array reshape (3,4) br con shape {br.shape} : {br}")

c=ar.reshape((2,2,3))
print(f"Array reshape (2,2,3) c con shape {c.shape} : {c}")

d=ar.reshape(3,-1)
print(d)

#reshap non crea una copia ma fa una review dell'array originale
ar1=np.array([0])
ar2=ar1.reshape(1)
ar2[0]=88
print(ar1[0])