"""

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns


x=np.linspace(0,10,100)
y1=np.sin(x)
y2=np.cos(x)
y3=y1*y2
dates=pd.date_range("2025-01-01",periods=10)
df=pd.DataFrame({
    "Date":dates,
    "Vendite":[100,120,150,130,160,170,200,210,190,220],
    "Profitto":[20,25,30,28,35,33,40,42,38,45]
})
fig=plt.figure(figsize=(12,6))
gs=gridspec.GridSpec(2,2,figure=fig)

ax1=fig.add_subplot(gs[0,0])
ax2=fig.add_subplot(gs[0,1])
ax3=fig.add_subplot(gs[1,:])

ax1.plot(x,y1,label="sin(x)")
ax1.plot(x,y2,label="cos(x)")
ax1.set_title("Funzioni trigonometriche")
ax1.legend()
ax1.grid(True)

sns.boxplot(y=df["Vendite"],ax=ax2)
ax2.set_title("Boxplot vendite")

ax3.plot(df["Date"],df["Vendite"],label="Vendite")
ax3.plot(df["Date"],df["Profitto"],label="Profitto", marker="s")
ax3.set_title("Serie temporali")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()
