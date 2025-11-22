
"""
i set sono degli insiemi
è una collezione di elementi senza duplicati e senza ordine
è un contenitore di elementi, se provi ad aggiungere due volte lo stesso elemento lo stesso compare una sola volat

"""

#creazione set con {}
s={"sdfdfs","fsdfsdf","fgsdf","fgsdf"} #il duplicato viene rimosso nei set (rimane solo una versione)
print(s)
#se scrivo solo s{} non creo un set vuoto ma un dizionario
s_d={}
print(type(s_d))
#per creare un set vuoto utilizzare la parola set
s_s=set({})
print(type(s_s))

#trasformare una lista in un set per eliminare duplicati
giorni_lista=["lunedi","martedi","lunedi","mercoledi","giovedi","venerdi","venerdi"]
giorni_set=set(giorni_lista)
print (type(giorni_set))
print (giorni_set)

#ricerca iterare con costurtto in
for s in giorni_set:
    print(s)

#verificare presenza valore
print("lunedi" in giorni_set) #true esiste il dato, false non esiste all'interno del set

#aggiungere un solo elemento .add
giorni_set.add("domenica")
#aggiungere più elementi (per esempio da una lista o da un altro set)
giorni_set.update(["gennaio","febbraio","lunedi"]) #duplicati ignorati
#attenzione alle parentesi, se non le metto aggiunte le singole lettere delle parole indicate
#perchè .update aggiunge elementi iterabili, pertanto l'iterabile di "gennaio" è "g","e","n","a", ecc
#se invece metto gli elementi da aggiungere tra parentesi [] gli iterabili sono gli elemnti inclusi
print(giorni_set)

#rimuovere elementi se l'elemento non esiste non da errore
giorni_set.discard("gennaio")
#rimuovere elementi se l'elemento non esiste da errore
giorni_set.remove("febbraio")
print(giorni_set)

#unione di set
s1={1,2,3,6}
s2={4,5,6}
print(type(s1), type(s2))
print(s1.union(s2))
print(s1.intersection(s2)) #solo elementi comuni oppure &
print(s1&s2)
print(s1.difference(s2)) #elementi di s1 che non stanno in s2 oppure -
print(s1-s2) #elementi di s1 che non stanno in s2

#verifica di appartenenza
s={"mela","arancia"}
print("mela" in s)
print("pera" in s)

#utilizzo set e non vista se non ho bisogno di mantenere ordine e se 
#devo eliminare duplicati






