
"""
chiedi all'utente di scrivere un numero positivo
continua a chiedere finchè l'utente non inserisce un numero positivo
Quando il numero è positivo stampalo e termina
"""

i=False
while i==False:
    n=int(input("Scrivi un numero positivo (0 per uscire): "))
    if n>0:
        i=True
    if n==0:
        break
else:
    print(f"Hai digirato un numero positivo ({n}).")