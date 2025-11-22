"""
definisci una funzione chiamata media che:
* riceve una lista di numeri
* calcola e restituisce la media
"""

def media(numeri:list):
    s=0
    for i in numeri:
        print(i)
        s+=i
    return(s/len(numeri))

print(media([2,4,6]))