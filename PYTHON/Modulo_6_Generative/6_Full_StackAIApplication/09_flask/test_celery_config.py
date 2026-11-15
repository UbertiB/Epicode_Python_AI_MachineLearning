from celery import Celery
import os

try:
    print("Testing sqlite:/// as result backend...")
    app = Celery(backend='sqlite:///test.db')
    print("Backend loaded successfully.")
    print(f"Backend class: {app.backend.__class__.__name__}")
except Exception as e:
    print(f"Failed with sqlite:/// : {e}")

try:
    print("\nTesting db+sqlite:/// as result backend...")
    app = Celery(backend='db+sqlite:///test.db')
    print("Backend loaded successfully.")
    print(f"Backend class: {app.backend.__class__.__name__}")
except Exception as e:
    print(f"Failed with db+sqlite:/// : {e}")

try:
    print("\nTesting sqla+sqlite:/// as broker...")
    app = Celery(broker='sqla+sqlite:///test.db')
    print("Broker loaded successfully.")
except Exception as e:
    print(f"Failed with sqla+sqlite:/// : {e}")
