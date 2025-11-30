import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(0)
prodotti = ['A', 'B', 'C', 'D']
regioni = ['Nord', 'Centro', 'Sud']
mesi = list(range(1, 13))
anni = [2024, 2025]

records = []
for anno in anni:
    for mese in mesi:
        for regione in regioni:
            vendite = np.random.poisson(lam=200, size=len(prodotti))
            for i, prodotto in enumerate(prodotti):
                records.append([anno, mese, regione, prodotto, vendite[i]])


df = pd.DataFrame(records, columns=['Anno', 'Mese', 'Regione', 'Prodotto', 'Vendite'])
df.set_index(['Anno', 'Mese', 'Regione', 'Prodotto'], inplace=True)


totali_annuali = df.groupby(['Anno', 'Prodotto']).sum().unstack()['Vendite']
percentuali = totali_annuali.div(totali_annuali.sum(axis=1), axis=0) * 100

df_reset = df.reset_index()
df_pivot = df_reset.pivot_table(index=['Anno', 'Mese'], columns='Prodotto', values='Vendite', aggfunc='sum')
correlazioni = df_pivot.corr()


plt.figure(figsize=(18, 12))


plt.subplot(2, 2, 1)
plt.imshow(correlazioni, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Correlazione')
plt.xticks(range(len(prodotti)), prodotti)
plt.yticks(range(len(prodotti)), prodotti)
plt.title('Correlazioni tra prodotti')
for i in range(len(prodotti)):
    for j in range(len(prodotti)):
        plt.text(j, i, f"{correlazioni.iloc[i, j]:.2f}", ha='center', va='center', color='black')


plt.subplot(2, 2, 2)
bottom = np.zeros(len(totali_annuali))
for prodotto in prodotti:
    plt.bar(totali_annuali.index, totali_annuali[prodotto], bottom=bottom, label=prodotto)
    bottom += totali_annuali[prodotto].values
plt.title('Vendite annuali per prodotto')
plt.ylabel('Totale vendite')
plt.legend()


plt.subplot(2, 2, 3)
df_mensili = df_reset.groupby(['Anno', 'Mese']).sum().reset_index()
df_mensili['Periodo'] = df_mensili['Anno'].astype(str) + '-' + df_mensili['Mese'].astype(str)
plt.plot(df_mensili['Periodo'], df_mensili['Vendite'], marker='o')
plt.xticks(rotation=45)
plt.title('Trend vendite mensili totali')
plt.ylabel('Vendite')


plt.subplot(2, 2, 4)
plt.scatter(df_pivot['A'], df_pivot['B'], alpha=0.7)
plt.xlabel('Vendite Prodotto A')
plt.ylabel('Vendite Prodotto B')
plt.title('Confronto vendite A vs B')

plt.tight_layout()
plt.show()


print("Totali annuali per prodotto:\n", totali_annuali)
print("\nPercentuali di vendita per prodotto:\n", percentuali.round(2))
print("\nCorrelazioni tra prodotti:\n", correlazioni.round(2))

