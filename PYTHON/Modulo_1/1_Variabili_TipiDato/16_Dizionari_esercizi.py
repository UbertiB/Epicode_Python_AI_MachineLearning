"""
- crea bìun dizionario che rappresenti uno studente con le chiavi:
nome, eta, corso
- modifica il valore di eta
- aggiungi una nuova chiave matricola
- usa get per recuperare un valore sconosciuto senza errore
- itera su tutte le coppie chiave/valore e stampale
"""

dict={"Nome":"Marco","Eta":35, "Corso":"Matematica"}
dict["Eta"]=45
dict["Matricola"]="4564479846"
print(dict.get("Nome","non presente"))    
print(dict.get("nome","non presente"))    