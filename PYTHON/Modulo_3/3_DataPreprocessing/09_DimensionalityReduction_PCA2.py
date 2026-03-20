"""
DATA PREPROCESSING
DIMENSIONALITY REDUCTION CON PCA2 (PRINCIPAL COMPONENT ANALYSIS)

La PCA è un ottimo strumento per applicare la dimensionality reduction.
Per comprendere la PCA, è necessario conoscere come si misurano:    
    - la varianza: che rappresenta la dispersione tra i dati
    - la covarianza: che rappresenta la relazione che esiste tra i dati
L'obiettivo finale è capire come l'algebra lineare ci permette di trovare una direzione di 
massima informazione e capire i passaggi concreti per calcolare i Componenti Principali.

La VARIANZA è la misura statistica di quanto i dati sono dispersi lungo un singolo asse;
quantificando lo 'SPREAD' (quanto i dati sono sparpagliati rispetto alla loro media).
Calcolare la varianza è il primo passo per capire la dispersione delle singole feature.
Matematicamente, la varianza è definita come il quadrato della deviazione standard.

La COVARIANZA misura la correlazione e la direzione del movimento tra due variabili x e y:
    - Una covarianza negativa (Cov<0) indica che si muovono in direzioni opposte.
    - Una covarianza zero (Cov=0) suggerisce che le due variabili sono indipendenti.
    - Una covarianza positiva (Cov>0) indica che le variabili si muovono nella stessa direzione.
La sua formula confronta lo scostamento di ogni punto dalla media x,y

La matrice di Covarianza (S) contiene tutti i valori di covarianza tra ogni coppia 
possibile di dimensioni.
Per un set di dati con n attributi, la matrice è di covarianza risulta di dimensione nXn
Sulla diagonale principale, la matrice contiene la varianza ciascuno attributo con se stesso.

Questa matrice è cruciale perchè codifica l'informazione sulla ridondanza e sulla dispersione 
totale dei dati.

La PCA sfrutta la relazione tra Autovalori e Autovettori della matrice di covarianza.
Un vettore è un ente algebrico con 3 caratteristiche:
1) modulo (grandezza), l'informazione che porta
2) direzione (la retta su cui giace), quando è grande quanto è lungo
3) verso (di percorrenza della retta)
L'autovettore u di una matrice A, è un vettore che, quando moltiplicato per A, non cambia direzione
L'autovettore è il fattore scalare per cui l'autovettore viene moltiplicato
Risolvere l'equazione (a-autovettore)*u=0

La PCA sfrutta la relazione tra Autovalori e Autovettori della matrice di coverianza
Un vettore ("una freccia") sfrutta la relazione tra Autovalori e Autovettori della matrice
di covarianza.
Un vettore ("una freccia") è un ente algebrico che ha tre caratteristiche:
    1) modulo (grandezza)
    2) direzione (la retta su cui giace)
    3) Un autovettore u di una matrice A e un vettore che, quando moltiplicato per A, 
    non cambia direzione.

Un autovettore di una matrice A è un vettore che quando moltiplicato per A, non cambia direzione.
L'autovettore è il fattore scalare di cui l'autovettore viene moltiplicato.
Risolvere l'equiazione permette di trovare questi elementi.

Gli autovettore della matrice di covarianza S diventano i nuovi assi della base trasformata,
cioè i Componenti Principali (PC)
Questi nuovi assi sono vettori ortogonali
Il cambiamento di base, garantisce che le nuove variabili X siano completamente scorrelate tra
loro.
Due vettori (u e v) di dimensioni (n*1) si dicono ortogonali, se e solo se u(t)v=0
u(t) X v = 0

"""