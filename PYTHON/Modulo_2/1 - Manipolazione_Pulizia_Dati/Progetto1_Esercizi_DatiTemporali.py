import pandas as pd
import numpy as np

data={"timestamp":["2023-10-01 10:00:00","2023-10-01 11:00:00","2023-10-01 12:00:00"],
      "user_id":[1,2,1],
      "amount":[10.0,5.0,7.5]}
df=pd.DataFrame(data)

#
#pulizia e sistemazione 
#
#timestamp
df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True)
df["timestamp_local"]=df["timestamp"].dt.tz_convert("Europe/Rome").dt.round("min")
#ottimizzazione tipi di dato
df["amount"]=pd.to_numeric(df["amount"],downcast="float")
df["user_id"]=df["user_id"].astype("category")
#impostazione indice temporale
df = df.set_index("timestamp_local")
df = df.sort_index()

series=df.resample("min").agg({"amount":"sum","user_id":"count"}).fillna(0)
series["sum_24h"]=series["amount"].rolling(24*60,min_periods=1).sum()
series["avg_7d"]=series["user_id"].rolling(7*24*60,min_periods=1).sum()

print(series)

#print("DataFrame Pulito e Indicizzato:\n",df)



