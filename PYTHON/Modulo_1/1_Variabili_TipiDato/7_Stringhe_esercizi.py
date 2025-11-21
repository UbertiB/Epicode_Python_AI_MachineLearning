
"""
* chiedi una frase ed inverti l'ordine delle parole
* controlla se la frase è un polindromo (ignora spazi e maiuscole)
"""

frase=input("Inserisci una frase: ")
print(frase[::-1])

print(f"la '{frase}' è un polindromo: {frase[::-1].strip()==frase.strip()}")
