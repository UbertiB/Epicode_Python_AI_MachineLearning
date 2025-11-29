import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from Codice1 import Persona
from Codice2 import Saluta

p=Persona("Luca", 25)
print(p.saluta())
print(Saluta())
