
"""
con il while si ripetono delle istruzioni fino a quando un'istruzione non rimane vera
continua fino a quando vera
- lo usiamo se non sappiamo quante volte andrà ripetuta una o più istruzioni, altrimento uso ciclo FOR
- ha una condizione dinamica
- la eseguo fino a quando la condizione vera non cambia (diventa falsa)
la condizione è valutata prima di ogni giro/iterazione, se falsa il cilo termina subito
se la condizione è subito falsa il ciclo non parte neanche
Evita i loop infiniti ricordandosi di aggiornare la condizione all'iterno del ciclo
in alcuni casi i loop infiniti hanno senso, esempio nei video giochi si inizia con while True
Break termina il ciclo anche se la condizione del ciclo è vera
da utilizzarsi per interrompere il ciclo al verificarsi di un evento
Continue non ferma il ciclo ma salta il resto delle istruzioni e passa all'iterazione successiva
"""
i=1
while i<4:
    print(i)
    i+=1

i=1
print(i)
while i<4:
    if i==2:
        break
    i+=1
    
