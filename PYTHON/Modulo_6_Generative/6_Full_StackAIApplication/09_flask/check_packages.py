
try:
    import sqlalchemy
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
except ImportError:
    print("SQLAlchemy IS NOT INSTALLED")

try:
    import celery
    print(f"Celery version: {celery.__version__}")
except ImportError:
    print("Celery IS NOT INSTALLED")

try:
    import kombu
    print(f"Kombu version: {kombu.__version__}")
except ImportError:
    print("Kombu IS NOT INSTALLED")

import sqlite3
print(f"sqlite3 is available: {sqlite3.version}")
