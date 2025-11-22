
"""
sono un tipo di sequenza (come liste e stringhe) ma sono immutabili.
non possono essere modificate una volta create, non posso modificare elementi, aggiungerne nuovi e cancellare elementi
Utilizzati per valori fissi (esempio coordinate geografiche)
"""

#creazione tupla
giorni=("lunedi","martedi","mercoledi", "giovedi","venerdi","sabato","domenica")
print (type(giorni))

#accesso ai dati
print(giorni[0]) #primo elemento
print(giorni[-1]) #ultimo elemento
print(giorni[len(giorni)-1]) #ultimo elemento

# quante volte compare un valore
print(giorni.count("lunedi"))

#posizione del valore
print(giorni.index("lunedi"))

#slicing
print(giorni[:2])

#se cerco di modificare ho errore
#giorni[0]="domanice"

"""
la rigidità non è un difetto, perchè garantisce che il dato è integro (una volta inserito)
inoltre sono molto veloci (appunto perchè non sono mutabili)
"""

#creazione tupla con un solo elemnto
x=(5,) #è  una tupla
y=(5) #non è un a tupla è un intero

#iterare le tuple
#in controlla se esiste elemento
for g in giorni:
    print(g)

#lunghezza, conta le occorrenze
len(giorni)

#annidamento tuple
dati1=("Mario",25)
dati2=("Anna",20)
dati=dati1+dati2
print(type(dati1))
print(type(dati2))
print(dati)
print(type(dati))

#lista e tuple, la prima creata con [] la seconda con (), si accede nello stesso modo
#lista
numeri=[0,1,2]
print(type(numeri))
print(numeri[0])
#tupla
t_numeri=(0,1,2)
print(type(t_numeri))
print(t_numeri[0])

"""
differenza con le liste è che le liste sono mutabili, ma più lente
le tuple possono essere utilizzate come chiavi dei dizionari (appunto perchè immutabili)
"""


