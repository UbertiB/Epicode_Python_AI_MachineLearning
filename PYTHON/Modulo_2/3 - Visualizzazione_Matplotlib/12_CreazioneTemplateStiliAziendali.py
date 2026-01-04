"""
Creazione di template per stili aziendali, per coerenza visiva
Creare template riutilizzabili che includono palette, font, branding, e layout riutilizzabili.
Per fare in modo che ogni grafico rispetti lo stile aziendale
Importante definire uno stile, con colori principali, font leggibili su schermo e su stampa
e le linee devono trasmettere le informazioni in modo chiaro.
Matplotlib ci consente di salvare tutte le impostazioni di stile in un file (MPLSTYLE)
per evitare di dover impostare i parametri di stile tutte le volte.
Sarà possibile applicare questo file a tutti i grafici.

La scelta della palette colori è uno degli aspetti più importante, i colori devono essere
armonizzati ai colori aziendali, consigliabile definire palette primaria per linee e grafici
principale ed una secondaria per evidenziare dettagli, annotazioni, o trend particolari.
Una palette aziendale ben progettata permette di creare grafici immediatamente riconoscibili 
con il brand.
Consigliabile utilizzare fonts aziendali o in assenza font neutri  e leggibili 
come sanserif e serif per titoli.

I templete sono utili per fare in modo che tutti i grafici abbiano la stessa faccia (font, colori, spessori,
griglie, formati, loghi)

"""

import matplotlib.pyplot as plt
import numpy as np
plt.style.use("azienda.mplstyle")

x=np.arange(10)
y=np.random.randint(5,15,size=10)
plt.plot(x,y, label="vendite")
plt.title("Grafico vendite stile aziendale")
plt.xlabel("Giorni")
plt.ylabel("Vendite")
plt.legend()
plt.show()


palette={"primario": "#192155", "secondario": "#d60077"}

x=np.arange(10)
vendite=np.random.randint(50,150,size=10)
acquisti=np.random.randint(30,100, size=10)
plt.plot(x,vendite,color=palette["primario"])
plt.plot(x,acquisti,color=palette["secondario"])
plt.title("Vendite vs acquisti")
plt.xlabel("Mese")
plt.ylabel("Unita")
plt.legend()
plt.show()

#dico a matplotlib di utilizzare la famiglia di font 'sans-serif'
plt.rcParams["font.family"] = "sans-serif"
#definisco l'elenco dei fonts prefeiti in ordine, cioè se non trova arial utilizza calibri, se non lo trova usa dejavu (quasi sempre presente perchè arriva da matplotlib)
plt.rcParams["font.sans-serif"] = ["Arial", "Calibri", "DejaVu Sans"]
x=np.linspace(0,10,100)
y=np.sin(x)

plt.plot(x,y,label="Trend")
plt.title("Trend settimanale - Brand xyz")
plt.xlabel("Giorni")
plt.ylabel("Valore")
plt.legend()
plt.show()

