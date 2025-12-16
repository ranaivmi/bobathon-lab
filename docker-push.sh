#!/bin/bash

# Script de push Docker Hub
# Auteur: Mickael Ranaivoarisoa
# Description: Build, tag et push l'image Flask API sur Docker Hub

set -e  # Arrêter en cas d'erreur

# Configuration
DOCKER_USERNAME="ranaivmi"
IMAGE_NAME="flask-api"
VERSION="1.0.0"
LOCAL_IMAGE="bobathon-lab-web-server"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Docker Hub Push Script - Flask API            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    exit 1
fi

# Vérifier si l'utilisateur est connecté à Docker Hub
echo -e "${YELLOW}🔐 Vérification de la connexion Docker Hub...${NC}"
if ! docker info | grep -q "Username: $DOCKER_USERNAME"; then
    echo -e "${YELLOW}⚠️  Vous n'êtes pas connecté à Docker Hub${NC}"
    echo -e "${BLUE}📝 Connexion à Docker Hub...${NC}"
    docker login
    echo ""
fi

# Build l'image
echo -e "${BLUE}🔨 Build de l'image Docker...${NC}"
docker-compose build web-server
echo -e "${GREEN}✅ Build terminé${NC}"
echo ""

# Tag l'image avec latest
echo -e "${BLUE}🏷️  Tag de l'image avec 'latest'...${NC}"
docker tag $LOCAL_IMAGE $DOCKER_USERNAME/$IMAGE_NAME:latest
echo -e "${GREEN}✅ Tag 'latest' créé${NC}"

# Tag l'image avec la version
echo -e "${BLUE}🏷️  Tag de l'image avec version '$VERSION'...${NC}"
docker tag $LOCAL_IMAGE $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
echo -e "${GREEN}✅ Tag '$VERSION' créé${NC}"
echo ""

# Afficher les images taggées
echo -e "${BLUE}📋 Images taggées:${NC}"
docker images | grep $IMAGE_NAME
echo ""

# Push l'image latest
echo -e "${BLUE}🚀 Push de l'image 'latest' sur Docker Hub...${NC}"
docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
echo -e "${GREEN}✅ Image 'latest' poussée${NC}"
echo ""

# Push l'image avec version
echo -e "${BLUE}🚀 Push de l'image '$VERSION' sur Docker Hub...${NC}"
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
echo -e "${GREEN}✅ Image '$VERSION' poussée${NC}"
echo ""

# Résumé
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ Push Réussi !                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📦 Images disponibles sur Docker Hub:${NC}"
echo -e "   ${YELLOW}docker pull $DOCKER_USERNAME/$IMAGE_NAME:latest${NC}"
echo -e "   ${YELLOW}docker pull $DOCKER_USERNAME/$IMAGE_NAME:$VERSION${NC}"
echo ""
echo -e "${BLUE}🌐 Voir sur Docker Hub:${NC}"
echo -e "   ${YELLOW}https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME${NC}"
echo ""
echo -e "${BLUE}🚀 Pour utiliser l'image:${NC}"
echo -e "   ${YELLOW}docker run -d -p 8080:80 $DOCKER_USERNAME/$IMAGE_NAME:latest${NC}"
echo ""

# Made with Bob
