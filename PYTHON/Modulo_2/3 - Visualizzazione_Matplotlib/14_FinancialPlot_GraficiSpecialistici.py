"""
Financial plot e grafici specialistici

nel campo della finanza i grafici sono importanti strumenti di analisi e supporto decisionale.

LINE CHART:
grafico lineare
mostra il prezzo di chiusura nel tempo, usato molto nel trading, mostra i valori del titolo nel tempo
ma non fornisce dettagli sulle oscillazioni

CANDLESTICK: è il grafico standard nel trading, rappresenta apertura, massimo, minimo e chiusura, ogni
candella rappresenta l'intervallo temporale (giorno, ora, minuto) il corpo della candela varia di colore
a seconda che la chiusura sia supeiore o inferiore rispetto all'apertura

Questi due grafici permettono sia di avere una visione d'insieme sia una visione più dettagliata

OHLC CHART
Simile a candlestick ma usa barre verticali (rappresenta le stesse informazioni). Utile per analizzare volatilità giornaliera
Un trattini a sx indica il prezzo di apertura, uno a dx il prezzo di chiusura, mentre la lunghezza della barra copre massimo e minimo
Molto aprezzato dagli analistici perchè fornisce un colpo d'occhio pulito

Oltre ai grafici i trader utilizzano indicatori matematici per interpretare andamenti di mercato
i più diffusi:
MEDIE MODBILI: linee che smussano i prezzi
RSI oscillatore che misura la forza di un trend e segnala iper comprato o iper venduto
MACD: combina due medie mobili per identificare segnali di inversione
Gli indicatori matematici sono spesos affiancati ai grafici

il VOLUME DI SCAMBI
trend con volumi elevati è considerato più affidabile rispetto ad uno con pochi volumi
VOLUME BAR: mostrano interesse degli operatori
VOLUME PROFILE distribuzione dei volumi per fascia di prezzo

"""

import yfinance as yf
import mplfinance as mpf