"""
Una volta analizzati i dati e puliti, devo esportarli per condividerli, archiviarli o passarli ad altri sistemi
Salvare i dati con pandas è semplice
Posso salvare con csv, e Excel (ma anche altri)
csv o Excel sono utilizzati in contesti differenti

CSV semplice file di testo con delimitatore (spesso la , ma si può cambiare)
E'un formato universale che può essere aperto con diversi programmi, esempio
excel, google sheets, database, editor testo
E' un formato leggero, leggibile, portatile, perfetto per scambiare i dati
Per impostazione predefinita Pandas salva l'indice come prima riga, 
ma si può controllare questo comportamento escludendo l'indice con index=false
EXCEL
i files excel possono contenere molti più dati
esempio hanno più fogli, hanno delle formule, tabelle con intestazioni colorate, ecc
Excel può andare bene quando dobbiamo presentare i dati
Excel però è molto più pesante e mono universale rispetto csv (non si apre con tutti i programmi)

"""
import pandas as pd

data={"nome":["Anna","Luca", "Marco"],
        "eta":[23,27,25]}
df=pd.DataFrame(data, index=["a","l","m"])  #indici personalizzati, potrebbe aver senso utilizzare loc

#
# CSV
#
df.to_csv("output.csv",index=True) #tutto il dataframe sul file csv, anche l'indice
df.to_csv("output_noindex.csv",index=False) #senza index
df.to_csv("output_nonomicolonne.csv",header=False) #senza nomi colonne
df.to_csv("output_sep.csv",sep=";")#posso cambiare il separatore con sep=";"
df.to_csv("output_colonne.csv",columns=["eta"])#posso esportare solo alcune colonne

#
#EXCEL
#
df.to_excel("output.xlsx",sheet_name="Dati",index=False)
#salvare in più fogli
data2={"prodotti":["Prodotto A","Prodotto Z", "Prodotto D"],
        "prezzi":[125,200,155]}
df2=pd.DataFrame(data2)
with pd.ExcelWriter("output_multifoglio.xlsx") as documento:
    df.to_excel(documento, sheet_name="Utenti")
    df2.to_excel(documento,sheet_name="prodotti")