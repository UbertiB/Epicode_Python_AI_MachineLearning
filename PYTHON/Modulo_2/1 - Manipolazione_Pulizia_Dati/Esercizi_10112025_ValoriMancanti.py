"""
gestione mancanti
"""

import pandas as pd
import numpy as np

df=pd.DataFrame({"Col1":[1,2,np.nan,4],
                 "Col2":[5,np.nan,5,5],
                 "Col3":[np.nan,9,10,11]
                })

df["Col1"].fillna(df["Col1"].median(),inplace=True)
df["Col2"].fillna(df["Col2"].mode()[0],inplace=True)
df["Col3"].fillna(0,inplace=True)

print (df)