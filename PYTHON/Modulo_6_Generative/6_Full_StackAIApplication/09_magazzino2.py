from flask import Flask  #python -m pip install Flask

# per attivare Flask in ascolto sul computer e sulla porta scrivere (in power shell):
# python -m flask --app 09_magazzino2 run --host=120.0.0.61 --port=5000
# dall'URL (es. Chrome) scrivi: http://120.0.0.61:5000/giacenza/ABC1234


app = Flask(__name__)

@app.get("/")
def home():
    return "<h1>Magazzino</h1>"

GIACENZE_DI_PROVA = {
    "ABC1234": 120,
    "DEF5678": 0,
}
@app.get("/giacenza/<articolo>")
def leggi_giacenza(articolo):
    giacenza = GIACENZE_DI_PROVA.get(articolo)

    if giacenza is None:
        return {"articolo": articolo, "errore": "Articolo non trovato"}, 404

    return {"articolo": articolo, "giacenza": giacenza}