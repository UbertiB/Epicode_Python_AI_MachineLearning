import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

date=pd.date_range("2023-01-01",periods=22, freq="ME")

vendite=[10,20,12,15,25,22,24,28,30,35]

np.random.seed(42)
eta_clienti=np.random.randint(18,65,50)

spesa_media=eta_clienti * 2 + np.random.randint(-20,20,50)
plt.figure(figure=(8,5))
plt.plot(date,vendite,market="o", color="blue", linewidht=2,linestyle="--",label="vendite")
plt.title("andamento mensile vendite 2023")
plt.xlabel("mese")
plt.ylable("vendite (migliaia  di euro)")
plt.legend()
plt.grid(True,linestyle="--",alpha=0.6)
plt.show()

plt.figure(figsize=(7,5))
plt.hist(eta_clienti, bins=8, color="skyblue", edgecolor="black", alpha=0.8)
plt.title("distribuzione eta dei clienti")
plt.xlabel("eta")
plt.ylabel("frequenza")
plt.show()

plt.figure(figsize=(8,5))
plt.scatter(eta_clienti,spesa_media, color="red", marker="o", alpha=0.7)
plt.title("relazione tra eta e spesa media")
plt.xlabel("eta dei clienti")
plt.ylabel("spesa media in Euro")
plt.grid(True,alpha=0.5)
plt.show()

fig,ax=plt.subplot(2,2,figuresize=(10,8))

ax[0,0].plot (date,vendite,marker="o", color="blue")
ax[0,0].set_title("vendite mensili")

ax[0,1].hist (eta_clienti,bins=8, color="orange",edgecolor="black")
ax[0,1].set_tile("Distribuzione eta")

ax[1,0].scatter(eta_clienti,spesa_media,color="green",alpha=0.7)
ax[1,0].set_tile("Eta vs spesa")

ax[1,1].fill_between(date,vendite,color="lightblue",alpha=0.6)
ax[1,1].plot(date,vendite,color="blue")
ax[1,1].settile("Vendite comulativa")

plt.tight_layout()
plt.show()
             
              