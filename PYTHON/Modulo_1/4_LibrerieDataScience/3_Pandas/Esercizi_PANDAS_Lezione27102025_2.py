import pandas as pd

studenti_dati={"Nome":["Alice","Marco", "Francesco", "Luca", "Francesco","Giorgia","Maria"],
               "Materia":["Inglese","Fisica","Matematica","Storia","Italiano","Matematica","Fisica"],
               "Voto":[28,22,30,18,20,24,23]}
studenti_df=pd.DataFrame(studenti_dati)
studenti_df.to_csv("Studenti_voti.csv",index=False)
studenti_df=pd.read_csv("Studenti_voti.csv")

#media dei voti per ogni studente
media_per_studente=studenti_df.groupby("Nome")["Voto"].mean().reset_index()
media_per_studente.rename(columns={"Voto":"Media_Studente"},inplace=True)

#media dei voti per materia
media_per_materia=studenti_df.groupby("Materia")["Voto"].mean().reset_index()
media_per_materia.rename(columns={"Voto":"Media_Meteria"},inplace=True)

#studente con media più alta
studente_top=media_per_studente.loc[media_per_studente["Media_Studente"].idxmax()]

analisi_df=studenti_df.merge(media_per_studente, on = "Nome")
analisi_df=studenti_df.merge(media_per_materia, on = "Materia")

analisi_df.to_csv("studenti_analisi.csv",index=False)

print("Media per studnete \n",media_per_studente)
print("Media per materia \n",media_per_materia)
print(f"\nStudente con la media più alta: {studente_top["Nome"]}({studente_top["Media_Studente"]})")


