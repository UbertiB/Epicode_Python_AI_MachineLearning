# pip install pandas sqlalchemy pyodbc
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Parametri di connessoine
server   = r"PC03\GAMMA"     
database = "GAMMA_DNP"
user     = "sa"
password = "chianti"

# Scegli driver disponibile: 18 -> 17
drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
if "ODBC Driver 18 for SQL Server" in drivers:
    DRIVER = "{ODBC Driver 18 for SQL Server}"
elif "ODBC Driver 17 for SQL Server" in drivers:
    DRIVER = "{ODBC Driver 17 for SQL Server}"
else:
    raise RuntimeError(f"Nessun driver ODBC 17/18 trovato. Drivers: {drivers}")

# Stringa ODBC 
odbc_str = (
    f"DRIVER={DRIVER};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};PWD={password};"
    "Encrypt=yes;TrustServerCertificate=yes;"
    "Connection Timeout=15;"
)

# SQLAlchemy
conn_url = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)

engine = create_engine(conn_url, fast_executemany=True)

# --- LETTURA ---
print ("-------------")
print ("LETTURA ALL")
print ("-------------")
with engine.connect() as cn:
    df = pd.read_sql(text("SELECT TOP (5) * FROM MG66_ANAGRART ORDER BY MG66_CODART"), cn)
print(df)
print ("-------------")
print ("LETTURA con parametri")
print ("-------------")
with engine.connect() as cn:
    df_param = pd.read_sql(
        text("""
            SELECT *
            FROM dbo.MG66_ANAGRART
            WHERE MG66_CODART BETWEEN :da AND :a
        """),
        cn,
        params={"da": "'000004'", "a": "'0100127430/1'"}  # esempio
    )
print(df_param)



