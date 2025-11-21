"""
stringhe sequenza di caratteri
non è un blocco unico ma una sequenza fatta di elementi più piccoli
indice 0=prima lettera, ecc
-1=ultimo
questo si chiama indexing
oltre a prendere singoli caratteri posso estrasrre singole lettere con la sintassi [1:4] yth(della parola python), questo è detto slicing
possono essere scritte con "" o con '', su più righe con tripli apici
/n va a capo /t per tabulazione // per barra inveversa
posso fare concatenazione (unire più righe), ripetizione (moltiplico la stringa per n volte), esempio parola+5
len mi restituisce la lunghezza
indicizzazione (slicing)
queste operazioni ci permettono di trattare il testo come fosse una struttura matematica.
La formattazione è importante, per inserire dei valore all'interno di una frase posso_
1)f string
2)format metodo compatibile con le versione + vecchie
3)formattazione con la % ma è datata, ora si usano le f string
upper(), lower(), capitalize()
strip(), rstrip(), lstrip()
replace(old, new)
utili per la pulizia dei dati
altri metodi:
split(seP9 per dividere una stringa in singole parole
join(iterable)
startswith() per capire se una stringa inzia con un testo
endswith() se termina con un determinato testo
"""
testo="Python è fantastico" 
print(testo.strip)
print(testo.upper)
print(testo.replace("P","p"))

#indicizzazione e slicing
print(testo[::2]) #prendo in considerazione il testo con un passo di 2
print(testo[::-1]) #inverto la stringa

#index error (se accedo ad un indice che non esiste)
#le stringhe sono immutabili
x="ciao"
print(x)
x="barbara"
print(x)



