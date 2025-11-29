import numpy as np

a=np.array([10, 25, 30, 45, 60, 75, 80, 95, 100, 20])
print(np.where(a==25))  #ricerca elemento presente
print(np.where(a==100))  #ricerca elemento presente
print(np.where(a==50))  #ricerca elemento non presente
print(np.where(a>50))  #ricerca elementi maggiori di 50
print(np.where(a%2==0))  #ricerca elementi pari 

print("**********************")
print("Filtrare array con condizione")
b=a[a>50]

print(a)
print(b)