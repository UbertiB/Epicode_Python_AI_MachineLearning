
"""
scrivi un programma che:
- ha una variabile eta
- se eta<18 stampa minorenne
- se eta almeno 18 ma meno 65 adulto
- altirmenti anziano
"""

eta=int(input("Quanti anni hai: "))
if eta<18:
    print("Sei minorenne")
elif eta<65:
    print ("adulto")
else:    
    print("anziano")