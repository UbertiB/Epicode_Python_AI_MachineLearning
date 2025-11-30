import pandas as pd
import numpy as np

"""
ESERCIZIO 1:    Crea un dataframe con due colonne: lunghezza e larghezza. 
                Aggiungi una nuova colonna che calcoli l'area di un rettangolo.
"""
dati1={"Lunghezza":[10,11,15,23,18,11,12],
      "Larghezza": [20,22,24,20,21,20,25]}
df1=pd.DataFrame(dati1)
df1["Area"]=df1["Lunghezza"]*df1["Larghezza"]
print(df1)
"""
ESERCIZIO 2:    Genera un datafram con una colonna categoriale "Tipo" (es. A B C) e una colonna numerica "Valore". 
                Applica one-hot encoding alla colonna "tipo"
"""
dati2={"Tipo":["A","B","C","D","E"],
      "Valore":[10,11,10,15,18]}
df2=pd.DataFrame(dati2)
df_encoded=pd.get_dummies(df2,columns=["Tipo"])

print(df_encoded)
"""
ESERCIZIO 3:    Crea un dataframe con date giornaliere e valori numerici casuali. 
                Estrai le feature: giorno della settimana, mese e differenza rispetto al giorno prima
"""
dati3={"Data":["15/10/2025","16/09/1975","25/11/2015"],
      "Valori":np.random.randint(1,100,3)}
df3=pd.DataFrame(dati3)
df3["Data_modificata"]=pd.to_datetime(df3["Data"],dayfirst=True)
df3["Giorno_della_settimana"]=df3["Data_modificata"].dt.day_name()
df3["Mese"]=df3["Data_modificata"].dt.month_name()   
df3["Diff_giorno_precedente"]=df3["Valori"].diff().fillna(0)
print(df3)
