"""
una volta che i dati sono nel dataframe, dobbiamo capirli, esplorarli e 
scegliere solo le parti che ci interessano.
Per capire cosa abbiamo caricato:
df.head(): mostra le prime 5 righe
df.head(10): mostra le prime 10 righe
df.tail(): mostra le ultime righe
Questi sono il punto di partenza per farsi un idea del dataset, ancora prima di iniziare un'analisi più completa

"""
import pandas as pd


data={"Nome":["Luca","Anna","Mario"],
      "Eta":[20,35,45], 
      "Corso":["Fisica","Informatica","Economia"]}
df=pd.DataFrame(data)
print(df.head(1))
print(df.tail(1))
print(df.info()) #per capire la struttura, numero colonne, righe, e tipi di dati
print(df.describe()) #calcola statistiche base sulle colonne numeriche (media, deviazione standard, min, max, quartili)
print(df["Nome"]) #per estrarre una colonna specifica dal dataframe
print(df.loc[:, ["Nome"]]) #per estrarre una colonna specifica dal dataframe
print(df.loc[:, ["Nome", "Corso"]]) #per estrarre due o più colonne dal dataframe
print(df.loc[0]) #per selezionare la riga con indice 0 (la prima) nome di indici o delle righe
print(df.iloc[0]) #lavora con le posizioni numeriche delle righe indipendentemente dai nomi
print(df.iloc[0:2,1:3]) #selezione mista di righe e colonne righe 0 e 1 colonne 1 e 2
print(df[df["Eta"]>25])
print(df[df["Eta"]>25 & (df["Corso"]=="Informatica")])
print(df["Eta"].isin([35,45]))