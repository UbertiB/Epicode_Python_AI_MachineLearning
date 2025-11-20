"""
il casting serve per cambiare il tipo di dato
non sempre tipi diversi sono compatibili (esempio se somma stringa con un numero mi genera un errore)
casting implicito: gestito da python esempio int/float=float
casting esplicito: gestito dal programmatore
"""

a=5 #int
b=2.5 #float
c=a+b #7.5 float

x=int(2.9)
print(x)

list("ciao") #["c","i","a","o]  #da stringa a list
print(list)
set([1,1,2,3]) #{1,2,3}    da list a set
tuple([1,2,3]) #(1,2,3)    da list a tuple

#boolean casting
#bool(0) #false
# tutto il resto true
#boll(32) è true
#boll("") false

#
# ERRORI COMUNI
#
#int("ciao") #ho errore

eta=input("quanti anni hai?")
#print(eta+5)   #errore perchè print da sempre un str
print(int(eta)+5)   #ok

#converti da intero a float
n_int=10
n_float=float(n_int)
print(n_int)
print(n_float)

#da float a inter
n_float=9.7
n_int=int(n_float)
print(n_float)
print(n_int)

#da stringa ad intero
n_str="123"
n_int=int(n_str)
print(n_str)

#da stringa a float
num_str="3.15"
num_float=float(num_str)
print(num_float)

#errori di casting
m_str="ciao"
try:
    num_int=int(m_str)
except ValueError:
    print("non puoi convertire 'ciao' in intero")

    
