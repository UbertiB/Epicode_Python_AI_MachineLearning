"""
l'incapsulamento nasconde i dettagli interni e protegge i dati
la generalizzazione trova caratteristiche comuni tra + classi ed a riunirle in una classe più generale

Incapsulare significa che un oggetto raggruppa i suoi dati e decide quali rendere 
accessibili all'esterno e quali no. Serve per proteggere i dati, modifiche non controllate
e garantire che l'oggetto sia utilizzato in modo corretto.
In python ho diversi livelli di accesso
- publico: variabile ad accesso ovunque
- Protetto: solo per uso interno (_)
- Privato: in nome viene offuscato, name mangling (__)

La generalizzazione individua caratteristiche comuni in più classi e le porta
in una classe "generale". Questo riduce la duplicazione di codice, favorisce
la riusabilità, permette di organizzare le classi in gerarchia logica

"""
#
#incapsulamento
#
class ContoBancario:
    def __init__(self,conto):
        self_saldo=self_saldo
    def deposita(self, importo):
        self._saldo+=importo
    def mostra_saldo(self):
        return self._saldo
conto=ContoBancario(1000)
conto.deposita(100)
print(conto.mostra_saldo())

#
#generalizzazione
#
class Persona:
    def __init__(self,nome):
        self.nome=nome
class Studente(Persona):
    pass
class Docente(Persona):
    pass
#Docente e studente hanno caratteristiche comuni indicate in persona
