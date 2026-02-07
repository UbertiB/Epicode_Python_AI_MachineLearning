"""
TEMI E STILI AZIENDALI
Standarizzare temi e stili permette di avere un 'tema aziendale' che valga per 
tutti i grafici, ognuno che rispetti determinate scelte stilistiche per rispettare
la coerenza visiva.
Grafici chiari, coerenti con i colori e font del brand.
Se non lo standarizzi, ottieni report che sembrano fatti da persone diverse.
Seabor offre potenti stumenti per controllare i nostri temi, colori, font e lauyout 
dei grafici, consentendoci di creare stili personalizzati e facilmente riuilizzabili.
Seaborn offre temi e stili predefinitvi, sono poi implementabili i propri.
Seaborn imposta lo stile tramice i rcParams di matplotlib. Quindi un tempo seaborn
influenza anche i grafici creati con matplotlib. 
La funzione chiave è sns.set_theme(...), e poi sovrascrivere dettagli con 
l'argomento rc={...}
Attenzione alla leggibilità su diversi schermi, in stampa o pdf, formati numerici
coerenti (percentuali, migliaia, valuta), griglie non invadenti, font disponibili
su tutti i pc aziendali e colori accessibili.
Concetti utili:
* Style: sfondo, grglia, 'spines' (cornici)
* Context: scala degli elementi (presentazione vs notebook)
* Palette: ciclo di colori
Seborn fornisce diversi tempi di base, i principali sono:
1) darkgrid (più adatto per esplorazione iterativa dei dati, grazie alla griglia visibile)
2) whitegrid (più adatto a pubblicazioni stampate o report aziendali)
3) dark
4) white
5) ticks
Ogni tema modifica gli elementi di fondo del grafico (sfondo, griglia, colori 
degli assi, e ticks)
I tempo possono essere impostati tramite set_theme(style="whitegrid")
Ooppure modificare temporanemaente all'interno di un blocco con axesstyle ed il nome
per applicazioni locali.
Seaborn concente un controllo dettagliato sugli elementi grafici con la funzione 
set_theme e set_contest set_style set_palette
set_rc per impostare parametri di matplotlib

La palette dei colori può essere una lista di colori esadecimali o rgb o generata 
con sns.color_palette

Il font gioca un ruolo essenziale nella leggibilità e nella coerenza visiva con altri
materiali aziendali.
Attraverso set font o si cambia il font, la dimensione, peso, e famiglia tipografica
i font sans serfi prefereibili per presentazione e dashboard
mentre serif e monospece in contesti accademici o tecnici

E' possibile creare colori, font stili in una funzione personalizzata per richiamarla
all'occorenza senza dover riscrivere sempre tutto.

"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(0)
df=pd.DataFrame({
    "categoria":np.repeat(["A","B","C"],50),
    "valore": np.random.randn(150),
})
#
#Temi predefiniti
#
sns.set_theme(style="whitegrid")
sns.boxplot(data=df,x="categoria",y="valore", palette="deep")
plt.title("Tema predefinito: whitegrid")
plt.show()

#
#Palette personalizzati
#

#palette aziendale
custom_palette = ["#004488", "#BB5566", "#DDAA33"]
sns.set_palette(custom_palette) #palette di default per tutte le figura
sns.palplot(sns.color_palette())

sns.barplot(data=df, x="categoria", y="valore", ci=None) #barplot che riprende tema aziendale
plt.title("Palette personalizzata aziendale")
plt.show()

#
#Tema aziendale personalizzato
#
def set_tema_azienda():
    sns.set_theme(
        style="whitegrid",
        palette=["#002B5B", "#E43D40", "#F2C14E"],
        rc={
            "axes.facecolor": "#F8F9FA",
            "axes.labelcolor": "#002B5B",
            "xtick.color": "#333333",
            "ytick.color": "#333333",
            "font.family": "sans-serif",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.titleweight": "bold"
        }
    )

set_tema_azienda()
sns.lineplot(x=range(10), y=np.random.randn(10))
plt.title("Tema aziendale personalizzato")
plt.show()

