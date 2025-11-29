import numpy as np

#ITERARE GLI ARRAY NUMPY

ar=np.array([10,20,30,40,50])
print("**********************")
print("Iterare su un array 1D")
print("**********************")
for i in ar:
    print(i)

print("**********************")
print("Iterare su un array 2D")
print("**********************")
br=np.array([[1,2,3],[4,5,6],[7,8,9]])
print("iterare scorrendo sulle righe")
for row in br:
    print(row)
print("per iterare su tutti gli elementi bisogna fare un ciclo annidato sulle righe e sulle colonne")
for row in br:
    print("riga")
    for elem in row:
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