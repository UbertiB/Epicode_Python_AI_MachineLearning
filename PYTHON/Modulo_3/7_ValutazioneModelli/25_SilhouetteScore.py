"""
SILHOUETTE SCORE

E' una metrica riservata ai problemi di clustering
Il Silhouette Score è una metrica utilizzata per valutare la qualità dei cluster ottenuti da algoritmi di 
clustering.
Esprime quanto ogni punto è simile al proprio cluster rispetto agli altri cluster.
La metrica prende in considerazione sia la COESIONE INTERNA del cluster sia la SEPARAZIONE dai cluster vicini.
Un valore alto indica punti ben raggruppati nel prorpio cluster e bene separati dagli altri.
Questo indice è particolarmente utile quando non esistono etichette predefinite per valutare il clustering.

Il Silhouette Score di un punto si calcola come rapporto tra la distanza media dal proprio cluster e la 
distanza media dal cluster più vicino.
Il risultato varia tra -1 e 1:
    * valori vicini a -1 indicano possibili errori di assegnazione
    * valori vicini a 0 indicano che i cluster sono sovrapposti
    * valori vicini a +1 indicano punti ben raggruppati.
La media dei valori di tutti i punti fornisce lo score complessivo del clustering

Una Silohuette score elevato (vicni a 1) indica cluster compatti e bene separati, segnale di buon clustering
Score vicini a zero suggerisce che alcuni punti si trovano tra cluster diversi, indicando confusione
nel modello.
Valori negativi mostrano punti assegnati al cluster sbagliato rispetto alla loro posizione naturale.
L'indice permette di confrontare diversi algoritmi o diverse configurazioni del clustering.
E' uno strumento utile anche per determinare il numero ottimale di cluster.

A differenza di altri indici come Rand Index o Adjusted Rand Index, il Silhouette Score non richiede etichette.
Misura invece la qualità intrinseca del clustering basandosi solo basandosi sulle distanze tra i punti.
Rand Index valuta concordanza con una classificazione nota, mentre Silhouette score valuta la compattezza
dei cluster stessi.
In pratica, è molto utile in scenari di clustering non supervisionato puro.
La combinazione di più metriche può fornire una valutazione più completa.

Il Silhouette Score può essere rappresentato tramite diagrammi a barre o grafici 2D o 3D dei punti colorati
per ogni cluster.
Le barre orizzontali mostrano i valori di silhouette per ogni punto, aiutando a indivisuare punti mal 
assegnati.
Si può evidenziare il valore medio con una linea verticale per capire la  qualità complessiva del custering.
Questi grafici aiutano a comunicare risultati anche a chi non conosce il dettaglio matematico.
La visualizzazione è spesso utile durante la fase di scelta del numero ottimale di cluster.

Il Silhouette Score è utile per ottimizzare il numero di cluster nel K-Means, DBSCAN o altri algoritmi.
Permette di confrontare configurazioni diverse senza avere etichette di riferimento.
Aiuta a identificare cluster 'sbagliati' o punti che potrebbero essere outlier.
Può essere combinato con altre metriche di valutazione interna per migliorare l'analisi dell'interpretazione.
Viene spesso usati in settori come marketing, biologia, analisi di immagini.

In Python, il Silhouette Score si calcola facilmente con sklearn.metrics.silhouette_score
Serve passare due oggetti come parametri: l'array dei dati e le etichette assegnate dal clustering.
Si può specificare il metodo di distanza (metric="euclidean" di default)
E' possibile calcolare anche il Silhouette Score per ogni singolo punto usando silhouette_samples.
L'uso corretto della funzione consente di integrare facilmente il calcolo in pipeline di clustering.

"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.metrics import silhouette_score

data=load_digits()
X=data.data
y=data.target

df=pd.DataFrame(X,columns=data.feature_names)
df["target"]=y
#print(df)
#1800 righe per 65 colonne
#target 10 classe diverse numerate da 0 a 9 

K=10
kmeans=KMeans(n_clusters=K, random_state=42)
y_pred=kmeans.fit_predict(X)

silhouette=silhouette_score(X,y_pred)
print(f"Silhouette score:\t{silhouette:.3f}")

#silhouette di 0.176 indica che i punti non sono bene separati tra loro

"""
Vantaggi
Il Silhouette Score permette di valutare il clustering senza conoscere le etichette reali.
Combina informazioni di coesione e separazione in un singolo indice interpretabile.
Può esser eusato per confrontare algoritmi diversi o parametri differenti, come il numero di cluster K
Aiuta a identificare punti 'problematici' o fuori cluster
E' facilmente calcolabile anche su dataset di dimensioni moderate.
Svantaggi
Non è sempre affidabile su dastaset con cluster di forma molto complessa o non convessi.
Può essere influenzato da outlier e punti isolati.
Il calcolo della distanza media può diventare costoso per dataset molto grandi.
Non indica direttamente quale algoritmo è migliore, serve come indicatore generale di qualità
In casi di cluster di dimensioni molto diverse, può penalizzare quelli piccoli

Il Silhouette Score è uno strumento potente per valutare cluster senza etichette.
Permette di diagnosticare cluster troppo compatti, cluster non separati o punti anomali.
Non sostituisce la valutazione soggettiva o visuale dei cluster, ma la integra.
Può essere combinato con altre metriche interne o esterne per ottenere un giudizio  e un
quadro completo.
L'indice fornisce un criterio quantitativo chiaro durante il tuning del clustering 

"""
