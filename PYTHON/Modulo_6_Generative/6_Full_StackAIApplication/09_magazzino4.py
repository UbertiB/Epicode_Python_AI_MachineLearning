# per attivare Flask in ascolto sul computer e sulla porta scrivere (in power shell):
# python -m flask --app 09_magazzino3 run --host=120.0.0.61 --port=5000
# dall'URL (es. Chrome) scrivi: http://120.0.0.61:5000/giacenza/ABC1234



from flask import Flask
from flask import Flask, render_template, request

#template_folder da standard è nella cartella .\templates, 
# con template_folder="." dico che il file templates si trova nella stessa cartella del file .py
app = Flask(__name__, template_folder=".")

ARTICOLI_DI_PROVA = ("ABC1234", "DEF5678")

# Ogni riga contiene il codice articolo e la quantità del movimento.
# Carichi positivi, scarichi negativi.
MOVIMENTI_DI_PROVA = [
    ("ABC1234", 150),
    ("ABC1234", -30),
    ("DEF5678", 25),
    ("DEF5678", -25),
]


def calcola_giacenza(articolo):
    if articolo not in ARTICOLI_DI_PROVA:
        return None

    return sum(
        quantita
        for codice, quantita in MOVIMENTI_DI_PROVA
        if codice == articolo
    )


@app.get("/giacenza/<articolo>")
def leggi_giacenza(articolo):
    giacenza = calcola_giacenza(articolo)

    if giacenza is None:
        return {"articolo": articolo, "errore": "Articolo non trovato"}, 404

    return {"articolo": articolo, "giacenza": giacenza}

@app.get("/")
def pagina_giacenza():
    articolo = request.args.get("articolo", "").strip()
    giacenza = calcola_giacenza(articolo) if articolo else None

    return render_template(
        "09_magazzino.html",
        articolo=articolo,
        giacenza=giacenza,
    )