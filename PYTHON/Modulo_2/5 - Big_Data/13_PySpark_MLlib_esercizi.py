"""
ESERCIZIO 1
* Crea un pipeline MLlib su un df distribuito che includa Vector Assembler, StandardScaler
e un modello di regressione logistica. Valuta le predizioni su nuovi dati
ESERCIZIO 2
* Progettare una pipeline con almeno due trasformazioni di feature engineering
su variabili categoriche e numeriche, seguite da un modello di classificazione
k-means
ESERCIZIO 3
* Applica cross-validation distribuita su un dataset di esempio per testare diverse
combinazioni di parametri del modello, misurando l'accurancy o RMSE
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler,StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
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

"""
ESERCIZIO 1
* Crea un pipeline MLlib su un df distribuito che includa Vector Assembler, StandardScaler
e un modello di regressione logistica. Valuta le predizioni su nuovi dati
"""

if False:
#Sessione Spark
    spark=SparkSession.builder.appName("ESERCIZIO 1").getOrCreate()

    #creao DataFrame
    data = [
        (1,10.0,2.0,100.0),
        (2,15.0,3.0,200.0),
        (3,20.0,4.0,320.0),
        (4,22.0,4.3,340.0),
        (5,12.0,2.2,120.0),
        (6,18.0,3.6,260.0),
    ]
    columns=["id","feature1","feature2", "feature3"]
    df=spark.createDataFrame(data,columns)
    df=df.withColumn("label",when(col("feature3")>250,1.0).otherwise(0.0))

    #divido tra df di allenamento e df di predizione
    df_train, df_test = df.randomSplit([0.8,0.2],seed=42)

    #creo un assembler per combinare le feature in un'unica colonna vettoriale
    #con VectorAssembler unisco colonne numeriche in un vettore (perchè ML vuole una
    #singola colonna feature di tipo vettore)
    assembler=VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features") #ho 2 varibili in input e devo predire una terza variabile


    #standarizzo le feature (porta tutte su scale comparabili) e metto nella colonna scaledFeatures
    #media 0 e varianza 1
    scaler=StandardScaler(inputCol="features", outputCol="scaledFeatures")

    #creo un modello di regressione logistica
    lr=LogisticRegression(featuresCol="scaledFeatures", labelCol="label")    

    #creo una pipeline concatenando gli step: trasformazioni (assembler, scaler) + alleno modello (lr)
    pipeline=Pipeline(stages=[assembler, scaler, lr])

    #alleno il modello con i dati del df applicando tutti gli step della pipeline
    model=pipeline.fit(df_train)

    #applico il modello per fare previsioni
    predictions=model.transform(df_test)

    #visualizzo con le righe originali e le predizioni
    predictions.show()  

    spark.stop()


"""
ESERCIZIO 2
* Progettare una pipeline con almeno due trasformazioni di feature engineering
su variabili categoriche e numeriche, seguite da un modello di classificazione
""" 

if False:
  spark=SparkSession.builder.appName("ESERCIZIO 2").getOrCreate()
  #CLASSIFICAZIONE LOGISTICA CON STRINGINDEXER

  #Creo DataFrame
  data=[("Articolo1",1.0),("Articolo2",3.0),("Articolo1",1.0),("Articolo3",5.0),("Articolo3",5.0),("Articolo3",5.0)]
  columns=["articolo","quantita"]
  df=spark.createDataFrame(data,columns)

  #creo un indexer per convertire la colonna articolo (categorica) in indici numerici
  indexer=StringIndexer(inputCol="articolo", outputCol="articoloIndex")

  #creo un assembler per combinare le feature in un'unica colonna vettoriale
  assembler=VectorAssembler(inputCols=["articoloIndex"], outputCol="features")

  #creo un modello di regressione logistica
  lr=LogisticRegression(featuresCol="features", labelCol="quantita")

  #creo una pipeline con le fasi di indexing, assemblaggio e modellazione
  pipeline=Pipeline(stages=[indexer, assembler, lr])

  #alleno il modello con i dati
  model=pipeline.fit(df)

  #applico il modello per fare previsioni
  predictions=model.transform(df)

  #visualizzo
  predictions.show()    
  
  spark.stop()

"""
ESERCIZIO 3
* Applica cross-validation distribuita su un dataset di esempio per testare diverse
combinazioni di parametri del modello, misurando l'accurancy o RMSE
"""
if True:

    spark = SparkSession.builder.appName("ESERCIZIO 3").getOrCreate()

    # dataset di esempio (minimo ma sufficiente per dimostrare CV)
    data = [
        (10.0, 2.0, 100.0),
        (15.0, 3.0, 200.0),
        (20.0, 4.0, 320.0),
        (22.0, 4.3, 340.0),
        (12.0, 2.2, 120.0),
        (18.0, 3.6, 260.0),
        (30.0, 6.1, 520.0),
        (28.0, 5.8, 480.0),
        (16.0, 3.1, 210.0),
        (24.0, 4.9, 360.0),
        (14.0, 2.7, 160.0),
        (26.0, 5.2, 410.0),
    ]
    df = spark.createDataFrame(data, ["feature1","feature2","feature3"])

    # 1) crea label binaria
    df = df.withColumn("label", when(col("feature3") > 250, 1.0).otherwise(0.0))

    # Split train/test
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    # 2) Pipeline: assembler -> scaler -> logistic
    assembler = VectorAssembler(inputCols=["feature1","feature2"], outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)
    clf = LogisticRegression(featuresCol="scaledFeatures", labelCol="label")

    pipeline = Pipeline(stages=[assembler, scaler, clf])

    # 3) Grid parametri
    paramGrid = (
        ParamGridBuilder()
        .addGrid(clf.regParam, [0.0, 0.01, 0.1])
        .addGrid(clf.elasticNetParam, [0.0, 0.5, 1.0])
        .addGrid(clf.maxIter, [10, 50])
        .build()
    )

    # 4) Evaluator accuracy
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="accuracy"
    )

    # 5) CrossValidator
    cv = CrossValidator(
        estimator=pipeline,
        estimatorParamMaps=paramGrid,
        evaluator=evaluator,
        numFolds=3,
        parallelism=2
    )

    cvModel = cv.fit(train_df)

    pred_test = cvModel.transform(test_df)
    acc_test = evaluator.evaluate(pred_test)
    print("Accuracy su test:", acc_test)

    best = cvModel.bestModel.stages[-1]
    print("Best params:",
        "maxIter=", best.getMaxIter(),
        "regParam=", best.getRegParam(),
        "elasticNetParam=", best.getElasticNetParam())

    pred_test.select("feature1","feature2","feature3","label","probability","prediction").show()

    spark.stop()