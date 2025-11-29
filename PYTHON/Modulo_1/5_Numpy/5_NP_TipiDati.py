import numpy as np

"""
i tipi di dati è un aspetto importante, il tipo di dato
influisce su quanta memoria consumiamo
su quanto sono veloci le operazione
e che precisione otteniamo nei calcoli
dtype = data type
è un attributo di np che ci dice di che natura sono i suoi elementi
(ogni elementi di np ha lo stesso tipo)
tipi di dati numerici:
- interi (integer) int8, int16, int32, int64
- floating-point (virgola mobile): float16, float32, float64
- complessi (complex): numeri con parte reale e parte immaginaria complex64, complex128
Più grande è il numero maggiore è la precisione, o il range,
ma anche la memoria occupata e minore la velocità nel gestire il numero
altri tipi di dato:
- boolean: solo True e False
- object: molte meno efficiente
- stringhe (str, unicode) per dati testuali, anche se np è pensato
per lavorare con i numeri
Se non si specifica il tipo di dato np cerca di indovinarlo
Il tipo di dato si può cambiare anche dopo aver creato l'array con il metodo .astype()
Attenzione astype crea un nuovo array, non modifica l'originale, quindi la conversione è costosa
in termini di tempo e memoria (con array molto grandi)
Il tipo di dato è importante per:
- precisione
- memoria
- velocità
- compatibilità
"""
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
