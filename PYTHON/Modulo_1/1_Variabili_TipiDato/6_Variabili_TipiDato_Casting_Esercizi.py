
#
# VARIABILI
#

nome="Barbara"
eta=50
citta="Crema"

print(f"Mi chiamo {nome} abito a {citta} ed ho {eta} anni.")

#
# assegna valore ad una variabile ed aggiorna il valore
#
x=5
print(f"valore {x}")
x=10
print(f"valore {x}")

#
#somma di due variabili
#
n1=6
n2=7
print(f"somma= {n1+n2}")

#
#scambio di valori
#
x=20
y=15
x,y=y,x
print(f"x ora vale: {x} mentre y vale: {y}")

#
#calcolo area rettangolo
#
base=5
altezza=10
print(f"area rettangolo: {base * altezza}")

#
#somma di un intero e un decimale
#
a=10
b=3.5
print(f"Somma: {a+b}")

#
#media di 3 numeri
#
x,y,z=10,40,30
print(f"Media: {(x+y+z)/3}")

#
#concatenazione di stringe
#
s1="mi piace "
s2="giocare a calcio" 
print(f"concatenate: {s1+s2}")

#
#ripetizione di 3 stringhe
#
parola="ciao"
print(f"{parola} * 3")

#
#usa boolean per verificare su un numero è maggiore
#
a=15
b=30
c=45
print(f"{a<b}")
print(f"{b>c}")
print(f"{a<10}")

#
#TRASFORMAZIONE NUMERI
#
X=10
Y=float(X)
print(Y)

#
#converti un numero in stringa
#
n=4650000
s=str(n)
print(f"il numero è {s}")