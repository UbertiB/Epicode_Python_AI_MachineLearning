"""
i nomi non possono iniziare con un numero.
x=4 assegnamo il valore 4 alla variabile x
x=7 cambiamo valore
la variabile è come  un'etichetta se cambio valore l'etichetta rimane identica
Il nome deve iniziare con lettera o con _ 
no spazi nel nome, non può iniziare con numero
non si possono usare parole riservate
Python è case-sensitive quindi x <> X

Python assegna automaticamente il tipo in base al valore assegnato

le varibili sono oggetti e le variabili sono etichette
che si riferiscono ad un determinato oggetto
il tipo si può capire con type

lo scope delle varibili:
local scope: sono valide nei blocchi di codice (indentazione)
inizio/fine blocco la variabile è disponibile, al di fuori no
global scope: dichiarate all'esterno di una funzione e restano in vita per tutto il programma principale
è possibile accedere in qualsiasi parte del programma

"""

#
# ASSEGNAZIONI
#

nome="Anna" #str 
n=20 #int
x=3.52 #float  utilizzare il punto per il separatore decimale
m=True #boolean vero/falso

print(type(nome))

#
#CONVERSIONI
#
x="123" #stringa
y=int(x) #x convertita in numero da x

print(type(x))
print(type(y))

#
# input da tastiera
#
nome=input("Come ti chiami? ")
print(nome)

anni=input("Quanti anni hai? ")
print(f"tra 5 anni avrai {int(anni)+5}.")



