"""
LOC
ILOC
QUERY
BOOLEAN INDEXING

Quando si lavora con dataset di piccole dimensioni selezionare righe e/o colonne con la
notazione base di pandas è sufficiente. 
Nel momento in cui ho dataset di grandi dimensioni, questo approccio è insufficiente.
Scrivere df colonna o df 0 3 va bene con pochi dati
Per questo motivo Pandas mette disposizione altri strumenti
- loc
- iloc
- boolen index
- query sintassi tipo SQL
DataFrame: contiene informazioni strutturate su righe (identificate dagli indici) 
e colonne (identificata dalle etichette, nomi delle variabili)
Ogni elemento della tabella ha sempre due coordinate.
Si possono navigare i dati sia per etichetta sia per posizione numerica.

LOC (indicizzazione per etichette)
ci basiamo sulle etichette delle righe e delle colonne indicando i relativi nomi

ILOC (indicizzazione per posizioni numeriche).
Pensiamo ai dati in base al loro contenuto
ci basiamo sulle posizioni numeriche delle righe e delle colonne. Pensiamo ai dati 
in base alla loro posizione
Con iloc, gli indici partono sempre da zero.

BOOLEN INDEX
Consiste nel generare una serie di valori booleani (True False) che Pandas utilizza
come maschera per selezionare i dati corrispondenti. Le condizioni possono essere combinate
tra di loro, per costruire filtri complessi, combinate con & (AND logico), 
con | (OR logico), ^ (NOT negazione). Si applica sia a numeri che a stringhe
Posso costruire cicli precisi senza costruire funzioni

QUERY (sintassi tipo SQL)
Mode alternativo e più leggibile per filtrare i dati, con clausola SQL

TECNICHE DI INDICIZZAZIONE AVANZATA combinate tra di loro
Le tecniche di indicizzazione diventano ancora più potenti quando le combiniamo tra di loro.
Esempio posso utilizzare boolean index per filtrare le righe di interesse e successivamente
applicare loc per selezionare solo alcune colonne specifiche.
Oppure posso utilizzare una query per ridurre il DataFrame e poi restringere ulteriormente
usando iloc per estrarre direttamente righe in base alla loro posizione.

"""
import pandas as pd

#selezione ed ordinamento di BASE
if False:
    df=pd.DataFrame({
                "Nome":["Anna","Luca","Marco","Giulia","Sara","Paolo","Elena"],
                "Eta":[23,25,31,29,22,35,28],
                "Citta":["Roma","Milano","Roma","Torino","Napoli","Roma","Milano"],
                "Spesa":[120,80,150,90,200,130,95]
                 })
    roma=df.loc[(df["Citta"]=="Roma") & (df["Spesa"]>100),["Nome","Eta","Spesa"]]
    roma_ordinato=roma.sort_values(by = "Eta")
    print(roma_ordinato)

    roma_ordinato["Categoria"]=["Alta" if x>125 else "Media" for x in roma_ordinato["Spesa"]]
    print(roma_ordinato)

#selezione con iloc e sliceing
if False:
    df=pd.DataFrame({
                "Nome":["Anna","Luca","Marco","Giulia","Sara","Paolo","Elena"],
                "Eta":[23,25,31,29,22,35,28],
                "Citta":["Roma","Milano","Roma","Torino","Napoli","Roma","Milano"],
                "Spesa":[120,80,150,90,200,130,95]
                 })
    subset=df.iloc[0:4,[1,3]] #prime 4 righe, colonna eta (2) e colonna spesa (4)
    #print(df)
    media=subset.mean()
    minimo=subset.min()
    massimo=subset.max()
    print(f"Subset selezionato: \n{subset}")
    print(f"Statistiche descrittive:\n \nmedia:\n{media} \nminimo:\n{minimo} \nmassimo:\n{massimo}")

#selezione con boolean index con condizioni multiple e stringhe
if False:
    df=pd.DataFrame({
                "Nome":["Anna","Luca","Marco","Giulia","Sara","Paolo","Elena"],
                "Eta":[13,25,31,29,22,35,28],
                "Citta":["Roma","Milano","Roma","Torino","Napoli","Roma","Milano"],
                "Spesa":[120,80,150,90,200,130,95]
                 })    
    filtro=(df["Spesa"]>100)|(df["Nome"].str.startswith("G"))
    risultato=df.loc[filtro,["Nome","Eta","Citta","Spesa"]]
    risultato=risultato.sort_values(by="Spesa",ascending=False)
    risultato["Eta_gruppo"]=["Giovani" if x<30 else "Adulti" for x in risultato["Eta"]]
    print(risultato)

#selezione con query con variabili esterne
if False:
    df=pd.DataFrame({
                "Nome":["Anna","Luca","Marco","Giulia","Sara","Paolo","Elena"],
                "Eta":[13,25,31,29,22,35,28],
                "Citta":["Roma","Milano","Roma","Torino","Napoli","Roma","Milano"],
                "Spesa":[120,80,150,90,200,130,95]
                 }) 
    limite_spesa=100
    citta_esclusa="Milano"     
    risultato=df.query("Spesa > @limite_spesa and Citta != @citta_esclusa")[["Nome","Citta","Spesa"]]
    media_spesa=risultato["Spesa"].mean()
    risultato["Sopra_media"]=risultato["Spesa"]>media_spesa
    print(risultato)

#combinazione avanzata di tutte le tecniche
if True:
    df=pd.DataFrame({
                "Nome":["Anna","Luca","Marco","Giulia","Sara","Paolo","Elena"],
                "Eta":[13,25,31,29,22,35,28],
                "Citta":["Roma","Milano","Roma","Torino","Napoli","Roma","Milano"],
                "Spesa":[120,80,150,90,200,130,95]
                 }) 
    filtro=(df["Spesa"]>90) & (df["Citta"].isin(["Roma","Napoli"]))
    subset=df.loc[filtro,["Nome","Eta","Citta","Spesa"]]
    subset=subset.sort_values(by=["Eta","Spesa"],ascending=[True,False])
    subset["Categoria_spesa"]=["Alta" if x>150 else "Media" for x in subset["Spesa"]]
    media_categoria=subset.groupby("Categoria_spesa")["Spesa"].mean().reset_index()
    print(subset)
    print(f"Media per categoria: \n{media_categoria}")