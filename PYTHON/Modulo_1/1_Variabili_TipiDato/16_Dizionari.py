
"""
coppia di chiave e valore
si dichiare con le {}
chiavi uniche e immutabili, valori di qualsiasi tipo
"""
#creazione
dict1={"Nome":"Mario","Eta":20, "Citta":"Crema"}
#dict
#dati=dict("nome"="luca", citta="milano", eta=20)
dict_vuoto={}
#aggiungere elementi
dict1["studi"]="elementari" #se studi non c'è aggiunge altrimenti modifica
dict1["Nome"]="Carlo"

#accedere al valore
print(dict1["Nome"])
#modificare
dict1["Nome"]="Maria"
#rimuovere elementi
del(dict1["studi"])
print(f"rimosso ",dict1.pop("Eta"))
#eliminare tutto
dict1.clear()

print(dict1)

#se esiste con operatore in
dict2={"Nome":"Anna","Eta":25}
if "Nome" in dict2:
    print("chiave trovata")

#iterare solo le chiavi
for k in dict2:
    print (k)
#iterare coppie chiavi e valori
for k,v in dict2.items():
    print(k,v)
#iterare solo i valori
for v in dict2.values():
    print (v)


#utilizziamo i dizionari quando devo avere coppia chiave/valore
#è raccomandato per iterazione complesse

#recuperare il valore di una chiave GET
print (f"funzione get: {dict2.get("Nome","non esiste")}")
print (f"funzione get: {dict2.get("Nome1","non esiste")}")
#UPDATE per aggiornare se coppia di chiave e valori esiste già nel primo dizionario
d1={"Nome":"Marco","Eta":60}
d2={"Nome":"Maria","Eta":30}
d1.update(d2)
print(d1)
#UPDATE per aggiungere un dizionario ad un altro, se la coppia chiave/valore del secondo dizionario non è già presente nel primo dizionario
d1={"Nome":"Marco","Eta":60}
d2={"Studia":"Metematica","Media":30}
d1.update(d2)
print(d1)
#creare una copia
d1={"Nome":"Marco","Eta":60}
d2=d1.copy()
print(d2)
