import numpy as np

print("**************************")
print("Concatenare array 1D")
print("**************************")
a=np.array([1,2,3])
b=np.array([4,5,6])
c=np.array([7,8,9])
#concatenare array 1D
d=np.concatenate((a,b,c))
print(f"la concatenazione dell'array a: {a} e dell array b {b} e dell'array c {c} è un array d: {d}")

print("**************************")
print("Concatenare array 2D")
print("**************************")
x=np.array([[1,2,3],[4,5,6]])
y=np.array([[7,8,9],[10,11,12]])
#concatenare array 2D lungo l'asse 0 (righe)
z0=np.concatenate((x,y),axis=0)
print(f"la concatenazione lungo l'asse 0 (righe) degli array x: \n{x} \ne y: \n{y} \né un array z0: \n{z0}")
#concatenare array 2D lungo l'asse 1 (colonne)      
z1=np.concatenate((x,y),axis=1)
print(f"la concatenazione lungo l'asse 1 (colonne) degli array x: \n{x} \ne y: \n{y} \né un array z1: \n{z1}")  
print("**************************")

z00=np.vstack((x,y))
print(f"la concatenazione verticale (vstack) degli array x: \n{x} \ne y: \n{y} \né un array z00: \n{z00}")
z11=np.hstack((x,y))
print(f"la concatenazione orizzontale (hstack) degli array x: \n{x} \ne y: \n{y} \né un array z11: \n{z11}")
print("**************************")
#stacking con dstack (terza dimensione)
z2=np.dstack((x,y))
print(f"la concatenazione in profondità (dstack) degli array x: \n  {x} \ne y: \n{y} \né un array z2: \n{z2}")

print("**************************")
#stacking con stack (specificando l'asse)
z3=np.stack((x,y),axis=0)
print(f"la concatenazione con stack lungo l'asse 0 degli array x: \n{x} \ne y: \n{y} \né un array z3: \n{z3}")

    
