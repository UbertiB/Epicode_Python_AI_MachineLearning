import numpy as np   

print("**********************")
print("UFUNC IN NUMPY funzioni universali (funzioni matematiche che lavorano elemento per elemnte sugli array, in modo veloce ed efficiente)")
print("**********************")


a=np.array([1, 2, 3, 4, 5])
print(a)
print (np.sqrt(a))
print(a*2)
print(a+1)
print(np.add(a,a+1))
b=np.array([10, 20, 30, 40, 50])
print(np.subtract(b,6))
print(np.multiply(a,3))
print(np.dot(a,b))  
print(np.sum(b))
print(np.mean(b))
print(np.std(b))
print(np.var(b))
print(np.min(b))
print(np.max(b))
print(np.std(b))
print(np.mean(b))

print(np.add(a,b))

aa=np.array([[1,2,3]])
bb=np.array([[10],[40]])
print(f"add di due array con dimensione diversa {np.add(aa,bb)}")
