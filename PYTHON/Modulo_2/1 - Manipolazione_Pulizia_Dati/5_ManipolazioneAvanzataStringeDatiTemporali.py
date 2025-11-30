"""
due aspetti fondamentali
- gestione avanzata delle stringhe
- trattamento dei dati temporali
molti dati contengono informazioni testuali che necessità di essere gestiti, 
allo stesso modo, i dati temporali possono generare altre informazioni

GESTIONE DELLE STRINGHE
Le colonne di testo possono contenere errori di battitura, caratteri speciali, dati errati. 
Questi dati possono poi compromettere la successiva fase di analisi e portare a risultati incoerenti
La pulizia delle stringhe consiste in una serie di operazioni che rendono i dati coerenti ed utilizzabili
normalizzazione minuscole/maiuscole, eliminazione di spazzi all inizio o alla fine, 
rimozione caratteri non alfanumerici, uniformazione di categorie.

GESTIONE DELLE DATE (parsing date e resample)
spesso le date non sono salvate in un dato corretto, ma solitamente come stringhe o numeri.
E' importante convertire queste informazioni in un formato temporale.
Poi diventa possibile andare ad applicare operazione di resampling, cioè di ricampionamento
dei dati in base ad un'informazione temporale diversa (esempio per settimana, per mese, per ora, ecc)
Importante per ridurre la variabilità giornaliera e individuare la stagionalità dei dati
Posso trasformare una semplice colonna in uno strumento potento per l'analisi temporale dei dati
Le feature temporali più comuni sono il giorno della settimana, giorno festivo/lavorativo, mese, anno, ora
Le fature temporali possono aiutare anche a rilevare le anomalie.
La creazione di queste variabili è una fase molto importante 

1) uniformare stringhe e date
2) gestire i mancanti nei timestamp
3) controllare consistenza con .info() e describe()

"""

import pandas as pd
import numpy as np

data={"Clienti":["Anna Rossi","LUCA Bianchi","mArTa Verdi"," Paolo Neri   "],
      "Email":["anna@mail.com","lucaa@","marta@test","paolo@gmail.com"],
      "Telefono":["+39 3486789012","345678901","0039-333-222-1111","333 444 555"]
    }
df=pd.DataFrame(data)

#rimuovo spazi inizio e fine stringa, trasformo in minuscolo ogni carattere maiuscolo prima lettera stringa
df["Clienti_puliti"]=df["Clienti"].str.strip().str.title()
#validazione mail controlla se negli elementi delle stringa è presente l'argomento impostato tra le(), restituisce nuova colonna con valori boolenai
# controlla se presente @ e poi dei caratteri generali w+ poi controlla presenza . e poi altri caratteri, se cos' l'email sara considerata valida
df["Email_valide"]=df["Email"].str.contains(r"@\w+\.\w+") #controlla se presente @ con altro \w+ e poi il . ed altro \w+
#estrazione dominio solo qualora ci fosse la @ poi dei caratteri e poi un punto ed altri caratteri
df["Dominio"]=df["Email"].str.extract(r"@(\w+\.\w+)")
#standarizzare n. di teleofno, sostituendo (replace) \d indico tutti i valori numerici con l'accento iniziale tutti i valori non numerici, sostituiti con stringa "" nulla
df["Telefono_pulito"]=df["Telefono"].str.replace(r"[^\d]","",regex=True) # ^\d indico tutti i valori che non (^) sono numerici

print(df)


