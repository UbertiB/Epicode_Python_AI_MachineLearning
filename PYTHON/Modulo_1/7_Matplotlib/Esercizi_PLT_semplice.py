import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mesi=['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic']
vendite=[120,140,222,453,5334,655,422,75,11,567,23,53]
df=pd.DataFrame({'Mese':mesi,'Vendite':vendite})

plt.bar(df['Mese'],df['Vendite'],color='skyblue')
plt.title('Istogramma delle vendite mensili')
plt.xlabel('Mese')
plt.ylabel('Vendite')
plt.show

plt.plot(df['Mese'],df['Vendite'], marker='o',color='green')
plt.title('Grafico a linee delle vendite mensili')
plt.xlabel('Mese')
plt.ylabel('Vendite')
plt.show

plt.pie(df['Vendite'],labels=df['Mese'])
plt.title('Grafico a torta delle vendite mensili')
plt.show
