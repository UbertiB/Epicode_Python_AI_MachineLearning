
# ho degli studenti iscritti ai corsi

a={"Anna","Luca","Luca","Marco"}
b={"Luca","Sara","Marco"}

print(f"set a intersezione b: {a&b}")
print(f"solo a e non b: {a-b}")
print(f"Totali unici: {len(a|b)}")

#genera set di numeri casuali
import random
numeri=(random.randint(1,20) for _ in range(10))
print({numeri})

#conta le occorrenze di parole
frase="ciao come stai ciao tutto bene"
parole=frase.split()
conteggio={}
for p in parole:
    conteggio[p]=conteggio.get(p,0)+1
print(f"conteggio: {conteggio}")

#inverti i valori
d={"a":1,"b":2,"c":3}
inverso={v:k for k,v in d.items()}
print(f"inverso: {inverso}")

#crea un dizionario da due liste
chiavi={"nome","eta","citta"}
valori={"Anna",25,"Roma"}
d=dict(zip(chiavi,valori))
print(d)

#raggruppa le parole per lunghezza
parole={"ciao","come","va","oggi","tutto","benissimo"}
gruppi={}
for p in parole:
    gruppi.setdefault(len(p),[]).append(p)
print(gruppi)

#calcola con quanta frequenza sono ripetutte le lettere
testo="programmazione"
frequenza={}
for c in testo:
    frequenza[c]=frequenza.get(c,0)+1
print(frequenza)