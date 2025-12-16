#!/bin/bash

# Script de construction des images Docker
# Usage: ./docker-build.sh [--no-cache]

set -e

echo "=================================================="
echo "🔨 Construction des Images Docker"
echo "=================================================="

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    echo "Installez Docker depuis https://www.docker.com/get-started"
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker et Docker Compose sont installés${NC}"
echo ""

# Options de build
BUILD_ARGS=""
if [ "$1" == "--no-cache" ]; then
    BUILD_ARGS="--no-cache"
    echo -e "${YELLOW}⚠️  Build sans cache activé${NC}"
fi

# Afficher les informations
echo "📋 Informations:"
echo "  - Répertoire: $(pwd)"
echo "  - Date: $(date)"
echo ""

# Construire les images
echo "🔨 Construction de l'image Flask..."
docker compose build $BUILD_ARGS web-server

echo ""
echo "🔨 Pull de l'image Nginx..."
docker compose pull nginx

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Construction terminée avec succès!${NC}"
echo "=================================================="
echo ""
echo "📝 Prochaines étapes:"
echo "  1. Démarrer les services: ./docker-start.sh"
echo "  2. Voir les logs: docker compose logs -f"
echo "  3. Accéder à l'application: http://localhost"
echo ""

# Made with Bob
