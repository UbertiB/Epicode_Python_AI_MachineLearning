import matplotlib.pyplot as plt
import pandas as pd

#DATE NEI GRAFICI
date=pd.date_range("2023-01-01",periods=6, freq="ME")
valori=[10,20,15,25,30,28]
plt.plot(date,valori,marker="o")
plt.title("VISUALIZZARE IL TEMPO")
plt.xlabel("Data")
plt.ylabel("Valore")
plt.show()

#SUBPLOT
plt.subplot(2,1,1)
plt.plot([1,2,3],[1,4,9],color="red")
plt.subplot(2,1,2)
plt.plot([1,2,3],[1,2,3],color="blue")
plt.title("GRAFICI MULTIPLI")
plt.show()

