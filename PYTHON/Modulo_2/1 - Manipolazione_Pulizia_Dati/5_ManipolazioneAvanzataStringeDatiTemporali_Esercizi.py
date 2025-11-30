import pandas as pd
import numpy as np
from datetime import date
"""
ESERCIZIO 1: crea una colonna di stringhe con nomi sporchi (spazi, maiuscole casuali). 
Pulisci rendendo tutti i nomi minuscoli e senza spazi extra
"""
data1={"Colonna":["  Anna bianchi", "ROSSI MONICA","Ernesto Ugo  "]}
df1=pd.DataFrame(data1)
df1["Colonna_pulita"]=df1["Colonna"].str.strip().str.lower()
print(df1)

"""
ESERCIZIO 2: Genera un dataframe con date di nascita in formato stringa. 
Convertile in datetime e calcola l'eta in anni di ogni individuo
"""
data2={"Data":["16/09/1975","01/01/1900","18/02/2000"]}
df2=pd.DataFrame(data2)
df2["Data_pulita"]=pd.to_datetime(df2["Data"], format="%d/%m/%Y", errors="coerce")
oggi = pd.Timestamp.today().normalize()
df2["Eta"] = round(((oggi - df2["Data_pulita"]).dt.days / 365.25),0).astype("Int32")
print(df2)
"""
ESERCIZIO 3: Crea un dataset giornaliero di valori numerici su due mesi. 
Usa .resample() per ottenere: media settimanale, massimo mensile, e somma cumulativa.
"""
data3={"Valore":np.random.randint(1,100,size=59),
       "Data":pd.date_range(start="2025-01-01", periods=59, freq="D")}
df3=pd.DataFrame(data3)
df3.set_index("Data",inplace=True)  #resample funziona solo con indice datetime
#media settimanale
df3_settimanale=df3.resample("W").mean()
#massimo mensile
df3_mensile=df3.resample("M").max()
#somma cumulativa
df3["Somma_cumulativa"]=df3["Valore"].cumsum()

print(f"Originale: {df3}")
print(f"\nMedia settimanale: {df3_settimanale}")
print(f"\nMassimo mensile: {df3_mensile}")
print(f"\nSomma cumulativa: {df3["Somma_cumulativa"]}")