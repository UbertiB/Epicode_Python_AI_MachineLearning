
"""
i numeri si dividono tra interi e decimali
su questi posso fare operazioni matematiche
+=addizione
-=sottrazione
*=moltiplicazione
/:divisione (con risultato sempre float)
//: divisione intera (prende solo la parte intera scartando decimali)
%:modulo, resto delle divisione n%2 se è 0 il numero è pari, altrimenti dispari
**:potenza
"""

a=7
b=2
print(a+b)
print(a-b)
print(a*b)
print(a/b)
print(a//b)
print(a%b)
print(a**b)

"""
operatori unari
+x=restituisce lo stesso numero x
-x=restituisce il valore x con segno invertito
"""

"""
oltre agli operatori, se voglamo operazione più avanzate
doppiamo utilizzare la libreria math
"""
import math

x=7.3
print(math.floor(x)) #arrotondamento per difetto
print(math.ceil(x)) #arrotondamento per eccesso
print(math.trunc(x)) #tronca la parte decimale (senza arrondare)
print(math.fabs(x)) #valore assoluto, toglie il meno se presente

y=-4.7
print(math.floor(y))
print(math.ceil(y))
print(math.trunc(y))
print(math.fabs(y))

