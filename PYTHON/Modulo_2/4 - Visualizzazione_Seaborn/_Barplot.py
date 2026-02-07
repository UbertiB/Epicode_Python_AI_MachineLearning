"""
Il BARPLOT (grafico a barre) è il tipo di grafico di base quando si trattano variabili catagoriche:
a ogni categoria si associa un valore, che può dipendere da un'altra variabile (bar plot classico), 
oppure dal numero di osservazioni che appartengono a tale categoria
E' possibile utilizzera il barplot anche per una variabile continua tramite fasce di valori
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Creiamo un dataset di esempio
df = sns.load_dataset("tips")

#
# BARPLOT variabile indipendente (categoriale), dipendente (numerica)
#
df_sex=df.groupby(["sex"])[["tip"]].sum()
print(df_sex.head())
sns.barplot(data=df_sex, x="sex",y="tip")
plt.xlabel("Mancie")
plt.ylabel("Valori")
plt.title("BARPLOT: var. categoriale + var. numerica")
plt.tight_layout()
plt.show()

#
# BARPLOT variabile indipendente (categoriale), dipendente numerica (a fasce di valori)
#
df_mancie=df.