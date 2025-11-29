import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mesi=['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic']
vendite=[120,140,222,453,5334,655,422,75,11,567,23,53]
#df=pd.DataFrame({'Mese':mesi,'Vendite':vendite})

# GRAFICO A LINEE
#definisco il tipo di grafico e i dati
plt.plot(mesi,vendite,label="vendite 2025")
#titolo
plt.title ("grafico a linee PROVA",fontsize=14,color='red')
#griglia
plt.grid(True,linestyle='--',alpha=0.7)
#plt.marker='*'
#asse X
plt.xlabel("Mesi",fontsize=18,color='green')
#asse Y
plt.ylabel ("Vendite")
#legenda (gestire la proprietà label)
plt.legend( loc='upper left')
#dimensioni grafic
#plt.figure(figsize=(8,6))
#visualizzo grafico
plt.show ()
#salvo il grafico su file
plt.savefig('graficoprova.pdf',dpi=300)

#plt.plot(df['Mese'],df['Vendite'], marker='o',color='green')
#plt.title('Grafico a linee delle vendite mensili')
#plt.xlabel('Mese')
#plt.ylabel('Vendite')
#plt.show

#plt.pie(df['Vendite'],labels=df['Mese'])
#plt.title('Grafico a torta delle vendite mensili')
#plt.show
