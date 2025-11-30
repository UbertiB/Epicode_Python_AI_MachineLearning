"""
gli OUTLIER sono valori anomali che si discostano in maniere significati dal resto delle osservazioni
Errori di inserimento, errori di misurazione, inserimento manuale, condizioni eccezionali, 
fenomeni rari ma rilevanti
Importanti rilevarli perchè alcune statisthce sono influenzate dai valori estremi
Sono informazioni distribuite in modo anomalo, non seguono l'andamento generale della serie
Possono avere un impatto importante sulle statistiche
Importante rilevare gli outlier per gestirli
Esempio nel contesto delle vendite, può essere corretto che il sabato ho delle vendite
molto più alte rispetto agli altri giorni, questo non è un errore come potrebbe essere 
un errore di imputazione manuale

Non bisogna eliminare gli outlier in maniera automatica, un valore alto potrebbe essere
un errore, ma anche un valore reale
Poi è necessario documentare i metodo di rilevamento utilizzati, anche più di uno
sia metodo statistici sia con ml
Poi è buona cosa lavorare sempre con una copia dei dati originali.

"""
#
#Rilevare gli outlier
#uso della DEVIAZIONE STANRDARD, se un valore si discosta troppo dalla media, è segnalto come anomalia.
#

#uso dei METODI STATISTICI TRADIZIONALI, interquantile IQR
# è la differenza tra il terzo quartili ed il primo quartile
# i valori che cadono fuori da questo intervallo, sono consideratI POTENZIALMENTE outlier
#più sensbile alla 
#rispetto ai metodi statistiche richiedono maggiori risorse e maggior addestramento

#uso di metodi baseti sul MACHINE LEARNING progettati specificatamente per rilevare
#gli outlier analizzando i dati e come si combinano con gli altri dati

#MODELLI PREDITTIVI modello di regressione di una rete neurale. 
# Sono esempi isolation forest, dbscan

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

data={"Valori":[10,12,11,13,12,100,800]}
df=pd.DataFrame(data)


#
#METODO STATISTICI
#

#DEVIAZIONE STANDARD (sensibile alla distribuzione dei dati, meno adatta se dataset irregolare)
#Se un valore si discosta troppo dalla media, viene segnalato come anomalia

if True:
    media=df["Valori"].mean()  #media
    dev_std=df["Valori"].std()  #deviazione standard
    #evidenzio i possibili outlier con il metodo della deviazione standard
    df["Outlier"]=(abs(df["Valori"]-media)>2 *dev_std) # è un outlier se valore-media è maggiore  di d*deviazione standard (outlier=true)
    print(df)

#altro metodo per rilevare gli outlier
#INTERQUARTILE IQR
if True:
    data2={"Valori":[10,12,11,13,12,100,800]}
    df2=pd.DataFrame(data2)
    #Quantile 1
    Q1=df2["Valori"].quantile(0.25)
    #Quantile 3
    Q3=df2["Valori"].quantile(0.75)
    #IQR
    IQR=Q3-Q1
    #calcolo i limiti basso e alto
    limite_basso=Q1-1.5*IQR
    limite_alto=Q3+1.5*IQR
    print(f"limite basso: {limite_basso}, limite alto: {limite_alto}")

    df2["Outlier"]=(df2["Valori"]<limite_basso)|(df2["Valori"]>limite_alto)
    print(df2)

#terzo metodo per rilevare gli outlier con ml
#TECNICA CON MACHINELARNIG
#ISOLESCION FOREST

if True:
    data3={"Valori":[10,12,11,13,12,100,800]}
    df3= pd.DataFrame(data3)

    model=IsolationForest(contamination=0.2, random_state=42)
    df3["Outlier"]=model.fit_predict(df3[["Valori"]])

    print(df3)

# LOCAL OUTER FACTOR (LOF)

#MODELLIPREDITTIVI
#MODELLO REGRESSIONE RETE NEURALE (impara andamento tipico di un dastaset di vendite ed i valori che si discosano vengono segnalati cone outlier)

"""
utilizzate 3 tecniche per rilevare outlier, le prime due hanno rilevato gli stessi outlier
il metodo con il machine learnig ha rilvetao un valore come outlier che gli altri due metodi
statistici non avevano rilevato.
"""

