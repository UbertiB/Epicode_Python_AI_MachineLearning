import numpy as np

print("**********************")
print("NUMPY")
print("**********************")

# Creare array NumPy
dati=np.random.randint(10,100,size=(6,5))
print(f"dati orginali: \n{dati}")
print(f"shape dati: {dati.shape} \ndtype dati: {dati.dtype}")
# Accesso a elementi specifici
print(f"Elemento riga 2 colonna 3: {dati[2,3]}")
# Slicing   
print(f"Slicing righe 1-3 e colonne 2-4: \n{dati[1:4,2:5]}")
print(f"prima riga: {dati[0,:]}")
print(f"prima colonna: {dati[:,0]}")
print(f"submatrice prime due righe e prime tre colonne: \n{dati[0:2,0:3]}")
# View vs Copy
view=dati[0:2,0:2]
copy=dati[0:2,0:2].copy()
view[0,0]=999
print (f"view : {view} \n copy {copy} (la copy è invariata)")

# Reshape
reshaped=dati.reshape(3,10)
print(f"Array reshaped (3x10): \n{reshaped}")
# Iterare sugli array
print("Iterazione su ogni elemento con nditer:")
for x in np.nditer(dati):
    print(int(x), end=" ")
print()
# Concatenare e dividere array
extra=np.random.randint(10,100,size=(6,2))  
unito=np.hstack((dati,extra))
print(f"Array unito con nuove colonne: \n{unito}")

#dividere i dati con split
split=np.split(unito,2)
print(f"Array diviso in due blocchi (con split): \n{split[0]} \n {split[1]}")

# Cercare, filtrare e ordinare
mask=dati>50
print(f"Valori >50: \n{dati[mask]}")    
ordinati=np.sort(dati,axis=1)
print(f"Ogni riga ordinata: \n{ordinati}")

# Uso di ufunc
radici=np.sqrt(dati)
print(f"Radici quadrate di ogni elemento: \n{radici}")
# Statistiche con ufunc
print(f"Media per colonna: {np.mean(dati,axis=0)}")
print(f"Deviazione standard totale: {np.std(dati)}")


