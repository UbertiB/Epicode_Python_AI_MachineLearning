"""
scrivi un programma che analizza un testo e calcola varie statistiche
conta numero totali di parole
calcolare la frequenza di ogni parola
estrarre le parole uniche 
lunghezza media parole
"""
def pulisci_testo(testo:str):
    simboli=",.;:!?" #simboli da rimuovere
    for s in simboli:
        testo=testo.replace(s,'')
    return testo.strip().lower()

def conta_parole(testo:str):
    parole=testo.split()
    return len(parole)

def frequenza_parole(testo:str):
    parole=testo.split()
    freq={} #dizionario vuoto
    for p in parole:
        freq[p]=freq.get(p,0)+1
    return freq

def parole_uniche(freq):
    return set(freq.keys())

def top_n_parole(freq, n=5):
    return sorted(freq.items(),key=lambda x:x[1],reverse=True)[:n]

def lunghezza_media(freq):
    tot_caratteri=sum(len((p) * occ for p,occ in freq.items()))
    totale_parole=sum(freq.velues())
    return tot_caratteri/totale_parole

testo="""python è un linguaggio di programmazione molto potente
python è utilizzato per analisi dei dati, e sviluppo web
studiare python è divertente."""

pulito=pulisci_testo(testo)
print(pulito)
print(f"numero di parole: {conta_parole(pulito)}")
freq=frequenza_parole(pulito)
print (f"la frequenza delle parole è: {freq}")
print (f"parole uniche: {parole_uniche(freq)}")
print (f"top 5 parole: {top_n_parole(freq,5)}")
print (f"lunghezza media parole: {lunghezza_media(freq)} ")

    

