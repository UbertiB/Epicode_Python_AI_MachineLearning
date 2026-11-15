from flask import Flask  #python -m pip install Flask

# per attivare Flask in ascolto sul computer e sulla porta scrivere (in power shell):
# Python -m flask --app 09_magazzino run --host=120.0.0.61 --port=5000
# dall'URL (es. Chrome) scrivi: http://120.0.0.61:5000/giacenza/ABC1234

app = Flask(__name__)

@app.get("/")
def home():
    return "<h1>Magazzino</h1>"

@app.get("/giacenza/ABC1234")
def leggi_giacenza():
    return {"articolo": "ABC123", "giacenza": 120}