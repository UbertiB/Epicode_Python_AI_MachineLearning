# per attivare Flask in ascolto sul computer e sulla porta scrivere (in power shell):
# python -m flask --app 09_magazzino3 run --host=120.0.0.61 --port=5000
# dall'URL (es. Chrome) scrivi: http://120.0.0.61:5000/giacenza/ABC1234



from flask import Flask

app = Flask(__name__)

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