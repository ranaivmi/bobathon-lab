#!/bin/bash

# Script de démarrage des services Docker
# Usage: ./docker-start.sh [--build]

set -e

echo "=================================================="
echo "🚀 Démarrage des Services Docker"
echo "=================================================="

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier que Docker est en cours d'exécution
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas en cours d'exécution${NC}"
    echo "Démarrez Docker Desktop ou le daemon Docker"
    exit 1
fi

echo -e "${GREEN}✅ Docker est en cours d'exécution${NC}"
echo ""

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Fichier .env non trouvé${NC}"
    echo "📝 Création du fichier .env depuis .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✅ Fichier .env créé${NC}"
    echo ""
fi

# Options de démarrage
START_ARGS="-d"
if [ "$1" == "--build" ]; then
    START_ARGS="-d --build"
    echo -e "${YELLOW}🔨 Reconstruction des images activée${NC}"
    echo ""
fi

# Afficher les informations
echo "📋 Configuration:"
echo "  - Répertoire: $(pwd)"
echo "  - Date: $(date)"
echo ""

# Démarrer les services
echo "🚀 Démarrage des services..."
docker compose up $START_ARGS

echo ""
echo "⏳ Attente du démarrage des services..."
sleep 5

# Vérifier le statut des services
echo ""
echo "📊 Statut des services:"
docker compose ps

echo ""
echo "🔍 Vérification de la santé des services..."

# Attendre que les services soient healthy
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    FLASK_HEALTH=$(docker compose ps web-server --format json 2>/dev/null | grep -o '"Health":"[^"]*"' | cut -d'"' -f4 || echo "starting")
    NGINX_HEALTH=$(docker compose ps nginx --format json 2>/dev/null | grep -o '"Health":"[^"]*"' | cut -d'"' -f4 || echo "starting")
    
    if [ "$FLASK_HEALTH" == "healthy" ] && [ "$NGINX_HEALTH" == "healthy" ]; then
        echo -e "${GREEN}✅ Tous les services sont opérationnels!${NC}"
        break
    fi
    
    echo -e "${YELLOW}⏳ En attente... (Flask: $FLASK_HEALTH, Nginx: $NGINX_HEALTH)${NC}"
    sleep 2
    ATTEMPT=$((ATTEMPT + 1))
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}⚠️  Timeout: Les services mettent du temps à démarrer${NC}"
    echo "Vérifiez les logs avec: docker compose logs"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Services démarrés avec succès!${NC}"
echo "=================================================="
echo ""
echo "📍 Accès à l'application:"
echo -e "  ${BLUE}🌐 Interface Web:${NC} http://localhost"
echo -e "  ${BLUE}📡 API Health:${NC}    http://localhost/api/health"
echo -e "  ${BLUE}📊 API Stats:${NC}     http://localhost/api/stats"
echo -e "  ${BLUE}👥 API Users:${NC}     http://localhost/api/users"
echo ""
echo "📝 Commandes utiles:"
echo "  - Voir les logs:        docker compose logs -f"
echo "  - Arrêter les services: ./docker-stop.sh"
echo "  - Redémarrer:           docker compose restart"
echo "  - Statut:               docker compose ps"
echo ""

# Test rapide de l'API
echo "🧪 Test rapide de l'API..."
if curl -s -f http://localhost/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API accessible et fonctionnelle${NC}"
else
    echo -e "${YELLOW}⚠️  API pas encore accessible, attendez quelques secondes${NC}"
fi

echo ""

# Made with Bob
