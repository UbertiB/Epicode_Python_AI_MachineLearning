
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")

#
# 1) grafici di DISTRIBUZIONE
#

# a) histplot (distribuzione di una variabile numerica)

#da utilizzare quando si vuole capire forma, picchi, zeri, codce
#da non utilizzare per confronto tra troppe categorie

sns.histplot(data=df, x="total_bill")
plt.title("Distribuzione total_bill (HISTPLOT) no bins")
plt.show()

#con bins=20 divide tutti i 'total_bill' in 20 catagorie e vede la distribuzione per 
#ogni categoria, se non è indicato il bins seaborn ne calcola automaticamente uno suo
#in base ai dati, se si confrontano due istogrammi indicare sempre il bins, per fare in
#modo che abbiano la stessa granularità
sns.histplot(data=df, x="total_bill", bins=20)
plt.title("Distribuzione total_bill (HISTPLOT) bins=20")
plt.show()

# b) kdeplot (distribuzione 'lisciata' (stime densità))

#non mostra i dati reali, ma una curva che stima 'dove si concentrano i valori'
#capisci chi ha valori medi più alti, chi ha distribuzione più concentrata, code lunghe
#serve per confrontare distribuzioni, da utilizzarsi solo se si hanno a disposizione
#abbastanza dati (almeno qualche centinaio)
#mostra dove i valori sono più concentrati e la forma della distribuzione

sns.kdeplot(data=df, x="total_bill")
plt.title("KDE total_bill (unico colore, non indico hue)")
plt.show()

sns.kdeplot(data=df, x="total_bill", hue="sex", fill=True)
plt.title("KDE total_bill con confronta tra gruppi (hue='sex')")
plt.show()

#istogramma + kde istogramma = realtà kde = interpretazione
sns.histplot(data=df, x="total_bill", bins=20, stat="density")
sns.kdeplot(data=df, x="total_bill", hue="sex", fill=True)
plt.title("Istogramma (realtà) + KDE (interpretazione)")
plt.show()

#
# 2) grafici di CONFRONTO STATISTICO tra gruppi
#

#a) boxplot
#quando si vuole confrontare distribuzioni tra categorie, trovare outlier

sns.boxplot(data=df, x="day", y="total_bill")
plt.title("BOXPLOT total_bill per day")
plt.show()

#b) boxplot + forma distribuzione completa
sns.violinplot(data=df, x="day", y="total_bill", hue="sex", split=True)
plt.title("VIOLINPLOT total_bill per day e sex")
plt.show()

#c) scatterplot
#quando voglio verificare correlazioni, pattern, cluster tra due variabili numeriche
sns.scatterplot(data=df, x="total_bill", y="tip", hue="smoker")
plt.title("SCATTERPLOT total_bill vs tip")
plt.show()

#d) regplot
#scatter+retta di regressione (lineare)
#quando si vuole capire se relazione è circa lineare
#come cambia y al variare di x
sns.regplot(data=df, x="total_bill", y="tip")
plt.title("REGPLOT Regressione tip su total_bill")
plt.show()

#
# 3) grafici CATEGORIALI
#

# a) countplot
#conteggi per categoria, quando si vuole vedere volumi per categoria

sns.countplot(data=df, x="day")
plt.title("COUNTPLOT Conteggio record per day")
plt.show()

#b) barplot
#media stimata per categoria, quandi si confranta media tra gruppi

sns.barplot(data=df, x="day", y="tip", hue="sex")
plt.title("BARPLOT Tip medio per day e sex")
plt.show()

#
# 4) grafici MULTIVARIATI
#

#a) lmplot 
#grafico multivariante per esplorare relazioni numeriche, non è un grafico descrittivo
#usa due variabili numeriche (x,y) 
#puoi aggiungere variabili categoriali (hue,row,col)
#puoi generare più grafici contemporaneamente(FacetGrid)
#pertanto analizza più dimensioni insieme
#ma può anche essere considerato un grafico di relazioni tra variabili numeriche
#il cuore di lmplot è la relazione x-y, la regressione è l'oggetto principale
#come cambia y al variare di x

sns.lmplot(data=df, x="total_bill", y="tip")
plt.title("IMPLOT regressione (relazione) tra conto e mancia")

# b) pairplot
#tutte le relazioni tra numero definito di categorie

sns.pairplot(df[["total_bill", "tip", "size"]])
plt.title("PAIRPLOT relazioni tra categorie")
plt.show()

#c) heatmap (correlazioni)
#matrice numerica visualizzata a colori usata per vedere correlazioni 

corr = df[["total_bill", "tip", "size"]].corr()
sns.heatmap(corr, annot=True)
plt.title("HEATMAP Correlazioni tra variabili numeriche")
plt.show()

#
# 5) grafici TEMPORALI
#
#nell'esempio tips non c’è una colonna tempo reale. 
#quindi qui faccio una “sequenza record” per farti vedere l’uso di lineplot

#a) lineplot
#trend su asse ordinato, da utilizzarsi su serie temporali vere (esempio giorni, mesi, anni, ore, minuti, ecc)
df2 = df.reset_index().rename(columns={"index": "seq"})
sns.lineplot(data=df2, x="seq", y="total_bill")
plt.title("LINEPLOT su sequenza record (non è tempo reale)")
plt.show()












