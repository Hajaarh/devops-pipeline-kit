set -e

# Assure l'écriture dans /datasets
if [ -d /datasets ]; then
  chown -R appuser:appgroup /datasets
fi

# Exécute la vraie commande (python -m src.main)
exec "$@"
