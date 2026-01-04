"""
matplotlib ha degli stili predefiniti che cambiano da versione a versione. 
Quelli classici sono:
- default
- classic
- ggplot
- seaborn-v0_8 (non è di seaborn, è di matplotlib, spesso vecchi stili)
- bmh
- fast
- dark_background
- grayscale
- tableau-colorblind10

Si possono anche creare stili personalizzati (magari con colori aziendali) partendo da uno stile default
"""

#UTILIZZO DEGLI STILI PREDEFINITI IN MATPLOTLIB

import matplotlib.pyplot as plt

input_values=[1,2,3,4,5]
squares=[1,4,9,16,25]
plt.style.use('tableau-colorblind10')  #IMPOSTO STILE PREDEFINITO
fig,ax=plt.subplots()
ax.plot(input_values,squares,linewidth=3)
ax.set_title("Square Numbers",fontsize=24)  
ax.set_xlabel("Value",fontsize=14)
ax.set_ylabel("Square of Value",fontsize=14)
ax.scatter(2,4,)  #EVIDENZIO UN PUNTO SPECIFICO

plt.show()

#elenco stili predefiniti:
print(plt.style.available)
#per vedere i files di configurazione (.mplstyle):
import matplotlib
print(matplotlib.get_configdir())
#per vedere lo stile in  uso:
plt.style.use("tableau-colorblind10")


