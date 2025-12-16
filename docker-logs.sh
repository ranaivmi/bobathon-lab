#!/bin/bash

# Script pour consulter les logs Docker
# Usage: ./docker-logs.sh [service] [options]
#   service: flask-app, nginx, ou vide pour tous
#   options: -f (follow), --tail=N (dernières N lignes)

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=================================================="
echo "📋 Consultation des Logs Docker"
echo "=================================================="
echo ""

# Vérifier que Docker est en cours d'exécution
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas en cours d'exécution${NC}"
    exit 1
fi

# Déterminer le service et les options
SERVICE=""
OPTIONS=""

# Valider le nom du service
VALID_SERVICES="web-server nginx"

if [ -n "$1" ] && [ "$1" != "-f" ] && [[ ! "$1" =~ ^--tail ]]; then
    if [[ " $VALID_SERVICES " =~ " $1 " ]]; then
        SERVICE="$1"
        shift
    else
        echo -e "${YELLOW}⚠️  Service invalide. Services disponibles: web-server, nginx${NC}"
        exit 1
    fi
fi

OPTIONS="$@"

# Afficher les informations
if [ -z "$SERVICE" ]; then
    echo -e "${BLUE}📊 Logs de tous les services${NC}"
else
    echo -e "${BLUE}📊 Logs du service: $SERVICE${NC}"
fi

if [[ "$OPTIONS" =~ "-f" ]]; then
    echo -e "${YELLOW}⏳ Mode suivi en temps réel (Ctrl+C pour quitter)${NC}"
fi

echo ""
echo "=================================================="
echo ""

# Afficher les logs
if [ -z "$SERVICE" ]; then
    docker compose logs $OPTIONS
else
    docker compose logs $SERVICE $OPTIONS
fi

# Made with Bob
