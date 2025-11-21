
#verifica se un numero è multiplo di 3
n=9
if n%3==0:
    print("multiplo di 3")
else:
    print("non multiplo di 3")

#verifica se il voto è sufficiente
voto=int(input("Inserisci il voto: "))
if voto>18:
    print("sufficiente")
else:
    print("insufficiente")

#if con stringhe: controlla se un carattere è una vocale o consonante
c="a"
if c in ("aeiou"):
    print("vocale")
else:
    print("consonante")

#verifica se numero positivo/negativo/zero
n=0
if n>0:
    print("positivo")
elif n<0:
    print("negativo")
else:
    print("zero")

#verifica il maggiore di 3 numeri
a,b,c=7,13,9
if a>=b and a>=c:
    print("a maggiore")
elif b>c and b>a:
    print("b maggiore")
else:
    print("c maggiore")

# calcola il prezzo del biglietto
eta=70
if eta<12:
    prezzo=5
elif eta<65:
    prezzo=10
else:
    prezzo=8
print(prezzo)

#classificazione triangolo
a,b,c=5,5,3
if a==b==c:
    print("triangolo equilatero")
elif a==b or b==c or a==c:
    print("triangolo isoscele")
else:
    print("triangolo scaleno")