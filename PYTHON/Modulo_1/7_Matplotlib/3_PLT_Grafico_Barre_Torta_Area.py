import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mesi=['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic']
vendite=[120,140,222,453,5334,655,422,75,11,567,23,53]
#df=pd.DataFrame({'Mese':mesi,'Vendite':vendite})

#GRAFICO A BARRE
plt.bar(mesi, vendite,color='skyblue')
plt.title("GRAFICO A BARRE")
plt.show()

#GRAFICO A BARRE ribarlato
plt.barh(mesi, vendite,color='skyblue')
plt.title("GRAFICO A BARRE INVERTITO")
plt.show()

#GRAFICO A TORTA
plt.pie(vendite,labels=mesi, autopct="%1.1f%%")
plt.title("GRAFICO A TORTA")
plt.show()

#GRAFICO AD AREA
#molto utilizzato per dati cumulativi
x=[1,2,3,4,5]
y=[5,3,7,9,2]
plt.fill_between(x,y,0,color="lightblue",alpha=0.6)
plt.plot(x,y,color="blue")
plt.title("GRAFICO AD AREA")
plt.show()


