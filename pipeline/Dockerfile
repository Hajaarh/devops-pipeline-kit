##############################################################################
# Build des dépendances 
##############################################################################
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Outils de compilation (désinstallés ensuite pour alléger l’image finale)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential && \
    pip install --upgrade --no-cache-dir pip==24.0 wheel==0.43.*

WORKDIR /tmp

# On ne copie QUE requirements.txt pour profiter du cache Docker
COPY requirements.txt .

# Compilation → roues (.whl) déposées dans /wheels
RUN mkdir /wheels && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt && \
    # Nettoyage
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

##############################################################################
# Étape 2 : runtime minimal
##############################################################################
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /app

# --- installation des roues pré-compilées -----------------------------------
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels            

# --- code de l’application ---------------------------------------------------
COPY src/ ./src
        
# --- script d’entrée (donne les droits sur /datasets) ------------------------
COPY docker-entrypoint.sh /usr/local/bin/entry.sh
RUN chmod +x /usr/local/bin/entry.sh


# -------------------------  point d’entrée  ----------------------------------
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]



# ------------ volumes persistants (état + jeux de données) -------------------
VOLUME ["/app/state", "/datasets"]

