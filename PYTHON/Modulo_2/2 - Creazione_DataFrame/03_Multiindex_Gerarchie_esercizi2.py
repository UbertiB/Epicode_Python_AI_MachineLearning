import pandas as pd
import numpy as np

"""
il multiindex è un indice composto da più livelli, serve quando i dati sono gerarchici
"""
#
#CREAZIONE SEMPLICE multiindex (livello0=Citta, livello1=Negozio)
#
print("------------------------------")
print("-----CREAZIONE SEMPLICE-------")
print("------------------------------")
index1=pd.MultiIndex.from_tuples(
    [
        ("Roma","Negozio1"),
        ("Roma","Negozio2"),
        ("Milano","Negozio1")
    ],
    names=["Citta","Negozio"]  #2 livelli
)
print(index1)

#utilizzare multiindex in datafram
df1=pd.DataFrame({"Vendite":[100,150,200]},index=index1)
print(df1)

#
#CREAZIONE DA PRODOTTO CARTESIANO (tutte le combinazioni possibili) 
#utilizzare FROM_PRODUCT
#
print("------------------------------")
print("-----PRODOTTO CARTESIANO------")
print("------------------------------")
citta=["Roma","Milano"]
prodotti=["Pizza","Pasta"]
index2=pd.MultiIndex.from_product([citta,prodotti],names=["Citta","Prodotto"])
print(index2)
df2=pd.DataFrame({"Vendite":np.random.randint(20,200,len(index2))},index=index2)
print(df2)


print("------------------------------")
print("-----SELEZIONARE I DATI------")
print("------------------------------")
#Selezionare dati (.LOC)
#
print(".LOC")
# devo rispettare la gerarchia dei livelli (oppure utilizzare lo slice)
print(f"\nVendite di Milano (.loc): \n{df2.loc[("Milano")]}")
print(f"\nVendite di Milano/Pizza (.loc): \n{df2.loc[("Milano","Pizza")]}")
print(f"\nVendite di Pizza (.loc con slice): \n{df2.loc[pd.IndexSlice[:,"Pizza"],:]}")
print(":XS")
#Selezionare dati (.XS)
print(f"\nVendite di Milano (.xs); \n{df2.xs("Milano",level="Citta")}")
print(f"\nVendite di Pizza (.xs): \n{df2.xs("Pizza",level="Prodotto")}")

#
#MULTIINDIX A 3 LIVELLI
#
print("------------------------------")
print("----MULTIINDEX A 3 LIVELLI----")
print("------------------------------")
citta=["Roma","Milano"]
negozi=["Negozio1","Negozio2"]
prodotti=["Pizza","Pasta"]
index3=pd.MultiIndex.from_product([citta, negozi,prodotti],names=["Citta", "Negozio","Prodotto"])
df3=pd.DataFrame({"Vendite":np.random.randint(20,200,len(index3))},index=index3)
print(f"\nMultiindex a 3 livelli: \n{df3}")
print(f"\nVendite di Milano (.loc): \n{df3.loc[("Milano")]}")
print(f"\nVendite di Milano/Negozio1 (.loc): \n{df3.loc[("Milano","Negozio1")]}")
print(f"\nVendite di Milano/Negozio1/Pizza (.loc): \n{df3.loc[("Milano","Negozio1","Pizza")]}")
print(f"\nVendite Negozio1 (.loc): \n{df3.loc[pd.IndexSlice[:,"Negozio1"],:]}")
print(f"\nVendite Pizza (.loc): \n{df3.loc[pd.IndexSlice[:,:,"Pizza"],:]}")
print(f"\nVendite Pizza (.xs): \n{df3.xs("Pizza",level="Prodotto")}")



