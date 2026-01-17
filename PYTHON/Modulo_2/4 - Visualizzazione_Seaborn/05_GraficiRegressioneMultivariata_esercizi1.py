"""
GRAFICO REGRESSIONE CON Seaborn
Un grafico a regressione in Seaborn è uno scatter con sopra una funzione stimata (lineare o non lineare)
e spesso una banda di incertezza.
Serve per vedere velocemente trend, outlier, non linearità e 'quanto ci puoi credere'

LMPLOT è uno strumento di esplorazione visiva guidata. Non server a 'fare il modello', serve a capire se
ha senso farlo.
Tecnicamente un lmplot è:
- scatter plot
- regressione (lineare di default)
- banda di confidenza
- segmantazione (hue)
- pannelli (row, col)
Tutto con una sola funzione
"""



#Setup minimo
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")
sns.set_theme(style="whitegrid")

#
#1) CASO BASE: RELAZIONE SEMPLICE
#
sns.lmplot(data=df,x="total_bill",y="tip",ci=95,height=5,aspect=1.2)
plt.title("LMPLOT semplice")
plt.show()

# Se la pendenza della regressione lineare è <> da 0 allora una relazione esiste.
# Se i punti sono molto dispersi allora la relazione è debole
# Se la banda è larga allora c'è molta incertezza
# Se la linea di regressione è aperta ad imbuto allora  la varianza non è costante
# Rispondo a questa domana: - Vale la pensa approfondire?

#
#2) SEGMENTAZIONE (CON hue): stessa X comportamenti diversi
#
sns.lmplot(data=df,x="total_bill",y="tip",hue="smoker",ci=95)
plt.title("LMPLOT semplice con segmentazione (hue)")
plt.show()

# Se le linee di regressione lineare sono diverse, allora X dipende dal gruppo
# Se le linee di regressione lineare sono parallele ma spostaste, allora c'è una differenza costante tra i gruppi
# Se una delle linee di regressione lineare è basata su pochi punti, allora ignorala

#
#3) CONFRONTO PULITO CON FACET (row, col)
#
sns.lmplot(data=df,x="total_bill",y="tip",col="time",row="sex",ci=95)
plt.title("LMPLOT con facet (row, col)")
plt.show()

# Qui abbiamo diversi grafici con lo stesso asse (per un confronto onesto).
# Se alcuni pannelli sono vuoti i dati sono insufficienti
# Se i diversi pannelli hanno trend diversi, allora processi diversi, non un unico modello

#
# 4) FORMA DELLA RELAZIONE: order
#
sns.lmplot(data=df,x="total_bill",y="tip",order=2,ci=95)
plt.title("LMPLOT forma della relazione (order)")
plt.show()

# ORDER serve a dirgli che tipo di curva deve adattare ai dati, è il grado del polinomio usato per regressione
# Esiste perchè molte relazioni non sono lineari: crescono, poi saturano, o hanno una curva. Se uni una
# retta quando la relazione è curva, la linea 'taglia' male i dati
# Capisci che ti serve aumentare order quando con order=2 (default) la retta sta 'in mezzo',  
# ma sbaglia nello stesso verso:
# - a sinistra sottostima
# - al centro OK
# - a destra sovrastima

#
# QUANTO TOGLIERE LA CI 
#
sns.lmplot(data=df,x="total_bill",y="tip",ci=None)
plt.title("LMPLOT senza ci")
plt.show()
# Togli la CI quando vuoi vedere solo il trend e non la banda che distrae


