"""
esercizi funzioni
"""
#rubrica telefonica
#aggiunti un nuovo contatto
#modifica un contatto esistente
#eliminare un contratto
#cerca un contatto per nome
#visualizza tutti i contratti in ordin ealfabetico

rubrica=[] #lista vuota

def aggiunti_contatto(nome, numero=None, email=None):
    contatto={"nome":nome,"numero":numero,"email":email}
    rubrica.append(contatto)
    print(f"Contatto {nome} aggiunto in rubrica.")

def modifica_contatto(nome, numero, email):
    for c in rubrica:
        if c["nome"].lower()==nome.lower():
            if numero: #se ha passato il nuovo numero
                c["numero"]=numero
            if email: #se  ha passato la nuova mail
                c["email"]=email
            print (f"contatto modificato {nome}")
            return
    print("Contatto non trovato: {nome}")

def elimina_contatto(nome):
    for c in rubrica:
        if c["nome"].lower()==nome.lower():
            rubrica.remove(c)
            print(f"contatto eliminato: {nome}")
            return
        
    print("Contratto non trovato: {nome}")

def cerca_contatto(nome):
    for c in rubrica:
        if c["nome"].lower()==nome.lower():
            print(f"Contatto trovato {nome}")
            return
    return("Contatto non trovato")

def mostra_contatti():
    if not rubrica:
        print("rubrica vuota")
    ordinati=sorted(rubrica, key= lambda x:x["nome"].lower())
    for c in ordinati:
        print(rubrica)


aggiunti_contatto("Luca","46546465","luca@tiscali.it")
aggiunti_contatto("LAnna","9999999999999","annaa@gmail.it")
modifica_contatto("Luca","4444644444",'luca@gmail.com')
cerca_contatto("Anna")
elimina_contatto("Anna")
mostra_contatti()



