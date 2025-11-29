import numpy as np

# Tipi di dati in NumPy
print("**************************")
print("TIPI DI DATI IN NUMPY")
print("**************************")
a = np.array([1, 2, 3], dtype=np.int32)  # array di interi a 32 bit
print(f"Array: {a}, Tipo di dato: {a.dtype}")
b = np.array([1.0, 2.0, 3.0], dtype=np.float64)  # array di float a 64 bit
print(f"Array: {b}, Tipo di dato: {b.dtype}")
c = np.array([1, 2, 3], dtype=np.complex128)  # array di numeri complessi
print(f"Array: {c}, Tipo di dato: {c.dtype}")
d = np.array([True, False, True], dtype=np.bool_)  # array di booleani
print(f"Array: {d}, Tipo di dato: {d.dtype}")
e = np.array(['a', 'b', 'c'], dtype=np.str_)  # array di stringhe
print(f"Array: {e}, Tipo di dato: {e.dtype}")
f = np.array([1, 2, 3], dtype=np.uint8)  # array di interi senza segno a 8 bit
print(f"Array: {f}, Tipo di dato: {f.dtype}")
# Conversione tra tipi di dati
print("**************************")
print("CONVERSIONE TRA TIPI DI DATI")
print("**************************")
#astype converte il tipo di dato di un array
g = a.astype(np.float64)  # converti array di interi a float
print(f"Array originale: {a}, Tipo di dato: {a.dtype}")
print(f"Array convertito: {g}, Tipo di dato: {g.dtype}")
h = b.astype(np.int32)  # converti array di float a interi      
print(f"Array originale: {b}, Tipo di dato: {b.dtype}")
print(f"Array convertito: {h}, Tipo di dato: {h.dtype}")
