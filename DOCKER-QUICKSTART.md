# 🚀 Démarrage Rapide Docker

Guide ultra-rapide pour démarrer l'application Flask avec Docker.

## ⚡ En 3 Commandes

```bash
# 1. Construire les images
./docker-build.sh

# 2. Démarrer les services
./docker-start.sh

# 3. Accéder à l'application
open http://localhost
```

## 📋 Prérequis

- Docker Desktop installé et en cours d'exécution
- Port 80 disponible (ou modifier NGINX_PORT dans .env)

## 🎯 Commandes Essentielles

```bash
# Démarrer
./docker-start.sh

# Arrêter
./docker-stop.sh

# Voir les logs
./docker-logs.sh -f

# Reconstruire
./docker-build.sh --no-cache
```

## 🔗 URLs Importantes

- **Interface Web** : http://localhost:8080
- **API Health** : http://localhost:8080/api/health
- **API Users** : http://localhost:8080/api/users
- **API Stats** : http://localhost:8080/api/stats

> **Note** : Le port 8080 est utilisé pour éviter les conflits avec un éventuel Nginx système sur le port 80.

## 📊 Vérifier le Statut

```bash
# Statut des conteneurs
docker compose ps

# Logs en temps réel
docker compose logs -f

# Statistiques
curl http://localhost/api/stats | python3 -m json.tool
```

## 🛠️ Dépannage Rapide

### Changer le port ?
```bash
# Le port par défaut est 8080 (pour éviter les conflits)
# Pour utiliser un autre port, modifiez .env
echo "NGINX_PORT=3000" >> .env
docker compose down
docker compose up -d
# Accéder via http://localhost:3000
```

### Réinitialiser tout ?
```bash
./docker-stop.sh --remove-volumes
./docker-start.sh --build
```

### Voir les erreurs ?
```bash
docker compose logs flask-app
docker compose logs nginx
```

## 📚 Documentation Complète

Pour plus de détails, consultez [README-DOCKER.md](README-DOCKER.md)

## 🎉 C'est Tout !

Votre application Flask est maintenant conteneurisée et prête à l'emploi !