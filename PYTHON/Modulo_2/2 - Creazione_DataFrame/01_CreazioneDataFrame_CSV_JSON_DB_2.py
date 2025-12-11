
import pandas as pd
import sqlite3
import json

data_sales=({"data":["2023-01-01","2023-01-02","2023-01-08","2023-02-05","2023-02-07"],
       "store_id":["S1","S2","S1","S3","S2"],
       "product":["P1","P2","P1","P3","P2"],
       "qty":[10,5,7,3,8],
       "price":[100.0,200.0,100.0,300.0,200.0]
       })
df_sales=pd.DataFrame(data_sales)

data_stores= ({"store_id":["S1","S2","S3"],
               "region":["Nord","Centro","Sud"],
               "city":["Milano","Roma","Napoli"]})
df_stores=pd.DataFrame(data_stores)

data_promotiones=({"store_id":["S1","S2","S3"],
                   "promo_flag":[1,0,1]})
df_promotions=pd.DataFrame(data_promotiones)

df_sales.to_csv("transactions.csv",index=False)
df_stores.to_json("stores.json",orient="records",lines=True,force_ascii=False)
conn=sqlite3.connect("retail.db")
df_promotions.to_sql("promotions",conn,if_exists="replace",index=False)
conn.close()

#LETTURA DEI FILE SALVATI
df_sales=pd.read_csv("transactions.csv",parse_dates=["data"],dtype={"store_id":"category","product":"category"})
df_stores=pd.read_json("stores.json",orient="records",lines=True)
conn=sqlite3.connect("retail.db")
df_promo=pd.read_sql_query("select store_id, promo_flag from promotions ",conn)

df=df_sales.merge(df_stores,on="store_id", how="left")
df=df.merge(df_promo, on="store_id", how="left")

df["promo_flag"]=df["promo_flag"].fillna(0).astype("int8")
df_group=df.groupby(["region"]).agg(total_qty=("qty","sum"), promo_sales=("qty",lambda x:x[df["promo_flag"]==1].sum()))
print(df_group)

