"""
ESERCIZIO 1
* Crea un grafico lmplot che mostri la regressione lineare tra due variabili numeriche, regolando 
intervallo di confidenza e dimensione dei punti

ESERCIZIO 2
* Estendere il grafico introducendo una variabile categorica con hue, confrontando più gruppi

ESERCIZIO 3
* Utilizzare col e row per generare una griglia di regressioni e interpretare le differenze
tra i sottogruppi

ESERCIZIO 4
* Sperimentare una visualizzazione 3D di regressione multivariata coninua usando Matplotlib, scegliendo
colori e angolazioni appropriati

"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_theme(style="whitegrid")
df = sns.load_dataset("tips")
print(df.head())
#movimenti_per_total_bil=(df.groupby("total_bill").count().sort_values("total_bill"))

max_val=int(np.ceil(df["total_bill"].max() / 10) * 10)
bins=list(range(0,max_val+10,10)) #10,20,30,ecc
df["fascia_bill"]=pd.cut(df["total_bill"],bins=bins,right=True,include_lowest=True)
movimenti_per_fascia=df.groupby("fascia_bill").size()
print(movimenti_per_fascia)

"""
ESERCIZIO 1
* Crea un grafico implot che mostri la regressione lineare tra due variabili numeriche, regolando 
intervallo di confidenza e dimensione dei punti
"""

sns.lmplot(data=df,x="total_bill",y="tip",height=5,aspect=1.2,ci=95,scatter_kws={"s":40,"alpha":0.6},line_kws={"color":"red","linewidth":2})
plt.title("Relazione lineare total_bill/tip")
plt.xlabel("Totale bill")
plt.ylabel("Tip")
plt.show()
#ci=intervallo di confidenza del 75% attorno alla linea di regressione. Quanto siamo sicuri della stima ottenuta

"""
ESERCIZIO 2
* Estendere il grafico introducendo una variabile categorica con hue, confrontando più gruppi
"""
sns.lmplot(data=df,x="total_bill",y="tip",hue="sex",height=5,aspect=1.2,ci=95,scatter_kws={"s":40,"alpha":0.6})
plt.title("Relazione lineare total_bill/tip")
plt.xlabel("Totale bill")
plt.ylabel("Tip")
plt.show()
#ci=intervallo di confidenza del 95% attorno alla linea di regressione. Quanto siamo sicuri della stima ottenuta

"""
ESERCIZIO 3
* Utilizzare col e row per generare una griglia di regressioni e interpretare le differenze
tra i sottogruppi
"""

sns.lmplot(data=df,x="total_bill",y="tip",hue="sex",col="time",row="smoker",height=4)
plt.title("Regressione per mancia")
plt.xlabel("Total bill")
plt.ylabel("Tip")
plt.show()

"""
ESERCIZIO 4
* Sperimentare una visualizzazione 3D di regressione multivariata coninua usando Matplotlib, scegliendo
colori e angolazioni appropriati
"""

from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import numpy as np

# Variabili indipendenti: total_bill e size
X = df[['total_bill','size']].values
y = df['tip'].values

# Modello lineare 3D
model = LinearRegression()
model.fit(X, y)

# Creazione griglia per superficie
x_surf, y_surf = np.meshgrid(
    np.linspace(X[:,0].min(), X[:,0].max(), 20),
    np.linspace(X[:,1].min(), X[:,1].max(), 20)
)
z_surf = model.predict(np.c_[x_surf.ravel(), y_surf.ravel()]).reshape(x_surf.shape)

# Plot 3D
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y, c='blue', s=40, alpha=0.6, label='Dati reali')
ax.plot_surface(x_surf, y_surf, z_surf, color='orange', alpha=0.5)
ax.set_xlabel("Total Bill")
ax.set_ylabel("Size")
ax.set_zlabel("Tip")
ax.view_init(elev=25, azim=135)  # angolazione per migliore visualizzazione
plt.title("Regressione lineare multivariata 3D: tip ~ total_bill + size")
plt.show()

