# 🐳 Guide Docker - Serveur Flask Test

Documentation complète pour déployer et gérer l'application Flask avec Docker et Docker Compose.

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Architecture](#architecture)
3. [Installation Rapide](#installation-rapide)
4. [Configuration](#configuration)
5. [Commandes Docker](#commandes-docker)
6. [Gestion des Données](#gestion-des-données)
7. [Monitoring et Logs](#monitoring-et-logs)
8. [Dépannage](#dépannage)
9. [Production](#production)

---

## 🎯 Prérequis

### Logiciels Requis

- **Docker** : Version 20.10 ou supérieure
- **Docker Compose** : Version 2.0 ou supérieure

### Vérification de l'Installation

```bash
# Vérifier Docker
docker --version
# Sortie attendue : Docker version 20.10.x ou supérieur

# Vérifier Docker Compose
docker compose version
# Sortie attendue : Docker Compose version v2.x.x ou supérieur
```

### Installation de Docker

**macOS :**
```bash
# Télécharger Docker Desktop depuis https://www.docker.com/products/docker-desktop
# Ou via Homebrew
brew install --cask docker
```

**Linux :**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

---

## 🏗️ Architecture

### Vue d'Ensemble

```
┌─────────────────────────────────────────┐
│    Client (Navigateur / API Client)     │
└──────────────────┬──────────────────────┘
                   │ HTTP :80
                   ▼
┌─────────────────────────────────────────┐
│      Nginx Reverse Proxy Container      │
│      - Load balancing                   │
│      - Gestion des headers              │
│      - Compression gzip                 │
└──────────────────┬──────────────────────┘
                   │ HTTP :5001 (interne)
                   ▼
┌─────────────────────────────────────────┐
│       Flask Application Container       │
│       - Gunicorn (2 workers)            │
│       - API REST                        │
│       - Interface Web                   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      Volume Docker (db-data)            │
│      - SQLite Database persistante      │
│      - /app/data/test.db                │
└─────────────────────────────────────────┘
```

### Services Docker

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| **flask-app** | Custom (Python 3.11) | 5001 (interne) | Application Flask avec Gunicorn |
| **nginx** | nginx:1.25-alpine | 80 (exposé) | Reverse proxy et load balancer |

### Volumes

| Volume | Montage | Description |
|--------|---------|-------------|
| **db-data** | /app/data | Stockage persistant de la base SQLite |
| **nginx-logs** | /var/log/nginx | Logs Nginx |

---

## 🚀 Installation Rapide

### 1. Cloner ou Préparer le Projet

```bash
cd /Users/mickaelranaivoarisoa/Desktop/bobathon-lab
```

### 2. Créer le Fichier de Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer si nécessaire (optionnel)
nano .env
```

### 3. Construire et Démarrer

```bash
# Construire les images
docker compose build

# Démarrer les services
docker compose up -d

# Vérifier le statut
docker compose ps
```

### 4. Vérifier le Déploiement

```bash
# Health check
curl http://localhost/api/health

# Interface web
open http://localhost
```

**✅ Votre application est maintenant accessible sur http://localhost**

---

## ⚙️ Configuration

### Variables d'Environnement

Éditez le fichier `.env` pour personnaliser la configuration :

```bash
# Configuration Flask
FLASK_ENV=production          # production ou development
DEBUG=False                   # True pour activer le mode debug

# Configuration Nginx
NGINX_PORT=80                 # Port exposé (80 par défaut)

# Configuration Base de Données
DB_PATH=/app/data/test.db     # Chemin dans le conteneur

# Configuration Gunicorn
GUNICORN_WORKERS=2            # Nombre de workers
GUNICORN_THREADS=2            # Threads par worker
GUNICORN_TIMEOUT=60           # Timeout en secondes
```

### Mode Développement

Pour activer le hot-reload en développement :

1. Décommenter dans `docker-compose.yml` :
```yaml
volumes:
  - ./app.py:/app/app.py:ro
```

2. Modifier `.env` :
```bash
FLASK_ENV=development
DEBUG=True
```

3. Redémarrer :
```bash
docker compose restart flask-app
```

---

## 🎮 Commandes Docker

### Gestion des Services

```bash
# Démarrer tous les services
docker compose up -d

# Démarrer en mode interactif (voir les logs)
docker compose up

# Arrêter tous les services
docker compose down

# Arrêter et supprimer les volumes
docker compose down -v

# Redémarrer un service spécifique
docker compose restart flask-app
docker compose restart nginx

# Arrêter un service spécifique
docker compose stop flask-app
```

### Construction et Mise à Jour

```bash
# Reconstruire les images
docker compose build

# Reconstruire sans cache
docker compose build --no-cache

# Reconstruire et redémarrer
docker compose up -d --build

# Mettre à jour uniquement Flask
docker compose up -d --build flask-app
```

### Inspection et Debug

```bash
# Voir les logs de tous les services
docker compose logs

# Logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs flask-app
docker compose logs nginx

# Logs des 100 dernières lignes
docker compose logs --tail=100 flask-app

# Voir le statut des services
docker compose ps

# Voir les statistiques de ressources
docker stats

# Inspecter un conteneur
docker inspect flask-test-server
```

### Accès aux Conteneurs

```bash
# Shell interactif dans Flask
docker compose exec flask-app /bin/bash

# Shell interactif dans Nginx
docker compose exec nginx /bin/sh

# Exécuter une commande Python
docker compose exec flask-app python -c "from app import init_db; init_db()"

# Accéder à la base de données SQLite
docker compose exec flask-app sqlite3 /app/data/test.db
```

---

## 💾 Gestion des Données

### Sauvegarde de la Base de Données

```bash
# Méthode 1 : Copier le fichier de la base
docker compose exec flask-app cat /app/data/test.db > backup_$(date +%Y%m%d).db

# Méthode 2 : Export SQL
docker compose exec flask-app sqlite3 /app/data/test.db .dump > backup_$(date +%Y%m%d).sql

# Méthode 3 : Copier depuis le volume
docker cp flask-test-server:/app/data/test.db ./backups/test_$(date +%Y%m%d).db
```

### Restauration de la Base de Données

```bash
# Arrêter l'application
docker compose stop flask-app

# Restaurer depuis un fichier .db
docker cp ./backups/test_20231216.db flask-test-server:/app/data/test.db

# Ou restaurer depuis un export SQL
cat backup_20231216.sql | docker compose exec -T flask-app sqlite3 /app/data/test.db

# Redémarrer
docker compose start flask-app
```

### Réinitialiser la Base de Données

```bash
# Supprimer le volume de données
docker compose down -v

# Redémarrer (recrée la base)
docker compose up -d
```

### Inspecter les Volumes

```bash
# Lister les volumes
docker volume ls

# Inspecter le volume de données
docker volume inspect bobathon-lab_db-data

# Voir l'espace utilisé
docker system df -v
```

---

## 📊 Monitoring et Logs

### Health Checks

```bash
# Vérifier la santé de Flask
curl http://localhost/api/health

# Vérifier la santé via Docker
docker compose ps
# Les services doivent afficher "healthy"

# Statistiques de l'application
curl http://localhost/api/stats | python3 -m json.tool
```

### Logs

```bash
# Tous les logs en temps réel
docker compose logs -f

# Logs Flask uniquement
docker compose logs -f flask-app

# Logs Nginx uniquement
docker compose logs -f nginx

# Logs avec timestamps
docker compose logs -f --timestamps

# Filtrer les logs par niveau
docker compose logs flask-app | grep ERROR
docker compose logs nginx | grep "HTTP/1.1\" 5"
```

### Métriques de Performance

```bash
# Statistiques en temps réel
docker stats

# Utilisation des ressources par service
docker compose top

# Espace disque utilisé
docker system df

# Détails des volumes
docker system df -v
```

### Monitoring Continu

Créer un script `monitor-docker.sh` :

```bash
#!/bin/bash
while true; do
    echo "=== $(date) ==="
    docker compose ps
    curl -s http://localhost/api/health | python3 -m json.tool
    echo ""
    sleep 60
done
```

---

## 🐛 Dépannage

### Problèmes Courants

#### 1. Les conteneurs ne démarrent pas

**Diagnostic :**
```bash
docker compose ps
docker compose logs
```

**Solutions :**
```bash
# Reconstruire les images
docker compose build --no-cache

# Vérifier les ports
lsof -i :80
lsof -i :5001

# Nettoyer et redémarrer
docker compose down
docker compose up -d
```

#### 2. Port 80 déjà utilisé

**Solution :**
```bash
# Modifier le port dans .env
echo "NGINX_PORT=8080" >> .env

# Redémarrer
docker compose down
docker compose up -d

# Accéder via http://localhost:8080
```

#### 3. Erreur de base de données

**Diagnostic :**
```bash
docker compose exec flask-app sqlite3 /app/data/test.db "PRAGMA integrity_check;"
```

**Solutions :**
```bash
# Restaurer depuis une sauvegarde
docker compose stop flask-app
docker cp ./backups/test_latest.db flask-test-server:/app/data/test.db
docker compose start flask-app

# Ou réinitialiser
docker compose down -v
docker compose up -d
```

#### 4. Nginx retourne 502 Bad Gateway

**Diagnostic :**
```bash
docker compose logs nginx
docker compose logs flask-app
docker compose ps
```

**Solutions :**
```bash
# Vérifier que Flask est healthy
docker compose ps

# Redémarrer Flask
docker compose restart flask-app

# Attendre que Flask soit prêt
sleep 10
curl http://localhost/api/health
```

#### 5. Performances lentes

**Diagnostic :**
```bash
docker stats
docker compose exec flask-app sqlite3 /app/data/test.db "SELECT COUNT(*) FROM users;"
```

**Solutions :**
```bash
# Optimiser la base de données
docker compose exec flask-app sqlite3 /app/data/test.db "VACUUM;"

# Augmenter les workers Gunicorn dans .env
echo "GUNICORN_WORKERS=4" >> .env
docker compose up -d --build flask-app
```

### Nettoyage

```bash
# Nettoyer les conteneurs arrêtés
docker container prune

# Nettoyer les images non utilisées
docker image prune

# Nettoyer les volumes non utilisés
docker volume prune

# Nettoyage complet (ATTENTION : supprime tout)
docker system prune -a --volumes
```

---

## 🚀 Production

### Checklist de Déploiement

- [ ] Désactiver le mode debug (`DEBUG=False`)
- [ ] Configurer `FLASK_ENV=production`
- [ ] Ajuster le nombre de workers Gunicorn
- [ ] Configurer SSL/HTTPS sur Nginx
- [ ] Mettre en place des sauvegardes automatiques
- [ ] Configurer un monitoring externe
- [ ] Limiter les ressources des conteneurs
- [ ] Configurer les logs rotatifs
- [ ] Tester la procédure de restauration

### Configuration SSL (Optionnel)

1. Obtenir des certificats SSL (Let's Encrypt recommandé)

2. Modifier `nginx/conf.d/flask-app.conf` :
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... reste de la configuration
}
```

3. Monter les certificats dans `docker-compose.yml` :
```yaml
nginx:
  volumes:
    - ./ssl:/etc/nginx/ssl:ro
```

### Limiter les Ressources

Ajouter dans `docker-compose.yml` :

```yaml
flask-app:
  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 512M
      reservations:
        cpus: '0.5'
        memory: 256M
```

### Sauvegardes Automatiques

Créer un cron job :

```bash
# Éditer crontab
crontab -e

# Ajouter (sauvegarde quotidienne à 2h)
0 2 * * * cd /path/to/project && docker compose exec -T flask-app sqlite3 /app/data/test.db .dump > backups/backup_$(date +\%Y\%m\%d).sql
```

---

## 📚 Ressources Supplémentaires

### Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

### Commandes Utiles

```bash
# Voir toutes les images
docker images

# Voir tous les conteneurs (même arrêtés)
docker ps -a

# Voir tous les volumes
docker volume ls

# Voir tous les réseaux
docker network ls

# Informations système Docker
docker info

# Version de Docker
docker version
```

---

## 🆘 Support

### Logs de Debug

En cas de problème, collectez ces informations :

```bash
# Informations système
docker version
docker compose version

# État des services
docker compose ps

# Logs complets
docker compose logs > debug_logs.txt

# Configuration
docker compose config

# Inspection des conteneurs
docker inspect flask-test-server > flask_inspect.txt
docker inspect flask-nginx-proxy > nginx_inspect.txt
```

---

## 📝 Notes Importantes

- **Persistance** : Les données SQLite sont stockées dans un volume Docker et persistent entre les redémarrages
- **Sécurité** : L'application Flask n'est pas directement exposée, uniquement via Nginx
- **Performance** : Gunicorn utilise 2 workers par défaut, ajustez selon vos besoins
- **Développement** : Utilisez le mode développement uniquement en local
- **Production** : Suivez la checklist de production avant tout déploiement

---

**Version** : 1.0  
**Dernière mise à jour** : 16 décembre 2025  
**Auteur** : Bob