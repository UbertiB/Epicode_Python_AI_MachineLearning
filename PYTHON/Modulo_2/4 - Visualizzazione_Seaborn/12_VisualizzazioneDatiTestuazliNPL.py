"""
DATI TESTUALI E NLP
Visualizzazioni dei dati testuali e nlp
L'ANALISI DEI TESTI è una della frontiere più interessanti della data science moderna
In un mondo dominato dalle comunicazioni digitali, recensioni online, social, articoli di giornale,
il testo è una fonte ricchiessima di informazioni qualitative e quantitative.
Tuttavia la sua natura NON STRUTTURATA rende necessarie tecniche nlp per estrarre quantificare e visualizzare
i pattern nascosti.
La visualizzazione svolge un ruolo chiave in questo processo, consente di esplorare la FREQUENZA della parole,
le RELAZIONI tra termini, i SENTIMENTI e persino i TEMPI DOMINANTI di testi.
Seaborn unito ad altre liberie, permette di rappresentare graficamente risultati complessi, rendendo immediatamente
interpretabili anche da chi non a conoscenze linguistiche approfondite

FREQUENZA DELLA PAROLE
Il primo pasos nell'analisi dei testi è lo studio della frequenza delle parole, consente di identificare
i termini più ricorrenti e comprendere la sturttura lessicale del corpus
una volta eseguita la tokenizzazione, ciao la suddivisione del testo in parolo o frasi si può costruire una
distribuzione di frequenza e rappresentarla graficamente con istrogrammi o grafici a barre
Seaborn è ideale per questa visualizzazione, permette di ordinare parole per frequenza ed applicare pallette di colori
Le distribuzioni di frequenza aiutano non solo ad indivisuare parole comuni ma anche a rilevare stopword, termini
tecnici o specificità linguistiche di un dominio
Possono essere utilizzate come base per successive analisi di sentiment o topping modelling

RELAZIONI TRA LE PAROLE
Oltre alla frequenze indivisuali, è importante comprendere le relazioni tra le parole. Le co-occorenze
mostrano quanto spesso due termini appaiono insieme in un determinato contesto. 
La relazioni possono essere rappresentate con heatmap di correlazione tra le parole dove intensità  
del colore indica la forza della co-ccorenza
un altra possibilità è costruire grafici di rete in cui i nodi rappresentano parole ed i archi le relazioni 
tra esse con spessore proporzionale alla frequenza con cui appaiono insieme.

EMBENDDING E RIDUZIONE DIMENSIONALE
Con l'avvento dei modelli di word embenddings (come Word2Vec o GloVe, BERT) è possibile rappresentare le parole
come vettori numerici in uno spazio multidimensionale.
Ogni dimensione codifica una componente semantica e parole con significati simili tendono a collocarsi vicino
nella spazio vettoriale.
Per visualizzare questi spazi si usano tecniche di riduzione dimensionale come PCA o TSNE queste permettono
di rappresentare i vettori delle parole su due o tre dimesnioni, rendendo visibile le relazioni semantiche.
Con seaborn possiamo tracciar scatterplot bi-dimensionali che mostrano cluster di parole semantiche affini
come termini positivi o negativi o gruppi appartennenti a specifici domini.
Questo è utile per validare, visivamente, la qualità di un embedding confrontare modelli linguistici diversi.

ANALISI SENTIMENT
L'analisi del sentiment è una delle applicazioni più diffuse dell'nlp, consiste nel recensire testi, come
recensioni, twit o commenti in categorie di tono emotivo, tipicamente positivo/negativo/neutro.
Una volta ottenuto lo score di sentiment per ciascun testo è possibile rappresentare la distribuzione dei 
valori con istrogrammi kdeplot o boxplot
Consente anche di combinare la distriìbuzione del sentimento con altre variabili come categoria del prodotto
o la data di pubblicazione, consentendo di osservare tendenze nel tempo e tendenze tra i gruppi.
Le visualizzazioni di sentiment aiutano a comprendere la percezione generale di un argomento e possono evidenziare
picchi di negatività o positività associati ad eventi specifici.
In contesti aziendali rappresentano uno strumento prezioso per il monitoraggio della reputazione o analisi della
customer experience.

TOPIC MODELLING
Il topic modelling è una tecnica di nlp per identificare automaticamente i temi principali presenti in un 
insieme di argomenti.
Uno degli algoritmi più nota è LDA (o NMF) e consente di estrarre argomenti e assegna a ciascun documento una
distribuzione di probabilità sui diversi topic.
Le visualizzazione possono essere diverse tra le quali:
- barplot delle parole più rappresentative per ogni topic
- heatmap delle probabilità topic documento
- grafici bidimensionali che mostrano la separazione tra argomenti tramite la riduzione dimensionale
- bubble chart con importanza topic
Obbiettivo è offrire una rappresentazione chiara della struttura tematica del corpus, facilitando interpretazione
dei modelli e la scoperta di pattern semantici ricorrenti

CONFRONTO DOCUMENTI
Un aspetto importante è il confronto tra documenti, la similarità testuale può essere misurata tramite tecniche 
di embedding o metriche più semplici come la similarità del coseno tra vettori di frequenza delle parole
Le visualizzazioni più comuni includono:
- heatmap di similarità
- Cluster dendogrammi
- mappe bidimensionali
in cui documenti 'simili' si collocano simili nello spazio.
Utile per confrontare recensioni, articoli, o risposte aperte in sondaggi.

Spesso è importante escludere le STOPWORDS dai testi prima di fare analisi. Le stopwords sono parole comuni
che spesso non aggiungono significato utile quando analizzi testi. Esempi in italiano; il, la, e, di, un
Servono quando fai analisi testuali (NLP) vuoi che il modello si concentri su parole 'informative'. Se lasci
le stopwords, nel top frequenze ti escono loro (di, e, che) e non capisci nulla del contenuto reale.
Esempio:
testo='manca il ddt di consenga e il certificato del materiale'
senza rimuovere le stopwords, le parole più frequenti includono il, di, e
rimuovendo le stopwords, restano parole più utili: manca, ddt, consegna, certificato, materiale
Le stopwords possono essere costruite manualmente o recuperata utilizzando una lista di stopword già pronta
(NLTK, oppure spaCy)
    Esempio 1 
        testo = "manca il ddt di consegna e il certificato del materiale"
        parole = [p.lower() for p in testo.split()]
        stop = {"il", "di", "e", "del"}  # esempio piccolo, incompleto
        pulite = [p for p in parole if p not in stop]
    Esempio 2
        from nltk.corpus import stopwords
        testo = "manca il ddt di consegna e il certificato del materiale"
        parole = [p.lower() for p in testo.split()]
        stop = set(stopwords.words('italian'))
        pulite = [p for p in parole if p not in stop]
Non sempre tutte le stopword (automatiche) sono da rimuovere tutte. Alcune 'parole comuni' sono informative 
a livello gestionale, esempio:
- negazioni: 'non', 'senza' (cambiano il senso)
- preposizioni che indicano relazioni: 'da', 'a', 'per'
- unità e sigle: 'mm', 'kg', 'nr', 'pz'
Quindi stopword standard + lista personalizzata aziendale, dopo aver visto i risultati
In ERP parole tipo 'articolo', 'cliente' potrebbero essere troppo generiche e dominare il testo, valuta
la possibilità di includerle nelle stopwords, misura effetti con e senza

"""

import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np

#
#ANALISI DI FREQUENZA
#
testo="Data Science è un dei campi più affascinanti. La science dei dati unisce diversi campi: statistica, programmazione e analisi."
parole=[p.lower() for p in testo.split()]
#print(parole)
frequenze=Counter(parole) #crea un dizionario di parole con il conteggio 
#print(frequenze)
df_freq=pd.DataFrame(list(frequenze.items()), columns=["parola", "conteggio"])
print (df_freq)
plt.figure(figsize=(15,6))
sns.barplot(data=df_freq,x="parola",y="conteggio",palette="crest")
plt.title("Frequenza della parole")
plt.show()

#
#VISUALIZZAZIONE EMBENDDING CON RIDUZIONE DIMENSIONALE  (PCA)
#
#utile per vedere la somiglianza tra i vettori in modo visivo

from sklearn.decomposition import PCA

np.random.seed(0)
embeddings=np.random.rand(10,50)
print(f"Completo: \n{embeddings}")
pca=PCA(n_components=2)
ridotto=pca.fit_transform(embeddings) #riduzione dimensionale a 2 componenti (da 50 originali)
print(f"Ridotto: \n{ridotto}")
df=pd.DataFrame(ridotto, columns=["PC1","PC2"])
df["parola"]=[f"word{i}" for i in range(10)]
print(df)
sns.scatterplot(data=df,x="PC1",y="PC2",hue="parola",palette="tab10")
plt.title("Visualizzazione embendding con PCA")
plt.show()

#
#DISTRIBUZIONE DEL SENTIMENT
#
np.random.seed(1)
df_sentiment=pd.DataFrame({
    "categoria":np.random.choice(["positiva","negativa","neutra"],200),
    "valore":np.random.normal(0,1,200)
})
sns.boxplot(data=df_sentiment,x="categoria",y="valore",palette="Set2")
plt.title("Distribuzione del sentiment per categoria")
plt.show()
#utile per confrontare le distribuzioni per categoria di sentiment
