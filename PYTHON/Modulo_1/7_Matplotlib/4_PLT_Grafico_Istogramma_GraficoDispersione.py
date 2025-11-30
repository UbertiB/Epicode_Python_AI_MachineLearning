import matplotlib.pyplot as plt

#ISTOGRAMMA (guardiamo ad una sola variabile)
dati=[22,25,29,30,32,35,40,41,42,45,46,47,0.5,200]
plt.hist(dati,bins=5,color="skyblue",edgecolor="black")
plt.xlabel("Eta")
plt.ylabel("Frequenza")
plt.title("ISOGRAMMA")
plt.show()

#GRAFICO A DISPERSIONE (guardiamo a due variabili insieme)
#utile per capire se esiste una correlazione tra le due variabili
x=[5,7,8,7,6,9,5,6]
y=[99,86,87,88,100,86,103,87]
plt.scatter(x,y,color="red",marker="o")
plt.title("GRAFICO A DISPERSIONE")
plt.xlabel("Altezza")
plt.ylabel("Peso")
plt.show()

