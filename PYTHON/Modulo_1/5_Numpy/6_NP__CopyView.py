import numpy as np

"""
COPY:
copy crea una copia dell'array originale, ma non puntano alla stessa memoria sono due elementi diversi
Crea effettivamente una copia quindi può essere lento quando l'array è molto grande.
VIEW:
view è una finestra sui dati già esistenti, praticamente stiamo lavorando con lo stesso array 
(memorizzato nella stessa posizoine di memoria) solo che è filtrato in base alla view. 
Creare una view è più veloce rispetto alla copy, ma lavora con gli stessi dati originali

Molte operazione di np generano automaticamente una view, esempio con lo slacing 
b=a[1:3] a e b fanno riferimento alla stessa memoria
Altre operazioni generano automaticamente una copia
.copy()
oppure alcune trasformazioni che non possono essere fatte con la view
"""
print("**********************")
print("COPY IN NUMPY")
print("**********************")
a=np.array([1,2,3,4,5])  #crea un array numpy da una lista
print(f"array a: {a}")    
b=np.copy(a)  #copia dell'array a in b
print(f"array b: {b}")
b[0]=99  #modifico il primo elemento di b
print(f"dopo aver modificato b: {b}, metre a è {a}")  #a rimane invariato

print("**********************")
print("VIEW IN NUMPY")
print("**********************")
c=np.array([1,2,3,4,5])  #crea un array numpy da una lista
print(f"array c: {c}")
d=c.view()  #crea una vista dell'array c in d
print(f"array d: {d}")
d[0]=88  #modifico il primo elemento di d
print(f"dopo aver modificato d: {d}, mentre c è {c}")  #c viene modificato anche lui
e=a[:3] #crea una vista della quarta colonna di a in e
print(f"anche lo slicing è una semplice vista pertanto modificando uno modifica anche l'altro {e}")
e[0]=77  #modifico il primo elemento di e   
print(f"dopo aver modificato e: {e}, mentre a è {a}")  #a viene modificato anche lui

print("**********************")
print("COME SAPERE SE UN ARRAY È COPY O VIEW")
print("**********************")
print(f"a.base è {a.base}")  #None perché a è un array originale
print(f"b.base è {b.base}")  #None perché b è una copia di a    
print(f"d.base è {d.base}")  #c perché d è una vista di c


