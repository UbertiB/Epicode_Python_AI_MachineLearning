
"""
boolean contiene solo due valori 0=false e 1=vero
posso trasformare altri tipi di dati in boolean con funzione bol
0, vuoto, liste vuote=false
tutto il resto (1 ed altro diverso a 0)=true
operatori che restituiscono un boolean
== uguale
!= diverso
<
>
<=
>=
oltre a confronti ho operatori logici:
not a (inverte valore a)
a and b (la condizione vera se entrambi veri)
a or b (almeno uno vero)
not funziona al contrario 
"""

a=5
b=3
print(a>0 and b>a)
print(not a==b)

"""
short circuit evaluation
evita calcoli inutili: in a and b se a è falso python non guarda b restituisce subito false
utile per migliora le prestazioni
is (controlla se due variabili puntano allo stesso elemente e in restituiscono valori booleni 
"""

#verifica se un numero è positivo
n=5
print(f"il numero {n} è positivo: {n>0}")

#verifica se due stringhe sono uguali
s1="parola"
s2="Parola"
print(f" la parola {s1} è uguale a {s2}: {s1==s2}")

#controlla con and per vedere se due numeri sono entrambi positivi
a=5
b=10
print(f"{a>0 and b>0}")

#scriti un programma che chiede la sua eta
#il programma deve stampare true se eta >=18

eta=int(input("quanti anni hai? "))
if eta>=18:
    print("maggirenne")
else:
    print("minorenne")