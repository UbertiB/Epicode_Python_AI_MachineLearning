
a=10
b=6
if a>b:
    print("maggiore")
elif a==b:
    print("uguale")
else:
    print("minore")

#l'ordine delle condizioni è importante perchè python si ferma al primo vero

#posso verifica condizioni dentro altre, si chiama if annidato
x=15
if x>0:
    if x%2:
        print("pari positivo")


x=-10
if x>=0:
    print("positivo")
else:
    print("negativo")

x=10
b=7
if x>b:
    print("a > b")
elif a==b:
    print("a = b")
else:    
    print("a<b")


