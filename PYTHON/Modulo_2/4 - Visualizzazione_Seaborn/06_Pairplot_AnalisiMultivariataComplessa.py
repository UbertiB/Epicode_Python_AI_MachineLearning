"""
PAIRPLOT e analisi multivariata complessa

Quando si analizzano dataset con molte variabili, può diventare difficile capire rapidamente
come esse siano correlate tra di loro, in questi casi entra in gioco il pairplot di Seaborn, 
consentendo di visualizzare in una unica matrice le relazioni tra tutte le variabili numeriche, 
mostrando le distribuzioni individuali che le correlazioni bivariate.
Permette di identificare pattern, correlazioni lineari o no, oulier e cluster.

Un pairplot è una mappa esplorativa delle relazioni bivariate tra tutte le variabili numeriche di un df,
più la distribuzione di ciascuna variabile sulla diagonale.
Risponde alla domanda: 'Tra quali coppie di variabili vale la pena approfondire?', non serve a stimare
serve ad orientare

Per ogni coppia (X,Y) mostra:
- uno scatter: forma delle relazione
- una diagonale: distribuzione (istogramma o kde)
Con hue:
- confronti immediati tra gruppi
- separazioni, sovrapposizioni, pattern diversi

Paiplot crea automaticamente una griglia di grafici che mette in relazione ogni coppia di variabili 
numeriche di un df, sulle diagonali mostra le distribuzioni univariate (istogrammi o kdeplot),
mentre nelle cella mostra scatterplot per le relazioni tra due variabili. 
Il funzionamento è estremamente semplice, basta passare il dataset e Seaborn genera l'intera matrice.
Tuttavia il pairplot è anche altamente personalizzabile, possiamo modificare i tipi di grafici
sulla diagonale, impostare la palette di colore, filtrare colonne specifiche, 
aggiungere una variabile categoriale (hue), è anche possibile impostare dimensioni, trasparenza, 
marker ed altri parametri grafici, per rendere la visualizzazione più leggibile e coerente 
con lo stile dell'analisi. 
Consente di ottenere con un solo comando una panoramica completa delle correlazioni interne
di un dataset.

L'interpretazione di un pairplot è un passo fondamentale.
Per trarre conclusioni significative, ogni cella rappresenta la relazione tra due variabili
Se i punti formeranno paterne lineari, è probabile che esista una correlazione (positiva
o negativa) se invece sono dispersi senza un pattern, la relazione potrebbe essere debole o assente.
Le diagonali mostrano la distrinuzione delle singole variabili, come le forme simmestriche
indicano distribuzioni normali, mentre delle code lunghe o picchi accentuati possono individuare
gli outlier, queste informazioni ci aiutano a decidere se applicare trasformazioni, normalizzazioni
i trattamenti sui dati prima di ulteriori analisi

Con hue è possibile vedere come i punti si distribuiscono in base a categorie differenti 
rendendo immediata l'identificazione di gruppi o seperazioni naturali tra le classi,
suggerendo relazioni significative tra variabili numeriche e categoriali.
Uno dei principali vantaggi del pairplot è la capacità di mostrare tutte le correlazioni
in un unica figura, in un dataset con molte variabile consente di individusare rapidamente 
quali sono le coppie fortemente correlate e quali no, senza dover calcolare manualmente la matrice
di correlazione.
Attraverso la disposizione a griglia è possibile confrontare decine di relazioni
contemporaneamente. 
Quando alcune relazioni appaiono forti, possono essere approfondite in seguito
con grafici di regressione o analisi statistiche dettagliate. L'uso del parametro corner true 
riduce la ridondanza mostrando solo metà matrice, mentre kaind kde permette di visualizzare
la densità di distribuzione anziche istogrammi, rendendo il grafico più elegante e più
informativo. 
Infine l'integrazione con hue consente di confrontare come diverse classi si comportano
in piu variabili contemporaneamente, una funzione cruciale per l'analisi multivariata
e la selezione di feature rilevanti.

Il pairplot è estremamente utile anche per analizzare cluster o gruppi nei dati, aggiungendo
una colonna categoriale (hue) seaborn colora i punti in base ai gruppi, rendendo
immediatamente visibili separazione, sovrapposizioni o intersezioni tra le classi.

In un contesto clusering non supervisionato (kvins o dbscan) è possibile aggiungere 
al dataset una colonna con le etichette del cluster generati ed usare il pariplot 
per visualizzare la loro disposizione nello spazio delle feature, questo aiuta a comprendere 
se i cluster trovati sono coerenti, distinti o parzialmente sovrapposti.

Allo stesso modo, nel caso di analisi supervisionate, il pairplot consente
di osservare la separabilità delle classi, elemento chiave nella scelta
della variabili più predittive

La visualizzazione dei gruppi facilita sia l'interpretazione che la validazione
dei modelli di ml.

Quando il numero di variabili è molto elevato
il parplot diventa difficile da leggere, in questi casi è utile applicare
una riduzione dimensionale (come pca) o (tisne) per sintetizzare le informazioni
principali in due o tre componenti. 
Dopo aver ridotto le dimesnioni del dataset possiamo usare il paiplot per i nuovi componenti 
principale ed osservare come le variabili sintetizzate spiegano la variabilità totale dei dati.
Questo approcio aiuta ad individuare patern non globali ed a individuare strutture latenti nei dati
Combinare pca con pairplot è una tecnica comune nell analisi esplorativa
multivariata perchè unisce la potenza della riduzione dimensionale con 
la chiarezza visiva delle relazioni tra le componenti, ottentendo grafici compatti, interpretativi
ed altamente informativi

L'interpretazione di un paiplot è un passo fondamentale per trarre conclusioni significative.
Ogni cella rappresenterà la relazione tra due variabili:
- se i punti formeranno pattern lineari è probabile che esiste una relazione positiva o negativa
- se sono dispersi la relazione potrebbe essere debole o assente
le diagonali mostra la distrbuzione delle singole variabili

COME SI LEGGONO I DATI:
1) Relazioni evidenti
    * nuvole inclinate: possibile relazione
    * nuvole tonde: quasi sempre nessuna relazione
    * curve: non linearità
2) Ridondanza
    * due variabili quasi allineate: dicono la stessa cosa
    * in un modello una delle due è probabilmente inutile
3) Outlier
    * punti isolati che compaiono in più pannelli
    * candidati a influenzare qualsiasi regressione
4) Distribuzioni
    * asimmetrie forti
    * code lunghe
    * variabili 'a gradini' (discrete mascherate da continue)
5) Separazione per hue
    * gruppi ben separati: variabile discriminante
    * gruppi sovrapposti: informazione debole

"""

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=sns.load_dataset("iris") #contiene delle colonne come lunghezza del sepalo, larghezza del sepalo, lunghezza del petalo, larghezza del petalo, e speicie del fiore
print(df.head())

#
#PAIRPLOT BASE
#

sns.pairplot(df) #crea una griglia discatterplot ed istogrammi che dimostrano tutte le correlazioni possibile tra le variabili numeriche del df
plt.suptitle("Pairplot base (dataset iris)",y=1.02)
plt.show()

#le celle fuori diagonale sono gli scatterplot
#le celle diagonali mostrano le distribuzioni univariate, per default sono istrogrammi
#serve ad individuare le correlazioni tra le variabili, esempio petal lenth cresce insieme a patal widht
#Ci per mette di capire pattern generali dei dati prima di fare ml

#
#PAIRPLOT CON HUE E DIAG_KING=KDE
#

sns.pairplot(df,hue="species",diag_kind="kde", palette="Set2") #diag_kind="kde" sostituisce istrogrammi diagonali con curve di densita
plt.suptitle("Pairplot con distinzione per specie (hue)",y=1.02)
plt.show()
#risultato: il tipo di fiore è importante per la dimensione del petalo

#
#ANALISI DELLE SOLE VARIABILI 'INTERESSANTI' rilevate con il pairplot
#

#dopo aver capito che le variabili petal* hanno maggior valore rispetto a quelle sepal* continuo 
#con l'analisi delle sole variabili petal* esempio:
sns.lmplot(data=df, x="petal_length", y="petal_width", hue="species")
plt.title("LMPLOT variabili petal")
plt.show()

#
#RIDUZIONE DIMENSIONALE DEI DATI (con PCA)
#

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#PCA accetta solo variabili numeriche continue, 
#usa algebra pura per calcolare varianza, covarianza, autovettori
#La PCA serve a scoprire strutture latenti nei dati non a usare etichette già note.
#'species' è una variabile target, una spiegazione esterna, qualcosa che vuoi verificare dopo, non usare prima
#Pertanto le variabili categoriche non vanno passate a pca (utilizzo .drop per eliminare 'species')
#ed eliminate prima, per poi re-includere nelle analisi successive

#partiamo da 4 variabili numeriche e faremo generare x nuove variabili chiamate pca1, pca2, pcax,
#che sono le componenti principali che fanno davvero la differenza.
#per capire quale x utilizzare procedere nel seguente modo:
#1) Selezionare solo le variabili numeriche
#2) Standarizzare la variabilità delle variabili
#3) PCA iniziale per decidere quanti componenti tenere
#4) PCA finale con numero dei componenti scelti al punto 3
#5) Dataframe PCA
#6) Pairplot su componenti principali (calcolati da pca)

#1) Seleziono solo le variabili numeriche con .drop elimino le categoriche
X = df.drop("species", axis=1) 
#2) Standarizzazione (in modo da rendere le variabili confrontabili tra loro)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
#3) PCA iniziale per decidere quante componenti tenere
pca = PCA()
pca.fit(X_scaled)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.cumsum())
#4) PCA finale con SOLO 2 componenti (decisione motivata dai due print precedenti)
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
#5) DataFrame PCA
df_pca = pd.DataFrame(components, columns=["PC1", "PC2"])
df_pca["species"] = df["species"]
#6) Pairplot sulle componenti principali
sns.pairplot(df_pca, hue="species", diag_kind="kde", palette="coolwarm")
plt.suptitle("Pairplot sulle componenti principali (PC1, PC2)", y=1.02)
plt.show()

#Per visualizzare da cosa sono composti PC1 e PC2 procedere nel seguente modo:
loadings = pd.DataFrame(
    pca.components_,
    columns=X.columns,
    index=["PC1", "PC2"]
)
print("LOADINGS")
print(loadings.round(3))

# contributo percentuale
contrib = loadings**2
contrib = contrib.div(contrib.sum(axis=1), axis=0) * 100
print("\nCONTRIBUTI (%)")
print(contrib.round(1))


