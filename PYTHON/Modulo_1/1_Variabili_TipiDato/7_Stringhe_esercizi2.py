testo="Python"
#estrarre primo e ultimo carattere
print(f"primo carattere: {testo[0]}, ultimo carattere: {testo[-1]}")

#converti in maiuscolo/minuscolo
testo="ComPuTEr"
print(f"il testo è: {testo}, tutto maiuscolo: {testo.upper()}, solo la prima lettere maiuscola {testo.title},  tutto minuscolo: {testo.lower()}")

#conta quante volte compare una lettera
testo="programmazione"
lettera="a"
conteggio=testo.count(lettera) #COUNT
print(f"nella parola: {testo} la lettera {lettera} compare {conteggio} volte.")

#verifica se una parola inizia/finisce con una lettera specifica
testo="  fantastico "
print(f"{testo.strip().startswith("f")}")
print(f"{testo.strip().endswith("c")}")

#inverti una stringa
testo="parola" 
testo_invertito=testo[::-1]
print(f"l'inverso della parola '{testo}' è '{testo_invertito}'")

#rimuovi spazi inizio/fine
testo="   testo libero con spazi   "
print(f"{testo.strip()}")

#prendi le prime 3 lettere e ripetile per 3 volte
testo="parola"
print(f"la parola '{testo}' ripeto testo '{testo[:3]}' 3 volte: '{testo[:3]*3}'")
