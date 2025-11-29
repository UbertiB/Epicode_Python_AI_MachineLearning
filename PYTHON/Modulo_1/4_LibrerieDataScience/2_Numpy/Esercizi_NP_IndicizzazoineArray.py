import numpy as np

#lista
print("**********************")
print("Array monodimensionale")
print("**********************")
a=np.array([10,20,30,40,50])
print(a)
print(type(a))  
print (a[0])  #primo elemento
print (a[1:4])  #elementi dall'indice 1 al 3
print (a[-1])  #ultimo elemento
print (f"forma: {a.shape}")  #forma dell'array
print (a.dtype)  #tipo di dato degli elementi
print (a.ndim)  #numero di dimensioni

#array multidimensionale
print("**********************")
print("Array multidimensionale")
print("**********************")

b=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(b)
print(b[0,0])  #primo elemento
print(b[1:,1:])  #sottogriglia dall'indice 1,1 in poi
print(b.shape)  #forma dell'array   
print (b.dtype)  #tipo di dato degli elementi
print (b.ndim)  #numero di dimensioni

print("**********************")
print("intervalli di indici ") 
print("**********************")
c=np.array([5,10,15,20,25])
print(c)
print(c[1:4])  #elementi dall'indice 1 al 3
print(c[:3])  #primi 3 elementi 
print(c[2:])  #dall'indice 2 in poi
print(c[-3:])  #ultimi 3 elementi
print(c[::2])  #elementi con step 2
print(c[::-1])  #array invertito
print("d")
d=np.array([[10,20,30,40],[50,60,70,80]])
print(d)
print(f"tutta la prima riga {d[0,:]}")
print(f"tutta la seconda colonna {d[:,1]}")
print(f"tutta gli elementi della secoda riga {d[1,:]}")
print(f"accedere all'utimo elemento {d[-1,-1]} ")
