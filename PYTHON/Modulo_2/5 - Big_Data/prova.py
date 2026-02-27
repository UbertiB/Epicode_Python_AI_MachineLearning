import os
from pathlib import Path

os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

HADOOP_HOME = r"C:\hadoop"
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

# check secco, così non perdi tempo:
assert Path(HADOOP_HOME, "bin", "winutils.exe").exists(), "Manca winutils.exe in C:\\hadoop\\bin"
assert Path(HADOOP_HOME, "bin", "hadoop.dll").exists(), "Manca hadoop.dll in C:\\hadoop\\bin"
