
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import seaborn as sns

x=np.logspace(0.1,2,100) #100 numeri spaziati in una scala logaritmica
y=x**2 * np.random.rand(100)

plt.figure(figsize=(8,5))
plt.plot(x,y,marker="o")
plt.xscale("log")
plt.yscale("log")
plt.xticks=([0.1,1,10,100],["0.1","1","10","100"])
plt.yticks=([1,10,100,1000,10000])
plt.grid(True,which="both",linestyle="--",alpha=0.5)

max_idx=np.argmax(y)
plt.annotate(f"Max={y[max_idx]:.0f}",xy=(x[max_idx],y[max_idx]),
                    xytext=(x[max_idx]+1,y[max_idx]*1.2),
                    arrowprops=dict(facecolor="black"))
plt.title("Grafico logaritmico con annotazione dinamica")
plt.show()
