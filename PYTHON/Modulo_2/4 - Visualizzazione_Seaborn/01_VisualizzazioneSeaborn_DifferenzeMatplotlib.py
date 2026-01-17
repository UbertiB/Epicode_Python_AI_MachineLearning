"""
Capacità di visualizzare correttamente i dati è importante quanto l'analisi dei dati
Seaborn estende le funzionalità di Matplotlib, libreria più evoluta e potente.
Seaborn costruita sopra Matplotlib, integrato con Pandas
Seaborn è una libreria per la visualizzazione dei dati basata su Matplotlib, progettata per semplificare
la creazione di grafici statistici, chiari, eleganti ed informativi.
Mentre matplotlib fornisce un controllo totale e di basso livello sulla costruzione dei grafici,
Seaborn agisce come livello di astrazione più alto, automatizzando grand parte del lavoro. Uno dei punti
di forza è la sua capacità di lavorare direttamente con i df di Pandas, questo significa che è possibile
generare complessi passando semplicemente i nomi delle colonne senza dover manipolare manualmente
array o coordinate, inoltre Seaborn gestisce automaticamente la leganda, le scale, i colori e le etichette.
A differenza di Matplotlib che richiede spesso decine di righe di codice (per impostare figure, assi, colori ed 
annotazioni), Seaborn offre funzioni di alto livello come Barplot, boxplot, i ipmap, che uniscono semplicità
e potenza analitica. Seaborn nasce per analisi esplorativa e statistica riducendo la necessità di interventi
manuali.
Sebbene Seaborn nasce su Matplotlib le differenze tra le due sono sostanziali. Matplotlib è una libreriua
di basso livello, ideale per costruire grafici da zero e personalizzazrli in ogni dettaglio, perfetta
per chi deve creare visualizzazioni personalizzate
Seaborn invece pensato per l'analisi dei dati statitici, automatizzando molti aspetti delle gestione
del grafico (palette colori, gestione valori mancanti, disposizione degli assi), dispone di funzioni
integrate per la rappresentazioni di relazioni, distribuzioni e categorie.
Seaborn applica automaticamente temi estetici moderni e coerenti, mentre matplotlib bisogna impostarli 
manualmente, in pratica Seaborn offre un approccio più di alto livello, mentre matplotlib rimane lo 
strumento più flessibile per chi vuole un controllo completo.
Seaborn non si limita a rendere 'più belli' i graifici, intriduce struementi avanzati per analizzare
le relazioni tra variabili e per sintetizzare grandi quantità di informazioni in modo leggibile.
una delle sua funzioni più potenti è rei plot, che consente di creare grafici relazionali complessi 
(scatterplot, lineplot) collegati automaticamente a variabili del dataset.
Tra le funzioni più apprezzate c'è payplot che genera una griglia di grafici a coppie per mostrare tutte 
le relazioni numeriche di un dataset.
Ci consente di verificare pattern o relazioni visivamente.
Le palette di colori di seaborno sono studiate per migliorare l'intepretazione visiva.
Si integra perfettamente con numpy, pandas, e matplotlib, permettendo di integrare le sua abilità statistiche
con la potenza delle altre librerie
Le funzioni di regressione (come implot) e distribuzine (come joinplot) semplificano l'analisi di
correlazioni e tendenze nei dati. In pochi comandi è possibile ottenere grafici che con matplotlib
richiederebbero numerosi passaggi manuali
Capire quando utilizzare Seaborn e Matplotlib, seaborn è la scelta ideale durante la fase esplorativa
dell'analisi, è perfetto per dataset strutturati in un df, per analizzare correlazioni distribuzioni, categorie
e relaìzini, la sua estetica curata a la facilità d'uso lo rendono ideale per comunicazioni rapide
dei risultati.
Matplotlib rimene indispensabile per chi necessità di un controllo completo e personalizzato sulla
figura.
Seaborn per analisi rapida
Matplotlib per la rifinitura e l'elaborazione finale.

"""

import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


df=sns.load_dataset("tips") #seaborn offre dataset di esempio già pronti 

#TIPS contiene dati su mancie lasciate in un ristorante italiano

#HUE crea due regressioni separate per maschi e femmine con colori diversi

#scatterplot con regressione lineare (lmplot)
sns.lmplot(data=df, x="total_bill", y="tip",height=6, aspect=1.2)
plt.title("Tip vs Total bill (baseline)")
plt.title("Relazione tra conto totale e mancia")
plt.show()
#verifica la non linearità
sns.lmplot(data=df, x="total_bill", y="tip",lowess=True,scatter_kws={"alpha":0.35, "s":35}, height=5, aspect=1.2)
plt.title("LOWESS: controlla se la relazione è curva")
plt.show()
#nello stesso grafico metti tutto sia lowness che la retta
fig, ax = plt.subplots(figsize=(6,4))
sns.scatterplot(data=df, x="total_bill", y="tip", alpha=0.35, ax=ax)
sns.regplot(data=df, x="total_bill", y="tip", scatter=False, ax=ax, label="Lineare")
sns.regplot(data=df, x="total_bill", y="tip", lowess=True, scatter=False, ax=ax, label="LOWESS")
ax.legend()
plt.show()
#Paradosso di Simopon (variabili covarianti) hue
sns.lmplot(x="total_bill",y="tip",hue="sex",data=df, height=6,aspect=1.2)
plt.title("Relazione tra conto totale e mancia con regressione per sesso")
plt.show()

#
# MATRICE DI CORRELAZIONE
#

#heatmap di correlazione (riepilogo visivo delle correlazioni numeriche)
#corr=df.corr(numeric_only=True)
num = df.select_dtypes(include="number")
corr = num.corr()
sns.heatmap(corr,annot=True, cmap="coolwarm",center=0) #riepilogo visivo delle variabili numeriche e loro correlazioni
plt.title("Matrice di correlazione delle variabili numeriche (METODO PERARSON)")
plt.show()

corr1 = num.corr(method="spearman")
sns.heatmap(corr1,annot=True, cmap="coolwarm",center=0) #riepilogo visivo delle variabili numeriche e loro correlazioni
plt.title("Matrice di correlazione delle variabili numeriche (METODO SPEARMAN)")
plt.show()
#visualizza la differenza tra Pearson e Spearman
corr_p = df.corr(numeric_only=True, method="pearson")
corr_s = df.corr(numeric_only=True, method="spearman")
corr_diff = (corr_p - corr_s).abs()
diff_max = corr_diff.where(np.triu(np.ones(corr_diff.shape), 1).astype(bool)).max().max()
print(diff_max)  #restituisce una differenza molto bassa

