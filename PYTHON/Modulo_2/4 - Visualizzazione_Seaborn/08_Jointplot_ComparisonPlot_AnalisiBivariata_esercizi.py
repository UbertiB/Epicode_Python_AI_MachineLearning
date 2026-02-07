import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")
sns.set_theme(style="whitegrid")

#
# Esercizio 1
#

# Creare un Jointplot 2d con KDE, aggiungendo HUE per una variabile categoriale e configurando le 
# distribuzioni marginali come kde con rug plot.

sns.jointplot(data=df,x="total_bill",y="tip",kind="reg")
plt.legend()
plt.title("total bill vs tip (male/female)")
plt.tight_layout()
plt.show
#oppure
g = sns.jointplot(data=df,x="total_bill",y="tip",hue="sex",kind="kde",fill=True,marginal_kws=dict(rug=True), palette="Set2", height=7)
g.fig.subplots_adjust(top=0.92)  # lascia spazio sopra per il titolo
g.fig.suptitle("Jointplot KDE: total_bill vs tip per sesso", y=0.99)
plt.show()
#mostra una relazione lineare positiva tra total_bill e tip, con differenze tra i sessi
#la distribuzione marginale di total_bill mostra che i conti più comuni sono tra 10 e 20 dollari
#ci sono delle differenze di distribuzione delle mance per sesso (la kde male mostra più 'massa'
#sui conti alti e mance alte)
#la KDE mostra 'code' verso conti più alti.

#
# Esercizio 2 
#

# Costruisci una Comparison Plot combinato con violinplot boxplot e punti sovrapposti,
# confrontando almeno due variabili categoriali

plt.figure(figsize=(10,6))

# Violinplot
sns.violinplot(data=df,x="day",y="total_bill",hue="sex",palette="Pastel1",split=True,inner=None)
# Boxplot sovrapposto
sns.boxplot(data=df,x="day",y="total_bill",hue="sex",palette="Set2",fliersize=0,width=0.2,dodge=True)
# Scatter points sovrapposti
sns.stripplot(data=df,x="day",y="total_bill",hue="sex",palette="Set1",dodge=True,size=5,alpha=0.5)

plt.title("Comparison Plot combinato: violin + box + punti")
plt.ylabel("Total Bill")
plt.xlabel("Day")
plt.legend([],[], frameon=False)  # Evita doppia legenda
plt.show()

# Esercizio 3
# Creare un FacetGrid avanzato che mostri scatterplot e KDE per più categorie, aggiungendo legenda e differenziazione per gruppi.

g = sns.FacetGrid(df,col="time",row="smoker",hue="sex",margin_titles=True,palette="Set1",height=4, aspect=1)
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip", alpha=0.6, s=40)
g.map_dataframe(sns.kdeplot, x="total_bill", y="tip", levels=5, color="gray", alpha=0.3)

g.add_legend(title="Sex")
g.set_axis_labels("Total Bill", "Tip")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("FacetGrid scatter + KDE: tip vs total_bill per time, smoker e sesso")
plt.show()

#evidenzia una relazione lineare positiva, più debole per i fumatori rispetto ai non fumatori
#La relazione tra mancia e totale conto c'è in tutti i pannelli, cambia 'quanto' e quanto rumore c'è
#In ogni facet la nube è inclinata verso l'alto (relazione linere positiva), conti più alti tendono 
#ad avere mance più alte. Quello che cambia è dispersione e presenza outlier.
#Pranzo+fumatori=pochi punti, qualsiasi conclusione è qui fragile (la KDE può risultare poco affidabile con pochi dati)
#Cena + non fumatori =più punti, quindi forma e trend sono più credibili
#Cena ha importo più alti ma anche più variabili rispetto al pranzo. Questo suggerisce che time (dinner/lunch)
#influisce sul comportamento della mancia
#Nel pannello cena + fumatori si nota una maggiore dispersione dei punti, suggerendo che i fumatori 
# tendono a essere meno coerenti nel dare mance rispetto ai non fumatori.
#Per quanto riguarda il sesso, in generale non ci sono differenze evidenti tra maschi e femmine, non si
#vedono due nuvole separate, ma si sovrappongono molto.