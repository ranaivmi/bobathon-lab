#!/bin/bash
set -e

echo "=================================================="
echo "🐳 Docker Entrypoint - Flask Test Server"
echo "=================================================="

# Afficher les informations de configuration
echo "📋 Configuration:"
echo "  - DB_PATH: ${DB_PATH:-/app/data/test.db}"
echo "  - PORT: ${PORT:-5001}"
echo "  - FLASK_ENV: ${FLASK_ENV:-production}"
echo "  - DEBUG: ${DEBUG:-False}"

# Créer le répertoire de données si nécessaire
DATA_DIR=$(dirname "${DB_PATH:-/app/data/test.db}")
if [ ! -d "$DATA_DIR" ]; then
    echo "📁 Création du répertoire de données: $DATA_DIR"
    mkdir -p "$DATA_DIR"
fi

# Vérifier si la base de données existe
if [ ! -f "${DB_PATH:-/app/data/test.db}" ]; then
    echo "🔧 Initialisation de la base de données..."
    python -c "
from app import init_db
init_db()
print('✅ Base de données initialisée avec succès!')
"
else
    echo "✅ Base de données existante trouvée"
    # Vérifier l'intégrité de la base de données
    if command -v sqlite3 &> /dev/null; then
        echo "🔍 Vérification de l'intégrité de la base de données..."
        if sqlite3 "${DB_PATH:-/app/data/test.db}" "PRAGMA integrity_check;" | grep -q "ok"; then
            echo "✅ Base de données intègre"
        else
            echo "⚠️  Problème d'intégrité détecté dans la base de données"
        fi
    fi
fi

# Afficher les statistiques de la base de données
if [ -f "${DB_PATH:-/app/data/test.db}" ]; then
    DB_SIZE=$(du -h "${DB_PATH:-/app/data/test.db}" | cut -f1)
    echo "📊 Taille de la base de données: $DB_SIZE"
fi

echo "=================================================="
echo "🚀 Démarrage de l'application..."
echo "=================================================="

# Exécuter la commande passée en argument (CMD du Dockerfile)
exec "$@"

# Made with Bob
