"""
Visualizzare dati discreti o categoriali richiede strumenti in grado di visualizzare il singolo punto
senza sovrapposizione eccessive.
Swarmplot e stripplot sono ideali per rappresentare distribuzioni di dati discrete, sono 
"scatter plot categoriali" costruiti sopra Matplotlib.
Richiedono una variabile categorica

plt.scatter: scatter generico (numerico-numerico) x,y
sns.stripplot: scatter con categorie + jitter
sns.swarmplot: scatter con categorie + 'impacchettamento' per non sovrapporre i punti
Con solo plt.scatter di Matplotlib puro, su x categorie devi arrangiarti (convertire categorie in numeri),
jitter a mano, legenda a mano). Con Seaborn (stripplot, swarmplot) la fai in una riga di codice.

Permettono di osservare densità dei punti, raggruppamenti ed outlier in modo chiaro
Lo Stripplot è utile per dataset piccoli o medi dove ogni punto ha un significato
mentro lo Swarmplot aggiunge la disposizione intelligente dei punti per evitare le sovrapposizioni

Lo STRIPPLOT è un grafico scatter monodimensionale che dispone i punti lungo un asse categoriale
mostra ogni singolo dato evidenziando valori replicati e variabilità all'interno delle categorie
E' possibile combinarlo con parametri come gitter per separare leggermente i punti sovrapposti e migliorare
leggibilità 
Adatto a dateset di piccole e medie dimensioni, perchè consente di reappresentare
ogni singola osservazione in modo dettagliato, mostrando come i dati si distribuiscono all'interno delle
categorie

Lo SWARMPLOT è simile allo stripplot ma distribuisce i punti evitando qualsiasi sovrapposizione creando
un effetto alveare, ideale per dataset piccoli o medi, perchè mostra la distribuzione reale dei dati
senza sovrapposizione e permette di osservare densità locali e raggruppamenti. 
La disposizoine intelligente dei punti lo rende più leggibile rispetto allo stripplot
Per dataset molto grandi può diventare affollato e rallentare il rendering

Lo stripplot è sicuramente più semplice e leggero da visualizzare, adatto a dataset grandi, 
dove la disposizione intelligente dei punti non è critica.
Lo swarplot offre maggior chiarezza per dataset piccoli o medi mostrando densità reali senza sovrapposizoni.
La scelta dei due strumenti dipende dai numero di punti e dalla necessità di evidenziare densita o 
valori replicati. 
L'uso combinato di entrambi permette di bilanciare la leggibilità del grafico e le informazioni che
esso può dasre mostrando sia la distribuzione complessita, sia la densità locale dei dati.
Un approccio avanzato consinte nel combinare lo stripplot allo swarmplot grazie ai grafici boxplot o violinplot
In questo modo la stima sintetica della distribuzione, come può essere una mediana, i quartili o la densità
viene integrata direttamente con la visualizzazione dei singoli punti, migliorando l'interpretazione,
permettendo di individuare outlier e pattern locali.
Consente di visualizzare simultaneamente la densità complessiva dei singoli valori

"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    "giorno": [
        "Lunedì", "Lunedì", "Martedì", "Martedì", "Mercoledì", "Mercoledì",
        "Giovedì", "Giovedì", "Venerdì", "Venerdì", "Sabato", "Sabato", "Domenica", "Domenica"
    ] * 5,
    "soddisfazione": [
        7, 8, 6, 7 , 8, 9, 7, 8, 9 , 10, 8, 9, 7, 8,
        6, 7, 5, 6 , 8, 8, 9, 9, 10, 10, 9, 8, 7, 6,
        5, 6, 7, 8 , 6, 7, 8, 9, 9 , 8,  8, 7, 6, 5, 
        7, 8, 9, 10, 7, 6, 8, 9, 10, 9,  7, 8, 9, 10, 
        8, 7, 6, 5,  7, 8, 9, 9, 10, 9,  8, 7, 7,  7
    ][:70],
    "fascia": [
        "Giovani", "Adulti", "Senior", "Giovani", "Adulti", "Senior", "Giovani",
        "Adulti", "Senior", "Giovani", "Adulti", "Senior", "Giovani", "Adulti"
    ] * 5
})
print(df)

plt.figure(figsize=(8,5))
sns.stripplot(data=df,x="giorno",y="soddisfazione",hue="fascia",dodge=True,jitter=0.2,palette="Set2", size=5)
plt.title("Striplot della soddisfazione per giorno e fascaie")
plt.xlabel("Giorno della settimana")
plt.ylabel("Punteggio di soddisfazione")
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
sns.swarmplot(data=df,x="giorno",y="soddisfazione",hue="fascia",dodge=True,palette="Set1", size=6)
plt.title("Swarmplot della soddisfazione per giorno e fascaie")
plt.xlabel("Giorno della settimana")
plt.ylabel("Punteggio di soddisfazione")
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
sns.violinplot(data=df,x="giorno",y="soddisfazione",inner=None,palette="coolwarm",cut=0)
sns.swarmplot(data=df,x="giorno",y="soddisfazione",hue="fascia",dodge=True,palette="Set2", size=5)
plt.title("Swarmplot combimato a vaiolinplot della soddisfazione per giorno e fascaie")
plt.xlabel("Giorno della settimana")
plt.ylabel("Punteggio di soddisfazione")
plt.legend()
plt.show()


