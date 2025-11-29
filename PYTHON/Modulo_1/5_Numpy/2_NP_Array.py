import numpy as np

# in np tutto gira intorno agli array

#creazione array convertendo una lista python
a=np.array([1,2,3,4,5])
print(f"Primo array NP:\n{a}")
# type restituisce il tipo di dato
print(f"Con type(a) ottengo il tipo dato {type(a)}")

#DA LISTA AD ARRAY NP
lista=[10,20,30,40]
arr=np.array(lista)
print(f"Secondo array NP:\n{arr}") 

#ARRAY MULTIDIMENSIONALI (+ liste)
b=np.array([[1,2,3],[4,5,6]])
print(f"Array NP multidimensionale:\n{b}")
print(f"con .shape ottengo la forma {b.shape}")  #shape restituisce la forma (righe, colonne)

#VALORI PREDEFINITI
print (f"np.zeros: array di 0: \n{np.zeros((3,4))}")   #array 3x4 di zeri
print (f"np.ones: array di 1 \n{np.ones((3,4),dtype=np.int16)}")  #array 2x3x4 di 1
print(f"np.full: array riempito con lo stesso valore \n{np.full(2,777)}")  #array 1*2 pieno di 7777
#np.eye(3)  #matrice identità 3x3
#RANDOM
print (f" np.random per numeri random \n{np.random.random((2,2))}")  #array 2x2 di numeri casuali
print (f"np.arange per riempire da un range \n{np.arange(0,10,2)}")  #array da 0 a 10 con step 2
print (f"np.linspace per riempire con valori equidistanti \n{np.linspace(0,1,5)}")  #array di 5 valori equidistanti tra 0 e 1
#RANDOM (anche per allenare modelli di ML)
print (f" np.random \n{np.random.rand(3,3)}")  #array di 3 numeri casuali tra 0 e 1
print (f"np.random.randinit \n{np.random.randint(0,10,size=(3,4))}")  #array 3x4 di interi casuali tra 0 e 10
#TIPO DI DATO
print (f"array con dtype per tipo di dato \n{np.array([1,2,3],dtype=float)}") #array di float

