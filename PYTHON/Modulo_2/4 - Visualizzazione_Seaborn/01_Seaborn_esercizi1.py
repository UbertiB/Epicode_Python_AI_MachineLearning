

import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")

#
#SEABORN 
#

#ISTOGRAMMA dei valori (histplot)
#utile per capire la distribuzione, se pochi "total_bill" fanno tutto
#(coda lunga? velori zero? picchi strani?)
sns.histplot(data=df, x="total_bill")
plt.title("Distribuzione totale conto (ISTOGRAMMA histplot)")
plt.show()

#
#MATPLOTLIB (più verboso ma maggior controllo sulla figura)
#
plt.hist(df["total_bill"], bins=20)
plt.title("Distribuzione totale conto (Matplotlib)")
plt.xlabel("total_bill")
plt.ylabel("frequenza")
plt.show()


#SCATTER PLOT con regressione
#per identificare relazioni tra variabili
#(crescono insieme? oppure stai correlando due cose che non c'entrano nulla?)
sns.scatterplot(data=df, x="total_bill", y="tip")
plt.title("Relazione conto vs mancia (SCATTERPLOT)")
plt.show()

#aggiungi una linea di regressione
sns.regplot(data=df, x="total_bill", y="tip")
plt.title("Relazione conto vs mancia (REGPLOT)")
plt.show()

#BOXPLOT mostra mediana, quartili, outlier
#per identificare gli outlier che falsano le medie
#valori fuori scala? errori di caricamento? casi 'one-shot'
sns.boxplot(data=df, x="day", y="total_bill")
plt.title("Distribuzione conto per giorno (BOXPLOT)")
plt.show()

#HEATMAP di correlazione
corr=df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Heatmap correlazioni (HEATMAP)")
plt.show()

sns.pairplot(df, vars=["total_bill", "tip", "size"])
plt.title("scatter matrix PAIRPLOT")
plt.show()



