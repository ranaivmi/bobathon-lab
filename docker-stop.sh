#!/bin/bash

# Script d'arrêt des services Docker
# Usage: ./docker-stop.sh [--remove-volumes]

set -e

echo "=================================================="
echo "🛑 Arrêt des Services Docker"
echo "=================================================="

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier que Docker est en cours d'exécution
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas en cours d'exécution${NC}"
    exit 1
fi

# Afficher le statut actuel
echo "📊 Statut actuel des services:"
docker compose ps
echo ""

# Options d'arrêt
STOP_ARGS=""
if [ "$1" == "--remove-volumes" ]; then
    echo -e "${RED}⚠️  ATTENTION: Les volumes (base de données) seront supprimés!${NC}"
    read -p "Êtes-vous sûr? (oui/non): " CONFIRM
    if [ "$CONFIRM" != "oui" ]; then
        echo "Opération annulée"
        exit 0
    fi
    STOP_ARGS="-v"
    echo ""
fi

# Arrêter les services
echo "🛑 Arrêt des services en cours..."
docker compose down $STOP_ARGS

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Services arrêtés avec succès!${NC}"
echo "=================================================="
echo ""

if [ "$1" == "--remove-volumes" ]; then
    echo -e "${YELLOW}⚠️  Les volumes ont été supprimés${NC}"
    echo "La base de données sera réinitialisée au prochain démarrage"
else
    echo "💾 Les données ont été préservées"
    echo "Pour supprimer les volumes: ./docker-stop.sh --remove-volumes"
fi

echo ""
echo "📝 Commandes utiles:"
echo "  - Redémarrer:           ./docker-start.sh"
echo "  - Reconstruire:         ./docker-build.sh"
echo "  - Voir les conteneurs:  docker ps -a"
echo "  - Nettoyer le système:  docker system prune"
echo ""

# Made with Bob
