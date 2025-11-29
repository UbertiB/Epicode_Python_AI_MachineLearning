import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
# Crea un array con i numeri da 1 a 10
arr = np.arange(1,11)
# calcola i quadrati e i cubi
quadrati = arr**2
cubi = arr**3   
# organizza i dati in un DataFrame
df = pd.DataFrame({ 
    "Numero": arr,
    "Quadrato": quadrati,
    "Cubo": cubi 
})
print (df)
# Visualizza un grafico a linee
plt.plot (df["Numero"], df["Quadrato"], label="Quadrati")
plt.plot (df["Numero"], df["Cubo"], label="Cubi")       
plt.xlabel("Numero")
plt.ylabel("Valore")    
plt.title("Quadrati e Cubi")
plt.legend()
plt.show()

