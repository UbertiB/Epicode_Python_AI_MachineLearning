import numpy as np

# 1. Creiamo un array di dati simulati con random
np.random.seed(42)  # per riproducibilità
dati = np.random.randint(10, 100, size=(6, 5))  # 6 righe (studenti) x 5 colonne (voti)
print("Dati originali:\n", dati)

# 2. Informazioni base: shape, dtype
print("\nShape:", dati.shape)
print("Tipo di dati:", dati.dtype)

# 3. Indicizzazione e slicing
print("\nPrima riga:", dati[0])
print("Prima colonna:", dati[:, 0])
print("Sub-matrice (prime 2 righe, prime 3 colonne):\n", dati[:2, :3])

# 4. View vs Copy
view = dati[:2, :2]
copy = dati[:2, :2].copy()
view[0, 0] = 999
print("\nDopo modifica della view:\n", dati)
print("La copy resta invariata:\n", copy)

# 5. Reshape dell’array
reshaped = dati.reshape(3, 10)
print("\nArray reshaped (3x10):\n", reshaped)

# 6. Iterare sugli array
print("\nIterazione su ogni elemento con nditer:")
for x in np.nditer(dati):
    print(int(x), end=" ")
print()

# 7. Concatenare e dividere array
extra = np.random.randint(10, 100, size=(6, 2))
unito = np.hstack((dati, extra))
print("\nArray unito con nuove colonne:\n", unito)

split = np.hsplit(unito, 2)
print("\nArray diviso in due blocchi:\n", split[0], "\n", split[1])

# 8. Cercare, filtrare e ordinare
mask = dati > 50
print("\nValori > 50:\n", dati[mask])

ordinati = np.sort(dati, axis=1)
print("\nOgni riga ordinata:\n", ordinati)

# 9. Uso di ufunc
radici = np.sqrt(dati)
print("\nRadici quadrate di ogni elemento:\n", radici)

# 10. Statistiche con ufunc
print("\nMedia per colonna:", np.mean(dati, axis=0))
print("Deviazione standard totale:", np.std(dati))
