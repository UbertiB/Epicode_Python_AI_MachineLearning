"""
ESERCIZI FINALI per mettere in pratica tutte le tecniche apprese


"""
import pandas as pd
import numpy as np

file_prodotti_json="10_prodotti.json"
prodotti=pd.DataFrame({
    "ProdottoID":np.arange(1,11),
    "Categoria": np.random.choice(["A","B","C"],10),
    "PrezzoUnitario":np.random.rand(10)*100,
})
prodotti.to_json(file_prodotti_json,orient="records")

file_clienti_csv="10_clienti_csv"
clienti=pd.DataFrame({
    "ClienteID":np.arange(1,21),
    "Nome": ["Cliente_"+str(i) for i in range(1,21)],
    "Segmento": np.random.choice(["Premium","Standard"])
})
clienti.to_csv(file_clienti_csv,index=False)

file_ordini_csv="10_ordini.csv"
ordini=pd.DataFrame({
    "OrdineID":np.arange(1,51),
    "ClienteID": np.random.randint(1,21,50),
    "ProdottoID":np.random.randint(1,11,50),
    "Quantita":np.random.randint(1,5,50)
})
ordini.to_csv(file_ordini_csv,index=False)

#Prendo i dati da diverse fonrti
df_prodotti=pd.read_json(file_prodotti_json)
df_clienti=pd.read_csv(file_clienti_csv)
df_ordini=pd.read_csv(file_ordini_csv)

#merge di tutto
df=df_ordini.merge(df_prodotti,on="ProdottoID",how="left").merge(df_clienti,on="ClienteID", how="left")

df["Categoria"]=df["Categoria"].astype("category")
df["Segmento"]=df["Segmento"].astype("category")
df["Quantita"]=df["Quantita"].astype("int16")

df["ValoreTotale"]=(df["PrezzoUnitario"]*df["Quantita"]).astype("float32")

subset=df.query("Segmento=='Premium' and ValoreTotale>50").copy()

#imposto l'indice sullo stesso df (inplace=true), le colonne messe come chiavi vengono spostate dalle colonne e messe in righe
#questo tramite drop=True, se si vuole evitare (ma si avrebbe un doppione di dati) di deve fare con drop=False
df.set_index(["Categoria","ClienteID"],inplace=True,drop=True)

#imposto il report
"""
report=df.groupby(level=["Categoria","ClienteID"]).agg(
    totale_vendite=pd.NamedAgg(column="ValoreTotale",aggfunc="sum"),
    media_quantita=pd.NamedAgg(column="Quantita",aggfunc="mean"),
    numero_ordini=pd.NamedAgg(column="OrdineID",aggfunc="count")
)
"""
report = df.groupby(["Categoria", "ClienteID"]).agg(
    totale_vendite=("ValoreTotale", "sum"),
    media_quantita=("Quantita", "mean"),
    numero_ordini=("OrdineID", "count"),
)
report=report.reset_index

#divido gli ordini tra i mesi, prendendo degli esempi (.sample) dal df originale
ordini_gennaio=df.sample(10,random_state=1).reset_index()
ordini_febbraio=df.sample(8,random_state=2).reset_index()
ordini_marzo=df.sample(12,random_state=3).reset_index()


ordini_totali=pd.concat([ordini_gennaio, ordini_febbraio, ordini_marzo],ignore_index=True)
ordini_totali=ordini_totali.merge(df_clienti, on="ClienteID",how="left")
metriche=ordini_totali.groupby(["ClienteID"]).agg(
    spesa_totale=("ValoreTotale","sum"),
    ordini_totali=("OrdineID","count")
)
print(metriche)
 
#leggiamo in ordine di chunk per datasetgrandi
totale_valore=0
for chunk in pd.read_csv(file_ordini_csv,chunksize=10):
    chunk=chunk.merge(df_prodotti,on="ProdottoID",how=("left"))
    chunk=chunk.merge(df_clienti,on="ClienteID",how="left")
    chunk["ValoreTotale"]= chunk["Quantita"] * chunk["PrezzoUnitario"]
    totale_valore+=chunk["ValoreTotale"].sum()
print(totale_valore)


