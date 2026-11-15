import sys
import os

with open('debug_output.txt', 'w') as f:
    try:
        import sqlalchemy
        f.write(f"SQLAlchemy version: {sqlalchemy.__version__}\n")
    except ImportError as e:
        f.write(f"SQLAlchemy NOT FOUND: {e}\n")

    try:
        import celery
        f.write(f"Celery version: {celery.__version__}\n")
    except ImportError as e:
        f.write(f"Celery NOT FOUND: {e}\n")

    try:
        import kombu
        f.write(f"Kombu version: {kombu.__version__}\n")
    except ImportError as e:
        f.write(f"Kombu NOT FOUND: {e}\n")

    f.write(f"Python: {sys.version}\n")
