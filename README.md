# devops-pipeline-kit

# Projet ELT - Car Prices 🚗

Ce projet met en place une **pipeline ELT** complète (Extract, Load, Transform) déployée via **Docker Compose**, permettant d’extraire un fichier CSV, de le charger dans **PostgreSQL**, et de planifier ce processus avec **n8n**. Le tout est encapsulé dans des conteneurs Docker pour faciliter la portabilité.

---

## Stack utilisées

| Technologie        | Rôle dans le projet                                               |
| ------------------ | ----------------------------------------------------------------- |
| **Python**         | Scripts d’extraction/chargement via `pandas` + API avec `FastAPI` |
| **FastAPI**        | API REST déclenchant l'import du CSV dans PostgreSQL              |
| **pandas**         | Lecture/chargement du CSV dans un DataFrame                       |
| **SQLAlchemy**     | Connexion entre Python et PostgreSQL, chargement avec `to_sql()`  |
| **PostgreSQL**     | Stockage des données structurées                                  |
| **pgAdmin**        | Interface graphique pour vérifier les tables                      |
| **n8n**            | Orchestration du déclenchement via HTTP POST                      |
| **Docker Compose** | Supervision et mise en réseau des conteneurs                      |

---

## 🛠 Installation

### 1. Pré-requis

* Docker Desktop installé et lancé
* Compte GitHub (pour cloner le dépôt)
* Éditeur de texte

### 2. Cloner le projet

```bash
git clone https://github.com/REPO/nom-du-projet.git
cd nom-du-projet
```

### 3. Ajouter les fichiers nécessaires

* Crée un dossier `datasets` à la racine
* Place un fichier `car_prices.csv` dedans

### 4. Vérifie `.env`

Créer un fichier `.env` à la racine avec :

```env
POSTGRES_PASSWORD=****
POSTGRES_DB=nom_serveur
API_URL=http://api
SYNC_INTERVAL=900
```

### 5. Lancer Docker Compose

```bash
docker compose up --build
```

Les services suivants seront lancés :

* `elt_postgres` → base PostgreSQL
* `elt_pipeline` → API FastAPI
* `elt_pgadmin` → pgAdmin 
* `elt_n8n` → n8n 

### 6. Connexion à pgAdmin (facultatif)

* URL : [http://localhost:5050](http://localhost:5050)
* Email : [admin@admin.com](mailto:admin@admin.com)
* Mot de passe : admin
* Serveur : `elt_postgres` port `5432`

### 7. Utiliser n8n

* [http://localhost:5678](http://localhost:5678)
* Crée un `Schedule Trigger` → `HTTP Request` vers `http://elt_pipeline:8000/load_csv`

---

## Structure du projet

```bash
├── docker-compose.yml            # Orchestration des conteneurs
├── .env                          # Variables d’environnement
├── pipeline/
│   ├── Dockerfile                # Image Python avec FastAPI
│   ├── docker-entrypoint.sh      # Entrée du conteneur pipeline
│   ├── state/                    # Logs CSV
│   └── src/
│       ├── main.py               # Serveur FastAPI + orchestration
│       └── load_csv.py           # Script d’ingestion CSV
├── datasets/
│   └── car_prices.csv            # Donnée source
```

---

## 🔁 Fonctionnement de la pipeline

### Étape 1 : Extraction (E)

* Script : `load_csv.py`
* Bibliothèque : `pandas`
* Lecture du fichier local `/datasets/car_prices.csv`

### Étape 2 : Chargement (L)

* Connexion via `SQLAlchemy`
* Chargement dans PostgreSQL (schéma `public`, table `car_prices`)

### Étape 3 : Transformation (T)

* (Non incluse ici mais faisable via SQL ou dbt si souhaité)

### Étape 4 : Déclenchement manuel/automatisé

* via n8n (`HTTP Request`)
* ou test local via Postman/cURL :

```bash
curl -X POST http://localhost:8000/load_csv
```

---

## ✅ Vérifications et tests

### Logs

Accessible via :

```bash
GET http://localhost:8000/logs
```

### pgAdmin

* Connecte-toi au serveur `elt_postgres`
* Base : `elt_postgreso`
* Table : `public.car_prices`

---

## Résultat attendu

* Une table `car_prices` avec plus de 550k lignes chargée dans PostgreSQL
* Une API accessible pour recharger les données
* Un déclencheur visuel via n8n ou appel API

---

## 📌 Commandes utiles

```bash
docker compose up --build          # Lancer tous les conteneurs
docker compose down                # Stopper les conteneurs
docker exec -it elt_postgres bash # Accès à la base Postgres
docker logs elt_pipeline           # Voir les logs du microservice
```

---

## Avantages de l'architecture 

* Projet à double orchestration python gère le workflow interne & n8n gère la grande orchestration.
* Modularité  : chaque composant est indépendant (microservices).
* Reproductibilité : tout peut être relancé avec une seule commande docker compose up.
* Scalabilité : Enrichir facilement la pipeline avec d’autres étapes ou traitements.

## Améliorations possibles

* 🔹Ajouter un nœud (n8n) PostgreSQL : pour permettre de vérifier que les données sont bien en base
* 🔹Ajout d'une notification automatique par mail, ou discord pour montrer que la pipeline sait notifier 
* 🔹Validation des données avant import
* 🔹Ajout de dbt ou Airflow pour pipeline avancé
* 🔹Export vers un dashboard Looker Studio ou Power BI
