import numpy as np

# in np tutto gira intorno agli array

#creazione array convertendo una lista python
a=np.array([1,2,3,4,5])
print(a)
# type restituisce il tipo di dato
print(f"Con type ottengo il tipo dato type(a)= {type(a)}")

# da vista a array np
vista=[10,20,30,40]
arr=np.array(vista)
print(arr)  

#array multidimensionali (+ liste)
b=np.array([[1,2,3],[4,5,6]])
print(b, b.shape)  #shape restituisce la forma (righe, colonne)

#valori predefiniti
print (np.zeros((3,4)))   #array 3x4 di zeri
print (np.ones((2,3,4),dtype=np.int16))  #array 2x3x4 di uni
np.full(2,777)  #array 1*2 pieno di 7777
#np.eye(3)  #matrice identità 3x3
print (np.random.random((2,2)))  #array 2x2 di numeri casuali

print (np.arange(0,10,2))  #array da 0 a 10 con step 2
print (np.linspace(0,1,5))  #array di 5 valori equidistanti tra 0 e 1

#array casuali (anche per allenare modelli di ML)
print (np.random.rand(3,3))  #array di 3 numeri casuali tra 0 e 1
print (np.random.randint(0,10,size=(3,4)))  #array 3x4 di interi casuali tra 0 e 10

#definire il tipo di dato
print (np.array([1,2,3],dtype=float)) #array di float

