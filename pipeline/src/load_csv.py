import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
import time



# ---------------------------------------------------------------------------
CSV_PATH = Path("/datasets/car_prices.csv")       
PG_DSN   = os.environ["PG_DSN"]
print(f"🔗 DSN = {PG_DSN}")
print(f"📁 CSV = {CSV_PATH}")
                
TABLE    = "car_prices"                           
SCHEMA   = "public"                                  # schéma cible
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def main() -> None:
    start = time.time()
    print("⏱️ Début du script load_csv")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"❌ CSV introuvable : {CSV_PATH}")

    print(f"📄 Lecture du CSV {CSV_PATH} …")
    df = pd.read_csv(CSV_PATH)
    print(f"✅ CSV chargé dans le DataFrame : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    print(f"🔗 Connexion à PostgreSQL avec {PG_DSN}")
    engine = create_engine(PG_DSN)

    try:
        df.to_sql(
            name=TABLE,
            con=engine,
            schema=SCHEMA,
            if_exists="replace",  # supprime et recrée la table
            index=False,
            method="multi"
        )
        print(f"🎉 {len(df):,} lignes importées dans {SCHEMA}.{TABLE}")
    except Exception as e:
        print("❌ Erreur lors de l'envoi vers PostgreSQL :", e)
        raise

    print("✅ Fin du script. Durée:", time.time() - start)

if __name__ == "__main__":
    main()