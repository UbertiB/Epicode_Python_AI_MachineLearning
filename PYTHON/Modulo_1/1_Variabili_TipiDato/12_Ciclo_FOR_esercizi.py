
#stampa numeri da 1 a 10
for i in range(1,11):
    print(i)

#stampa i numeri pari da 1 a 20
for i in range(2,21,2):
    print(i)

#oppure (più veloce precedente)
for i in range(1,21):
    if i%2==0:
        print(i)

#stampa ogni lettera di una parola
parola="parola"
for c in parola:
    print(c)

#effettua la somma dei numeri da 1 a 100
somma=0
for i in range(1,101):
    somma+=i
else:
    print(somma)

#stampa della tabellina del 3
tabellina=3
for i in range(1,11):
    print(f"{tabellina} x {i} = {i*tabellina}")

#calcola il fattoriale di un numero
n=5
fattoriale=1
for i in range(1,n+1):
    fattoriale*=i
print (fattoriale)

#conta quante vocali ci sono in una parola
parola="programmazione"
vocali="aeiou"
conta=0
for c in parola:
    if c in vocali:
        conta+=1
print (f"le vocali sono {conta}")

#stampa una matrice 3x3
for i in range(1,4):
    for j in range(1,4):
        print(i,j, end=" ")
    print()

#stampa i numeri da i a 10 saltando 5
for i in range(1,11):
    if i==5:
        continue
    print(i)

#stampa i numeri da 1 a 10 fermandoti al 7
for i in range(1,11):
    if i==7:
        break
    print(i)

