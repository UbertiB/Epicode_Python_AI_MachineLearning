import celery.app.backends
from kombu.utils.imports import symbol_by_name

print("Celery Result Backend Aliases:")
for alias, name in celery.app.backends.aliases.items():
    print(f"  {alias} -> {name}")

import kombu.transport
print("\nKombu Transport Aliases:")
for alias, name in kombu.transport.TRANSPORT_ALIASES.items():
    print(f"  {alias} -> {name}")
