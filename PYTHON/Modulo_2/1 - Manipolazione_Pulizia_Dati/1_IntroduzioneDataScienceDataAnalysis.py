"""
- Cos'è la DataScience: campo che combina statistica, informatica, matematica. 
       Deve conoscere il dominio (esempio medicina, aziendale, ecc) per estrarre valore dai dati 
       e supportare le decisioni, previsioni e automazione
       Obiettivi: trasformare i dasti grezzi in informazioni utili, creare modelli predittivi descrittivi
       , supportare le persone che devono decidere.
       La datascience comprende al suo interno la data analysis
- Cos'è la Data Analysis: processo in cui si trasforma grandi quantità di dati in informazioni utili a prendere decisioni
       tipologie di analisi: 
              1) descrittiva: cosa è successo 
              2) analisi diagnostica: perchè è successo 
              3) analisi predittiva: cosa accadrà in futuro 
              4) analisi prescrittiva: azioni da intraprendere
       ETA exploraty data analisty significa prendere un dataset e giocarci per recuperare informazioni
       necessario per capire i dati (data storytelling)
       Excel può andare bene per dati di piccole dimensioni
       Pandas con dati più grandi dimensioni
- Differenze e strumenti principali: 
       obbiettivo: 
              Data science: crea modelli, previsioni, automazione; 
              Data Analysis: Interpreta e descrive i dati
       Strumenti: 
              Data Science: ML, AI; Python, R, Big Data
              Data Analysis: SQL, Excel, Python (pandas), R
       Approccio:
              Data Science: innovativo, predittivo
              Data Analysis: Eplorativo, descrittivo
       Risultato:
              Data Science: Algoritmi, modelli predittivi
              Data Analysis: Report, dashboard, insight
       Un analista dati prendere i dati li contestualizza, li capisce prepara report e dashboart 
       che aiutano a prendere decisioni su dati passati, 
       mentre un data science crea il modello che prevede e suggerisce le strategie future
       La data analysis è il punto di partenza per arrivare alla data science
       La data science comprende anche la data analysis
- Processo tipico: 
- Conclusioni:
"""
import pandas as pd
import matplotlib.pyplot as plt

dati= {"Settimana": [1,2,3,4,5,6],
       "Vendite": [250,300,400,350,450,500]}

df = pd.DataFrame(dati)
media_vendite = df["Vendite"].mean()
print(f"Media vendite: {media_vendite}")
# grafico a barre (metodo .bar)
plt.bar(df["Settimana"],df["Vendite"],color="skyblue")
plt.axhline(media_vendite,color="red",linestyle="--",label="Media")
plt.xlabel("Settimana")
plt.ylabel("Vendite")
plt.title("Vendite settimanali")
plt.legend()
plt.show()