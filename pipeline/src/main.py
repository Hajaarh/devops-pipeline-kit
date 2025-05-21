"""
Boucle d’orchestration locale :
1. Charge le CSV présent dans /datasets (src.load_csv.main)
2. Enrichit avec l’API VPIC (src.fetch_api.main)
Répète toutes les SYNC_INTERVAL secondes.
"""

import os
import time
import importlib
import traceback
from fastapi import FastAPI
import subprocess
from threading import Thread

app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "API de pipeline opérationnelle ✅"}

@app.post("/load_csv")
async def load_csv():
    def background_task():
        run_loader()  # ton chargement CSV
    Thread(target=background_task).start()
    return {"status": "started", "message": "Chargement CSV en arrière-plan"}


@app.get("/logs")
def get_logs():
    try:
        with open("state/load_csv.log", "r") as f:
            return {"logs": f.read()}
    except FileNotFoundError:
        return {"logs": "Aucun log pour le moment."}

def run_loader():
    try:
        result = subprocess.run(["python", "-m", "src.load_csv.py"], capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "output": e.stderr
        }

INTERVAL = int(os.getenv("SYNC_INTERVAL", 900))

# Ordre d’exécution des sous-étapes
WORKFLOW = [
    "src.load_csv",     # charge le CSV local dans raw.vehicle_sales
    
]

def run(module_name: str) -> None:
    """importe dynamiquement le module et appelle sa fonction main()"""
    print(f"▶ {module_name}")
    mod = importlib.import_module(module_name)
    if not hasattr(mod, "main"):
        raise AttributeError(f"{module_name} ne possède pas de fonction main()")
    mod.main()

if __name__ == "__main__":
    while True:
        for step in WORKFLOW:
            try:
                run(step)
            except Exception as exc:
                print(f"❌ erreur dans {step} :", exc)
                traceback.print_exc()
        print(f"✓ cycle terminé — sleep {INTERVAL}s")
        time.sleep(INTERVAL)
