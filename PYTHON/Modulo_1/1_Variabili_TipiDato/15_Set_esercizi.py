
"""
immagina due corsi universitari corsa A e corso B
vogliamo sapere:
- chi frequenta entrambi
- chi frequenta solo a
- chi frquenta solo b
- chi frequenta almeno un corso
- quanti studenti unici si sono in totale
"""
corsoa={"Marco", "Anna", "Ettore", "Antonio", "Maria"}
corsob={"Marco", "Stefano", "Stefania", "Maria"}
#chi frequenta entrambi i corsi
print(corsoa.intersection(corsob))
#chi frequenta solo a
print(corsoa-corsob)
#chi frequenta solo b
print(corsob-corsoa)
#chi frequenta almeno un corso
print(corsoa.union(corsob))
#quanti studenti ci sono
print(len(corsoa.union(corsob)))