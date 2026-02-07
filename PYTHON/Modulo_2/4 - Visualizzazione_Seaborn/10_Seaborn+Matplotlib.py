"""
SEABORN + MATPLOTLIB
Integrazione tra Seaborn e Matplotlib
Regola generale Seaborn disegna, Matplotlib rifinisce
Seaborn da di defaul grafici ben fatti con funzioni ad alto livello. Matplotlib da il controllo finale (assi,
annotazioni, inset, doppio asse, layout complessi, gestione figure, salvataggio preciso)

Costruzione di plot ibrid combinando seaborn e matplotlib
Seaborn fornisce grafici statistici pronti all'uso e belle palette di colori
mentre matplotlib consente massimo controllo sugli elementi grafici e personalizzabili.
Spesso si vuole aggiungere al grafico Seaborn elementi extra come linee di riferimento, annotazioni, 
superifici di contorno, oppure combinari più tipi di grafico in una unica figura.

Seaborn si basa su mtplotlib ma la maggior parte delle sue funzioni produce automaticamente figure (fig) ed 
assi (as) questo rende facile iniziare ma limita la personalizzazione.
Integrando mtplotlib possiamo aggiungere layer, modificate titoli, assi, etichette, colori e linee di riferimento.
Permette anche di combianre più grafici in una unica figura.
Grazie a questa flessiblità possiamo adattare la visualizzazione a qualsiasi tipo di analisi

Il punto chiave per creare grafiic ibridi è il parametro AS ogni funzione Seaborn accetta un oggetto as di 
matoplotlib con cui disegnare il grafico, in questo modo possimao costruire la figura passo dopo passo 
aggiungendo layer, annotazioni o grafici multipli sullo stesso asse.

Un uso comune è sovrappopre un istogramma dei dati con una curva kde per evidenziare distribuzione.
Matplotlib può essere utilizzato per modificare colori, trasparenza, e bin dell'istogramma, mentre Seaborn 
aggiunge kde con un controllo dettagliato di bentwidh fil ed alpha.
Questa combinazione permette di confrontare distribuzioni empiriche e stime di densità in un unico grafico
rendendo visibili assimetrie, picchi e code

Nei dataset categoriali i violiplot sintetizzano la distribuzione di ogni gruppo, mentri punti singoli 
sovrapposti tramite swarmplot mostrano la densità reale. 
Usando AX possiamo disegnare entrambi sullo stesso asse, regolando trasparende e larghezza del violinplot
Questo approccio consente di integrare sintesi statistica e dettaglio puntuale utile per analisi esplorative
avanzate o per confronti tra più gruppi in un unica visualizzazione chiara.

E' possibile arrichire una heatmap di seaborn con linee di contorno provenienti da matplotlib ad esempio
per evidenziare regioni di maggiore densità o soglie critiche dove i contorni su una mappa di calore, ci permette
di combinare informazioni continuee e discrete, facilitando interpretazione di pattern complessi nei dati.

Utile in analisi multivariate scientifiche.

Seaborn offre jointgrid e parigrid per controllare le componenti di joinplot e pairplot, utilizzando as 
possiamo aggiungere layer extra a ciascun subplot, esempio scatterplot con linee di regressione, kde bidimensionali
annotazioni numeriche o punti evidenziati.

Per serie temporali è possibile combinare lineplot di seaborn con bande di incertezza con intervalli personalizzati
con matplotlib, esempio possiamo aggiungere aree colorate che rappresentano deviazioni standard, intervalli
di confidenza o soglie critiche, sovraponendo linee multiple ed annotazioni temporali.
Utile per visualizzare trend, variazioni ed anomalie nella rappresentazione temporale.


"""

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

#
# Esempio 1
#
sns.set_theme(style="whitegrid")

# Esempio finto: margine % per mese
mesi = np.arange(1, 13)
margine = np.array([0.18,0.22,0.20,0.19,0.25,0.23,0.21,0.17,0.16,0.20,0.24,0.26])

fig, ax = plt.subplots(figsize=(9,4))
sns.lineplot(x=mesi, y=margine, marker="o", ax=ax)

# Matplotlib: rifinitura “da report”
ax.axhline(0.20, linestyle="--")              # soglia target
ax.set(title="Margine % mensile", xlabel="Mese", ylabel="Margine")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0)) #formattatore per le tacche di y
ax.set_xticks(mesi)
plt.tight_layout()
plt.show()

np.random.seed(0)
data=np.random.normal(0,1,500) #500 campioni con media 0 e deviazione standard 1)
fig,ax=plt.subplots(figsize=(7,5))
#disegno istrogramma
ax.hist(data,bins=25,color="skyblue",alpha=0.6,edgecolor="k")
#sovrappongo la stima della densità kde (mostra la distribuzione)
sns.kdeplot(data,ax=ax,color="red",fill=True,alpha=0.3)
#titolo
ax.set_title("Overlay Istogramma + KDE")
plt.show()


df=pd.DataFrame({
    "gruppo":np.repeat(["A","B","C"],20),
    "valore":np.random.randn(60)+np.repeat([0,1,2],20) #aggiungo rumore
})
print(df)
fig,ax=plt.subplots(figsize=(7,5))
sns.violinplot(data=df,x="gruppo",y="valore",ax=ax,inner=None, color="lightgreen")
sns.swarmplot(data=df,x="gruppo",y="valore",ax=ax,color="darkgreen",size=5)
ax.set_title("Violn plot + swarmplot")
plt.show()


data = np.random.rand(10,10)
fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(data, ax=ax, cmap="YlGnBu", cbar=True)
contour = ax.contour(data, colors="red", linewidths=1, alpha=0.7)
ax.set_title("Heatmap con Contour Overlay")
plt.show()


df=pd.DataFrame({
    "gruppo":np.repeat(["A","B","C"],20),
    "valore":np.random.randn(60)+np.repeat([0,1,2],20) #aggiungo rumore
})
g=sns.JointGrid(data=df,x="gruppo",y="valore",height=5)
g.plot_joint(sns.scatterplot,color="blue",alpha=0.7)
g.plot_marginals(sns.histplot,kde=True,color="lightblue")
plt.suptitle("JoinGrid Ibrido")
plt.show()
