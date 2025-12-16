# 🐳 Guide Docker Hub - Push de l'Image Flask API

## 🎯 Vue d'Ensemble

Ce guide explique comment pousser votre image Docker Flask API sur Docker Hub avec le username **ranaivmi**.

---

## ⚡ Quick Start (5 minutes)

### 1️⃣ Se Connecter à Docker Hub

```bash
docker login
```

**Identifiants** :
- Username : `ranaivmi`
- Password : Votre mot de passe Docker Hub

### 2️⃣ Exécuter le Script

```bash
./docker-push.sh
```

**C'est tout !** Le script fait automatiquement :
- ✅ Build de l'image
- ✅ Tag avec `latest` et `1.0.0`
- ✅ Push sur Docker Hub

---

## 📋 Détails du Script

### Ce que Fait `docker-push.sh`

```bash
1. Vérification de Docker
2. Vérification de la connexion Docker Hub
3. Build de l'image (docker-compose build)
4. Tag de l'image :
   - ranaivmi/flask-api:latest
   - ranaivmi/flask-api:1.0.0
5. Push sur Docker Hub
6. Affichage du résumé
```

### Configuration

Le script utilise ces paramètres :

```bash
DOCKER_USERNAME="ranaivmi"
IMAGE_NAME="flask-api"
VERSION="1.0.0"
LOCAL_IMAGE="flask-web-server"
```

---

## 🎨 Utilisation Avancée

### Changer la Version

Éditez `docker-push.sh` :

```bash
VERSION="1.0.0"  # Changez ici
```

Versions recommandées :
- `1.0.0` - Release initiale
- `1.0.1` - Bug fix
- `1.1.0` - Nouvelle feature
- `2.0.0` - Breaking change

### Push Manuel (Sans Script)

```bash
# 1. Build
docker-compose build web-server

# 2. Tag
docker tag flask-web-server ranaivmi/flask-api:latest
docker tag flask-web-server ranaivmi/flask-api:1.0.0

# 3. Push
docker push ranaivmi/flask-api:latest
docker push ranaivmi/flask-api:1.0.0
```

### Tags Multiples

```bash
# Tag pour différents environnements
docker tag flask-web-server ranaivmi/flask-api:dev
docker tag flask-web-server ranaivmi/flask-api:staging
docker tag flask-web-server ranaivmi/flask-api:prod

# Push tous les tags
docker push ranaivmi/flask-api:dev
docker push ranaivmi/flask-api:staging
docker push ranaivmi/flask-api:prod
```

---

## 🚀 Utilisation de l'Image

### Pull depuis Docker Hub

```bash
# Pull latest
docker pull ranaivmi/flask-api:latest

# Pull version spécifique
docker pull ranaivmi/flask-api:1.0.0
```

### Run l'Image

```bash
# Run simple
docker run -d -p 8080:80 ranaivmi/flask-api:latest

# Run avec variables d'environnement
docker run -d \
  -p 8080:80 \
  -e DEBUG=false \
  -e DB_PATH=/data/prod.db \
  -v $(pwd)/data:/data \
  ranaivmi/flask-api:latest

# Run avec docker-compose
version: '3.8'
services:
  api:
    image: ranaivmi/flask-api:latest
    ports:
      - "8080:80"
    environment:
      - DEBUG=false
    volumes:
      - ./data:/data
```

### Tester l'Image

```bash
# 1. Pull et run
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 --name flask-api ranaivmi/flask-api:latest

# 2. Attendre le démarrage (2-3 secondes)
sleep 3

# 3. Tester
curl http://localhost:8080/api/health

# 4. Voir les logs
docker logs flask-api

# 5. Arrêter
docker stop flask-api
docker rm flask-api
```

---

## 🌐 Accès Docker Hub

### Voir Votre Image

```
https://hub.docker.com/r/ranaivmi/flask-api
```

### Statistiques

Docker Hub affiche :
- 📊 Nombre de pulls
- 📅 Date de dernière mise à jour
- 🏷️ Tags disponibles
- 📝 README (si configuré)

---

## 📝 Ajouter un README sur Docker Hub

### Créer un README

Créez `DOCKER-HUB-README.md` :

```markdown
# Flask API

API REST Flask avec Docker, Nginx et SQLite.

## Quick Start

```bash
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 ranaivmi/flask-api:latest
```

Accédez à : http://localhost:8080

## Endpoints

- `GET /api/health` - Health check
- `GET /api/users` - Liste des utilisateurs
- `POST /api/users` - Créer un utilisateur
- `PUT /api/users/:id` - Modifier un utilisateur
- `DELETE /api/users/:id` - Supprimer un utilisateur
- `GET /api/stats` - Statistiques

## Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `NGINX_PORT` | Port Nginx | `80` |
| `DEBUG` | Mode debug | `false` |
| `DB_PATH` | Chemin base de données | `/data/test.db` |

## Volumes

- `/data` - Données persistantes (base SQLite)

## Tests

19 tests automatiques avec Postman.

## Documentation

https://github.com/ranaivmi/flask-api

## Support

Pour toute question : mickael.ranaivoarisoa@gmail.com
```

### Publier le README

1. Aller sur https://hub.docker.com/r/ranaivmi/flask-api
2. Cliquer sur "Edit"
3. Coller le contenu du README
4. Sauvegarder

---

## 🔒 Sécurité

### Token d'Accès (Recommandé)

**Plus sécurisé que le mot de passe !**

```bash
# 1. Créer un token
Docker Hub → Account Settings → Security → New Access Token

# 2. Sauvegarder le token
export DOCKER_TOKEN="dckr_pat_xxxxxxxxxxxxx"

# 3. Se connecter avec le token
echo $DOCKER_TOKEN | docker login -u ranaivmi --password-stdin
```

### Ne Pas Inclure de Secrets

```bash
# ❌ Mauvais - Secrets dans l'image
COPY .env /app/.env

# ✅ Bon - Secrets via variables d'environnement
docker run -e DB_PASSWORD=secret ranaivmi/flask-api:latest
```

### .dockerignore

Assurez-vous que `.dockerignore` exclut :

```
.env
.env.local
*.key
*.pem
secrets/
```

---

## 🔄 Workflow CI/CD

### GitHub Actions

Créez `.github/workflows/docker-push.yml` :

```yaml
name: Docker Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ranaivmi
          password: ${{ secrets.DOCKER_HUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ranaivmi/flask-api:latest
            ranaivmi/flask-api:${{ github.ref_name }}
```

### Automatisation Complète

```bash
# 1. Développement local
./docker-start.sh
# Tests...

# 2. Commit et push
git add .
git commit -m "New feature"
git push origin main

# 3. GitHub Actions
# → Build automatique
# → Push sur Docker Hub
# → Notification

# 4. Déploiement
ssh serveur
docker pull ranaivmi/flask-api:latest
docker-compose up -d
```

---

## 📊 Gestion des Versions

### Stratégie de Versioning

```bash
# Développement
ranaivmi/flask-api:dev

# Staging
ranaivmi/flask-api:staging

# Production
ranaivmi/flask-api:latest
ranaivmi/flask-api:1.0.0
ranaivmi/flask-api:1.0.1
```

### Rollback

```bash
# Si problème avec latest
docker pull ranaivmi/flask-api:1.0.0
docker run -d -p 8080:80 ranaivmi/flask-api:1.0.0
```

---

## 🆘 Dépannage

### Erreur : "denied: requested access to the resource is denied"

**Solution** : Vérifiez que vous êtes connecté

```bash
docker login
```

### Erreur : "no basic auth credentials"

**Solution** : Reconnectez-vous

```bash
docker logout
docker login
```

### Image Trop Grosse

**Solution** : Optimisez le Dockerfile

```dockerfile
# Utilisez alpine
FROM python:3.11-slim-alpine

# Multi-stage build (déjà fait ✅)

# Nettoyez le cache
RUN pip install --no-cache-dir -r requirements.txt
```

### Push Lent

**Solution** : Vérifiez votre connexion internet

```bash
# Test de vitesse
curl -o /dev/null http://speedtest.wdc01.softlayer.com/downloads/test10.zip
```

---

## ✅ Checklist

### Avant le Push

- [ ] Tests passent (19/19)
- [ ] Image build avec succès
- [ ] Pas de secrets dans l'image
- [ ] .dockerignore configuré
- [ ] Version correcte dans le script

### Après le Push

- [ ] Image visible sur Docker Hub
- [ ] Pull fonctionne
- [ ] Run fonctionne
- [ ] Tests passent avec l'image pullée
- [ ] README publié (optionnel)

---

## 🎯 Commandes Rapides

```bash
# Push sur Docker Hub
./docker-push.sh

# Pull et test
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 ranaivmi/flask-api:latest
curl http://localhost:8080/api/health

# Voir les images
docker images | grep flask-api

# Supprimer les anciennes images
docker image prune -a

# Voir les logs
docker logs $(docker ps -q --filter ancestor=ranaivmi/flask-api:latest)
```

---

## 📚 Ressources

- **Docker Hub** : https://hub.docker.com/r/ranaivmi/flask-api
- **Documentation Docker** : https://docs.docker.com
- **Best Practices** : https://docs.docker.com/develop/dev-best-practices/

---

## 🎉 Résumé

**Pour pousser votre image** :

1. `docker login` (une fois)
2. `./docker-push.sh` (à chaque mise à jour)
3. Votre image est disponible sur Docker Hub !

**Pour utiliser l'image** :

```bash
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 ranaivmi/flask-api:latest
```

**Votre image est maintenant accessible depuis n'importe où dans le monde ! 🌍**

---

**Dernière mise à jour** : 16 décembre 2025  
**Version** : 1.0.0  
**Auteur** : Mickael Ranaivoarisoa