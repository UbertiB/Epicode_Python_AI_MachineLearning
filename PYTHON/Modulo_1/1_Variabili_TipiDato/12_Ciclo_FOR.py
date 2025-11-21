
"""
quando so quante volte ripetere una cosa
utilizzato per iterare una sequenza di dati
in ogni iterazione python prende l'elemnto successivo ed aggiorna la variabile
non mi devo preoccupare di aggiornare la condizone
for elemento in sequenza:
    operazioni
l'iterazione di diversi tipi
- liste: for frutto in ["mela","banana","pera"]
- stringhe: ogni carattere singolarmente for c in "ciao":
- dizionari: itera sulle chiavi o con .items() su coppie chiave-valore
- sequenze di numeri: con funzione range for numero in range(11)
supporta break (interrompe subito il ciclo)
continue (passas all'iterazione successiva)
else eseguito se il ciclo termina normalmente (senza break)
funzioni utili con ciclo for
-enumerate(): aggiunge un indice ad ogni elemento
 for i,val in enumerate(["a","b","c"])
    print(i,val)
-zip() combina due sequenze in parallelo
 for nome eta in zip(["A","B"],[21,22])
    print("{nome} {eta}")
Possibili cicli annidati
"""
# scrivi un programma che ha una lista di nomi e stampa ogni nome preceduto dal numero di ordine

for i,val in enumerate (["Anna","Ettore","Marco","Ginevra"]):
    print (f"{i}) {val}.")
