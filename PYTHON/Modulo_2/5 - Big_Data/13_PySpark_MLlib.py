"""
PYSPARK MLlib: PIPELINE E MODELLI BASE DISTRIBUITI

PySpark MLlib è la libreria di machine learning di Spark. In pratica è ML su DataFrame distribuiti, 
con un'API fatta apposta per costruire pipeline ripetibili: preprocessing, modellazione, valutazione,
tunning.
PYSPARK.ML: dataframe based.
1) Si parte da un datafram spark con colonne pulite (colonne con tipo dati corretto, valori coerenti,
   null gestiti, categorie normalizzate e senza 'sporco' che manda in crisi feature engineering).
2) Fai featurization: trasformi testo/categorie/numeri in feature numeriche. le colonne in formato 
   adatto al modello, ad esempio con StringIndexer,  OneHotEncoder, VectorAssembler.
3) Metti tutto in una colonna vettoriale, features (quasi sempre con VectorAssembler). La colonna
   vettoriale conterrà tutte le feature numeriche che il modello usera per fare previsioni.
4) Alleni un Estimator con .fit(df_train). L'estimator è un oggetto che rappresenta un algoritmo 
   di machine learning, ad esempio un classificatore o un regressore. 
   Quando chiami .fit() su un Estimator, Spark esegue il processo di addestramento del modello 
   sui dati di training, restituendo un Transformer che rappresenta il modello addestrato.
5) Applichi .transform(df_test) al modello addestrato per fare previsioni sui dati di test. Il metodo
    .transform() restituisce un nuovo DataFrame con le previsioni del modello, che possono essere 
    confrontate con i valori reali per valutare le prestazioni del modello.
6) Se serve, incapsuli tutto in una Pipeline, che è un oggetto che rappresenta una sequenza di fasi
   di elaborazione dei dati e di modellazione. La Pipeline consente di eseguire tutte le fasi in modo
   sequenziale, semplificando il processo di addestramento e valutazione del modello.

ESTIMATOR: .fit() -> MODELLO: impara dai dati e produce un modello addestrato, che è un Transformer.

TRANSFORMER: .transform() -> DATAFRAME CON PREVISIONI: applica una trasformazione ai dati (con il 
modello addestrato) e restituisce un nuovo DataFrame con le previsoni).

PIPELINE: sequenza di fasi (transformations e modellazione) che possono essere eseguite in modo
sequenziale, semplificando il processo di addestramento e valutazione del modello.

PERSISTENCE: caching e persistenza dei dati in memoria o su disco per migliorare le prestazioni delle
operazioni di machine learning su grandi dataset.

Cosa include MLlib:
- Classificazione e regressione (lineari, alberi ensemple)
- Clustering (es. K-means) e riduzione dimensionale (es. PCA)
- Racommendation: ALS (collaborative filtering) per sistemi di raccomandazione basati su matrice di
interazioni utente-prodotto
- Feature engineering: StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, PCA, ecc

Quando si lavora con lavora con dataset di grandi e distribuiti, applicare tecniche di ml richiede
strumenti progettati per l'elaborazione parallela.
PySpark e MLlib nasce per questo
E' la libreria di machine learning distribuito di Spark, progettata per fare cluster e partizioni senza 
sacrificare la scalabilita.
MLlib ha algoritmi comuni come regressione lineare, classificazione, e clustering, oltre a struementi
per feature engineering, pipeline e touning dei modelli.
L'obbietivo principale è consentire di costruire modelli predittivi su dataset di grandi dimensini.
La pipelne è una sequenza di trasformazioni e modelli applicati ai dati.
in input ha un df e produce un nuovo df con le trasformazioni o le predizzioni.
Questo consente di concatenare in un unico processo tutte le fasi di elaborazione dei dati e di modello.
perrocessing, feature engineering e modellazione
Le pipeline sono fondamentali per mantenere il codice leggibile, riproducibile e facilmente aggiornabile.
consentendo di gestire automaticamente i dati distribuiti tra i nodi.
garantendo che ogni trasformazioni vengano applicate in parallelo alle partizioni del dataset.

Una pipeline MLlib ruota attorno a un'idea: costruire una 'catena' di passi ripetibili che trasformano
i dati e poi allenano/applicano un modello.
Stager, Transformes, Estimators, sono i mattoni di questa catena.
- Hai un DataFrame 'grezzo'
- Fai trasformazioni (pulizia, encoding, feature engineering) 
- Alleni il modello
- Applichi il modello a nuovi dati
Esempio1 
StringIndexer è un estimator, deve 'imparare' la mappatura categorie-indici
dopo .fit() produce StringIndexerModel, un transformer che sa trasformare le categorie in indici.
Esempio2
LogisticRegressoin è un estimator, deve 'imparare' i pesi dei feature 
dopo .fit() produce LogisticRegressionModel, un transformer che sa fare previsioni sui dati nuovi.

TRANSFORMES:
E' un oggetto cha sa fare transform(df), prende in input un DataFrame e restitusce in output un nuovo
DataFrame con una o più colonne in più o modificate.
1) Stages: ogni fase della pipeline è rappresentata da uno stage, che può essere una trasformazione 
   o modelli.
2) Transformers: sono le fasi della pipeline che trasformano i dati, 
   ad esempio StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, PCA, ecc. 
   Questi stage prendono un DataFrame in input e restituiscono un nuovo DataFrame con le 
   trasformazioni applicate.
3) Estimators: sono le fasi della pipeline che rappresentano un algoritmo di machine learning, 
   ad esempio un classificatore o un regressore. 
   Questi stage prendono un DataFrame in input e restituiscono un modello addestrato (un Transformer) 
   quando viene chiamato il metodo .fit(). Producono un modello che può essere utilizzato per 
   predizioni futuri.

MLlib offre un set di modelli base, progettati per operare su dati distribuiti.
1) CLASSIFICAZIONE: obbiettivo prevedere una classe discreta. 
   Algoritmi: 
   - Logistic Regression: modello lineare per classificazione binaria o multiclasse, che stima la
     probabilità di appartenenza a ciascuna classe.
   - Decision Tree: modello ad albero che suddivide i dati in base a feature per prevedere la classe 
     di appartenenza.
   - Random Forest: ensemble di alberi decisionali che migliora la precisione e riduce l'overfitting
     combinando le previsioni di più alberi.
   - Gradient-Boosted Trees (GBT)): ensemble di alberi decisionali che costruisce alberi in modo
     sequenziale, correggendo gli errori dei modelli precedenti per migliorare le prestazioni complessive.
2) REGRESSIONE: obbiettivo prevedere un valore continuo.
    Algoritmi:
    - Linear Regression: modello lineare che stima la relazione tra una variabile dipendente e una o 
      più variabili indipendenti.
    - Decision Tree Regression: modello ad albero che suddivide i dati in base a feature per prevedere
      un valore continuo.
    - Random Forest Regression: ensemble di alberi decisionali che migliora la precisione e riduce
      l'overfitting combinando le previsioni di più alberi.
    - Gradient-Boosted Tress Regression (GBTR): ensemble di alberi decisionali che costruisce alberi
      in modo sequenziale, correggendo gli errori dei modelli precedenti per migliorare le prestazioni
      complessive.
3) CLUSTERING: obbiettivo raggruppare i dati in cluster basati su similarita.
   Algoritmi:
   - K-means: algoritmo di clustering che suddivide i dati in K cluster basati sulla distanza tra i
     punti e i centroidi dei cluster.
   - Gaussian Mixture Models (GMM): algoritmo di clustering che modella i dati come una combinazione
     di distribuzioni gaussiane, consentendo cluster di forma arbitraria e sovrapposti.
   - Bisecting k-means: variante di k-means che suddivide iterativamente i cluster in due, migliorando
     la qualità dei cluster rispetto a k-means standard.
4) RACCOMENDATION: obbiettivo prevedere le preferenze degli utenti basate su interazioni passate.
   Algoritmi:
   - Alternating Least Squares (ALS): algoritmo di collaborative filtering che decomprime la matrice
     di interazioni utente-prodotto in due matrici latenti, una per gli utenti e una per i prodotti,
     consentendo di prevedere le preferenze degli utenti per i prodotti non ancora interagiti.
   - Matrix Factorization: tecnica di decomposizione della matrice che rappresenta le interazioni utente
     prodotto, consentendo di identificare le caratteristiche latenti che influenzano le preferenze
     degli utenti e dei prodotti.
MLlib offre anche strumenti per il tuning dei modelli, come CrossValidator e TrainValidationSplit,
che consentono di eseguire la ricerca degli iperparametri in modo efficiente su grandi dataset distribuiti.
Questi strumenti utilizzano tecniche di validazione incrociata per valutare le prestazioni dei modelli con diverse combinazioni di iperparametri, aiutando a identificare la configurazione ottimale per il modello.

Tutti questi modelli sono utilizzati con spark sfruttando parallelistmo e partizionamento dei dati
per gestire grandi dataset distribuiti, consentendo di costruire modelli predittivi su scala.

Il feature engineering include operazioni come StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, PCA, ecc.
Questi strumenti consentono di trasformare i dati grezzi in feature numeriche che possono
essere utilizzate dai modelli di machine learning. 
Ad esempio, StringIndexer può essere utilizzato per convertire le colonne di testo in indici numerici, 
OneHotEncoder può essere utilizzato per creare variabili dummy da colonne categoriche, 
VectorAssembler può essere utilizzato per combinare più colonne di feature in un'unica colonna vettoriale, 
StandardScaler può essere utilizzato per normalizzare le feature numeriche e PCA può essere utilizzato 
per ridurre la dimensionalità dei dati mantenendo la maggior parte della varianza.
Questi strumenti di feature engineering sono fondamentali per preparare i dati in modo efficace per l
addestramento dei modelli di machine learning, migliorando le prestazioni e la capacità di generalizzazione dei modelli su grandi dataset distribuiti.

Dopo l'addestramento del modello è importante valutare le prestazioni del modello con metriche
appropriate, come accuracy, precision, recall, f1-score per classificazione, e RMSE, MAE, R-squared per regressione.

"""

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler,StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression
import os
from pathlib import Path

HADOOP_HOME = r"C:\hadoop"

# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

#Sessione Spark
spark=SparkSession.builder.appName("MLlib Pipeline").getOrCreate()

#creao DataFrame
data=[(1,10.0,2.0),(2,15.0,3.0),(3,20.0,4.0)]
columns=["id","feature1","feature2"]
df=spark.createDataFrame(data,columns)

if False:

  #REGRESSIONE LINEARE

  #creo un assembler per combinare le feature in un'unica colonna vettoriale
  #con VectorAssembler unisco colonne numeriche in un vettore (perchè ML vuole una
  #singola colonna feature di tipo vettore)
  assembler=VectorAssembler(inputCols=["feature1"], outputCol="features") #ho una sola valriabile in input e devo predirre una seconda variabile
  #se avessi due variabili in input e predirre una terza avrei scritto assembler=VectorAssembler(inputCols=["feature1","feature2"], outputCol="features")

  #standarizzo le feature (porta tutte su scale comparabili) e metto nella colonna scaledFeatures
  #media 0 e varianza 1
  scaler=StandardScaler(inputCol="features", outputCol="scaledFeatures")

  #definisco il modello di regressione lineare: 
  #featurescol sono i dati in input (standarizzato con istruzione precedente)
  #labelcol è la variabile da predire
  lr=LinearRegression(featuresCol="scaledFeatures", labelCol="feature2") #da predire feature2

  #creo una pipeline concatenando gli step: trasformazioni (assembler, scaler) + alleno modello (lr)
  pipeline=Pipeline(stages=[assembler, scaler, lr])

  #alleno il modello con i dati del df applicando tutti gli step della pipeline
  model=pipeline.fit(df)

  #applico il modello per fare previsioni
  predictions=model.transform(df)

  #visualizzo con le righe originali e le predizioni
  predictions.show()


if True:

  #CLASSIFICAZIONE LOGISTICA CON STRINGINDEXER

  #Creo DataFrame
  data=[("rosso",1.0),("blu",0.0),("rosso",1.0),("verde",0.0),("verde",0.0),("verde",0.0)]
  columns=["colore","valore"]
  df=spark.createDataFrame(data,columns)

  #creo un indexer per convertire la colonna colore (categorica) in indici numerici
  indexer=StringIndexer(inputCol="colore", outputCol="coloreIndex")

  #creo un assembler per combinare le feature in un'unica colonna vettoriale
  assembler=VectorAssembler(inputCols=["coloreIndex"], outputCol="features")

  #creo un modello di regressione logistica
  lr=LogisticRegression(featuresCol="features", labelCol="valore")

  #creo una pipeline con le fasi di indexing, assemblaggio e modellazione
  pipeline=Pipeline(stages=[indexer, assembler, lr])

  #alleno il modello con i dati
  model=pipeline.fit(df)

  #applico il modello per fare previsioni
  predictions=model.transform(df)

  #visualizzo
  predictions.show()

  
spark.stop()

#questi esempi non sono buoni esempi per 'classificazione lineare' perchè il dataset, in entrambi
#i casi è minuscolo, e inoltre faccio predizioni sugli stessi dati di trainning. Pertanto si vedranno
#prestazioni quasi 'perfette'


