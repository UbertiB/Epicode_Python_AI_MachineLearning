import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data={"Prezzo":[100,200,300,400,500],
      "Sconto":[0.1,0.15,0.2,0.25,0.3]}
df=pd.DataFrame(data)

df["Prezzo"]=df["Prezzo"].astype(int)
df["Sconto"]=df["Sconto"].astype(float)
df["Prezzo_scontato"]=df["Prezzo"]*df["Sconto"]
df["Tipo_prezzo"]=["Alto" if x>250 else "Basso" for x in df["Prezzo"]]
df["Categoria"]=np.where(df["Prezzo"]>250,"Costoso","Economico")
df["Tipo_sconto"]=["Alto" if x>20 else "Basso" for x in df["Sconto"]*100]
df.eval ("Prezzo_finale = Prezzo - Prezzo_scontato", inplace=True)
df.query ("Prezzo_finale > 200", inplace=True)
print(df)
