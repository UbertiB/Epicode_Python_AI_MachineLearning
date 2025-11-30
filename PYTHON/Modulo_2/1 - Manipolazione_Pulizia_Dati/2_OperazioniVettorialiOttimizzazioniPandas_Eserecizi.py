import numpy as np
import pandas as pd

"""
ESERCIZIO 1:    Crea un dataframe con una colonna di temperature in Celsius e 
                aggiungi una nuova colonna con la conversione in Fahrenheit
"""
dati1={"Celsius": [20.00,22.05,25.03,30.01,28.00]}
pd1=pd.DataFrame(dati1)
pd1["Fahrenheit"]=2 * pd1["Celsius"] * 9/5 + 32
print(pd1)
"""
ESERCIZIO 2:    Hai una colonna con punteggi numerici. 
                Crea una nuova colonna che indichi "promosso" se il punteggio è >= 18 e "Bocciato" altrimenti. 
                Usa np.where()
"""
dati2={"Punteggi":[15,18,14,20,22,8,24]}
pd2=pd.DataFrame(dati2)
pd2["Risultato"]=np.where(pd2["Punteggi"]<=18,"Bocciato","Promosso")
print(pd2)
"""
ESERCIZIO 3:    Hai due colonne "Ore_lavorate" e "Paga_oraria". 
                Crea una nuova colonna che calcoli il salario settimanale applicando un bonus del 10% se le ore sono superiori a 40
"""
dati3={"Ore_lavorate":[38,40,45,35,42,40],
       "Paga_oraria":[18.00,22.05,32.00,40,24.08,32.01]}
pd3=pd.DataFrame(dati3)
pd3["Salario_settimanale"]=np.where(pd3["Ore_lavorate"]<=40,pd3["Ore_lavorate"]*pd3["Paga_oraria"],pd3["Ore_lavorate"]* pd3["Paga_oraria"]*110)
pd3["Bonus_settimanale"]=np.where(pd3["Ore_lavorate"]<=40,0,pd3["Ore_lavorate"]* pd3["Paga_oraria"]*10/100)
print(pd3)