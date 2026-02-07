"""
JOINTPLOT
Il joinplot è un grafico '2 in 1': al centro mostra la relazioe tra due variabili 
(grafico bivariato) e ai margini mostra le distribuzioni separate delle due variabili 
(univariato). In pratica: scatter al centro e istrogrammi o KDE ai lati, nello stesso oggetto.
Utile quando vuoi capire se due metriche si muovono insieme e contemporaneamente come 
sono distribuite singolarmente.

Nota: hue su scatter, se hai troppi punti diventa confuso. In questo caso passa a
king='kde' 

"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(7)
n = 400

df = pd.DataFrame({
    "leadtime_giorni": np.random.normal(12, 4, n).clip(1, None),
    "rotazione": np.random.normal(5, 1.2, n)
})

# relazione plausibile: lead time più alto -> rotazione un po' più bassa
df["rotazione"] = df["rotazione"] - 0.08 * df["leadtime_giorni"] + np.random.normal(0, 0.6, n)

#ESEMPIO 1: SCATTER + ISTOGRAMMA
sns.jointplot(data=df, x="leadtime_giorni", y="rotazione", height=6)
plt.tight_layout()
plt.show()


#ESEMPIO 2: SCATTER + RETTA (KIND='REG')

sns.jointplot(data=df, x="leadtime_giorni", y="rotazione", kind="reg", height=6,joint_kws={"scatter_kws": {"alpha": 0.4}})
plt.show()

#ESEMPIO 3, DENSITà: KDE Utile quando hai molte righe e lo scatter diventa 'nebbia'

sns.jointplot(data=df, x="leadtime_giorni", y="rotazione",kind="kde", height=6)
plt.show()

#ESERCIZIO 4: Tanti punti HEX binning (kind='hex')
#spesso si hanno decine o centinaia di righe. Lo scatter mente per sovrapposizione. 
#Hex è un 2D istrogramma: il colore rappresenta quante osservazioni cadono in quella 'cella esagonale'
big = pd.concat([df]*40, ignore_index=True)  # simula molti record

sns.jointplot(data=big, x="leadtime_giorni", y="rotazione", kind="hex", height=6,joint_kws={"gridsize": 35})
# parametro di hexbin
plt.show()

#ESEMPIO 5: HUE per classe, se vuoi vedere se la relazione cambia per categoria
df2 = df.copy()
df2["classe_ABC"] = np.random.choice(["A", "B", "C"], size=len(df2), p=[0.2, 0.3, 0.5])

sns.jointplot(data=df2, x="leadtime_giorni", y="rotazione",hue="classe_ABC", height=6)
plt.show()

#ESEMPIO 6: controllo qualità del dato: dropna, limiti, margini custom
df3 = df2.copy()
df3.loc[np.random.choice(df3.index, 15, replace=False), "rotazione"] = np.nan

sns.jointplot(data=df3, x="leadtime_giorni", y="rotazione",hue="classe_ABC",dropna=True,
    xlim=(0, 30), ylim=(-2, 8),marginal_kws={"common_norm": False},height=6
)
plt.show()

#ESEMPIO 7: JoingGrid per massimo controllo
#Quando jointplot non basta, usi JointGrid e decidi tu cosa mettere 
#al centro e sui margini (anche funzioni diverse con parametri diversi).
g = sns.JointGrid(data=df2, x="leadtime_giorni", y="rotazione", hue="classe_ABC", height=6)

g.plot_joint(sns.scatterplot, alpha=0.35)
g.plot_marginals(sns.histplot, kde=True)

g.refline(x=12, y=df2["rotazione"].median())  # soglia esempio: leadtime target e mediana rotazione
plt.show()

#ESEMPIO 8: collegare al ML
#Uso pratico: predetto vs reale e residui. Se stai facendo forecasting o regressione (es. previsione 
#rotazione o domanda), un jointplot ti fa vedere bias, outlier e varianza che cresce.

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

X = df2[["leadtime_giorni"]]
y = df2["rotazione"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=7)

m = RandomForestRegressor(random_state=7)
m.fit(Xtr, ytr)
pred = m.predict(Xte)

eval_df = pd.DataFrame({"reale": yte.values, "predetto": pred})
sns.jointplot(data=eval_df, x="reale", y="predetto", kind="hex", height=6)
plt.show()

eval_df["residuo"] = eval_df["reale"] - eval_df["predetto"]
sns.jointplot(data=eval_df, x="predetto", y="residuo", kind="scatter", height=6)
plt.show()

if False:
    np.random.seed(0)
    df=pd.DataFrame({
        "altezza": np.random.normal(170,10,200),
        "peso":np.random.normal(65,15,200),
        "sesso": np.random.choice(["M","F"],200),
        "gruppo":np.random.choice(["A","B"],200)
    })
    sns.jointplot(data=df,x="altezza",y="peso",hue="sesso",kind="kde",fill=True,alpha=0.5)
    plt.show()
    #il kde 2d può essere pesante su df molto grande, se hai tanti punti utilizza kingscatter 
    #oppure sampling

    #camparision plot  con violino, boxplot e stripplot
    #l'ordine dei grafici è importante
    plt.figsize=(8,5)
    sns.violinplot(data=df,x="sesso",y="peso",inner=None,palette="Pastel1")
    sns.boxenplot(data=df,x="sesso",y="peso",width=0.2,palette="Set2") #width=0.2 rende scatola stretta per non nascondere il violino
    #striplot per vedere i punti reali
    sns.stripplot(data=df,x="sesso",y="peso",hue="gruppo",dodge=True,size=4,alpha=0.7)
    plt.title("Comparision plot combinato")
    plt.show()


    g=sns.FacetGrid(df,col="gruppo",height=4)
    g.map_dataframe(sns.scatterplot,data=df,x="altezza",y="peso",hue="sesso",alpha=0.7)
    g.map_dataframe(sns.kdeplot,data=df,x="altezza",y="peso",level=4,color="r",alpha=0.3)
    g.add_legend()
    plt.show()