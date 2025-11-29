import numpy as np

print("**********************")
print("GENERARE NUMERI CASUALI CON NUMPY")
print("**********************")

print("Diverse funzioni per generare numeri casuali con numpy.random")
#distribuzione uniforme tra 0 e 1
x=np.random.rand(5)  
print(f"Array x con numeri casuali tra 0 e 1 (random.rand): \n{x}")
#distribuzione uniforme tra interi
y=np.random.randint(0,100,size=4)
print(f"Array y con numeri interi casuali tra 0 e 100 con 4 elementi (random.randinit): \n{y}")

#distribuzione normale (gaussiana)
z=np.random.normal(loc=0.0, scale=1.0, size=6)
print(f"Array z con interi casuali tra 0 e 100 (rand.normal): \n{z}")

# Impostare un seed per la riproducibilità
np.random.seed(42)
seed_array=np.random.rand(3)
print(f"Array con seed impostato a 42: \n{seed_array}")

# Generare numeri casuali da una distribuzione specifica (es. binomiale)
binom_array=np.random.binomial(n=10, p=0.5, size=5)
print(f"Array con numeri casuali da distribuzione binomiale (n=10, p=0.5): \n{binom_array}")    
# Generare numeri casuali da una distribuzione specifica (es. poisson)
poisson_array=np.random.poisson(lam=3.0, size=5)
print(f"Array con numeri casuali da distribuzione poisson (lam=3.0): \n{poisson_array}")
print("**********************")

aa=np.random.choice(['apple', 'banana', 'cherry'], size=2)
print(f"Scelta causale tra una lista (random.choice): \n{aa}")   
aar=np.random.choice(['apple', 'banana', 'cherry'], size=2,replace=False)
print(f"Scelta causale tra una lista, senza ripetizione dei dati (random.choice  replace=false): \n{aar}")  

#cambiare ordine di un array
arr2=np.array([1,2,3,4,5])
np.random.shuffle(arr2)
print(f"Array arr2 con elementi mischiati (random.shuffle): \n{arr2}")
print("**********************") 

#ottenere sempre gli stessi numeri casuali impostando il seed (tutte le volte che lancio il programma ho sempre gli stessi numeri casuali)
np.random.seed(123)
fixed_random_numbers=np.random.rand(3)  
print(f"Numeri casuali con seed 123: \n{fixed_random_numbers}")
np.random.seed(123)
fixed_random_numbers2=np.random.rand(3)
print(f"Numeri casuali con seed 123 (seconda volta): \n{fixed_random_numbers2}")    
print("**********************")