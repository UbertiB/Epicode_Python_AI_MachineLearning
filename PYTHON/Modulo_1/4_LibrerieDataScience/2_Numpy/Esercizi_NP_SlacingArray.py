#slacing ci permette di selezionare porzioni di array numpy
import numpy as np

print("**************************")
print("SLACING ARRAY 1D")
print("**************************")
a=np.array([10,20,30,40,50,60,70,80,90,100])
print(a)
print (f"elementi dall'indice 2 al 5 {a[2:6]}")  #elementi dall'indice 2 al 5
print(f"primi 3 elementi {a[:3]}")  #primi 3 elementi
print("NEGATIVI negli SLACING")
print(f"Ultimi 4 elementi {a[-4:]}")  #ultimi 4 elementi
print(f"elementi dall'indice 1 al 7 con step 2 {a[1:8:2]}")  #elementi dall'indice 1 al 7 con step 2
print("STEP negli SLACING")
print(f"elementi con step 3 {a[::3]}")  #elementi con step 3
print(f"array invertito {a[::-1]}")  #array invertito    
print("**************************")
print("SLACING ARRAY 2D")
print("**************************")
b=np.array([[1,2,3,4,5],[6,7,8,9,10]])      
print(b)
print(f"tutta la prima riga {b[0,:]}")  #tutta la prima riga
print(f"tutta la seconda colonna {b[:,1]}")  #tutta la seconda colonna
print(f"sottogriglia righe 0-1 e colonne 1-3 {b[0:2,1:4]}")  #sottogriglia righe 0-1 e colonne 1-3
