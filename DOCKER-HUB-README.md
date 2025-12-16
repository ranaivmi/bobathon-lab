# Flask API

API REST Flask professionnelle avec Docker, Nginx et SQLite.

## 🚀 Quick Start

```bash
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 ranaivmi/flask-api:latest
```

Accédez à : **http://localhost:8080**

## 📋 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web |
| `/api/health` | GET | Health check |
| `/api/users` | GET | Liste des utilisateurs |
| `/api/users/:id` | GET | Détails d'un utilisateur |
| `/api/users` | POST | Créer un utilisateur |
| `/api/users/:id` | PUT | Modifier un utilisateur |
| `/api/users/:id` | DELETE | Supprimer un utilisateur |
| `/api/stats` | GET | Statistiques du serveur |

## 🎯 Exemples d'Utilisation

### Health Check

```bash
curl http://localhost:8080/api/health
```

**Réponse** :
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T15:00:00Z"
}
```

### Créer un Utilisateur

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Lister les Utilisateurs

```bash
curl http://localhost:8080/api/users
```

## ⚙️ Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `NGINX_PORT` | Port Nginx | `80` |
| `DEBUG` | Mode debug Flask | `false` |
| `DB_PATH` | Chemin base de données SQLite | `/data/test.db` |

### Exemple avec Variables

```bash
docker run -d \
  -p 8080:80 \
  -e DEBUG=false \
  -e DB_PATH=/data/prod.db \
  -v $(pwd)/data:/data \
  ranaivmi/flask-api:latest
```

## 📦 Volumes

| Volume | Description |
|--------|-------------|
| `/data` | Données persistantes (base SQLite) |

### Exemple avec Volume

```bash
docker run -d \
  -p 8080:80 \
  -v $(pwd)/data:/data \
  ranaivmi/flask-api:latest
```

## 🐳 Docker Compose

```yaml
version: '3.8'

services:
  api:
    image: ranaivmi/flask-api:latest
    ports:
      - "8080:80"
    environment:
      - DEBUG=false
      - DB_PATH=/data/prod.db
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Démarrer :
```bash
docker-compose up -d
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Nginx (Port 80)             │
│  - Reverse Proxy                    │
│  - Compression gzip                 │
│  - Headers de sécurité              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Flask + Gunicorn (Port 5001)   │
│  - API REST                         │
│  - 2 workers                        │
│  - Interface web                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         SQLite Database             │
│  - Stockage persistant              │
│  - Volume /data                     │
└─────────────────────────────────────┘
```

## ✅ Tests

L'API inclut **19 tests automatiques** avec Postman :

- ✅ Health check
- ✅ CRUD utilisateurs
- ✅ Validation des données
- ✅ Gestion des erreurs
- ✅ Performance (< 500ms)

## 🔒 Sécurité

- ✅ Utilisateur non-root dans le conteneur
- ✅ Headers de sécurité Nginx
- ✅ Pas de secrets dans l'image
- ✅ Variables d'environnement pour la config

## 📊 Performance

- **Temps de démarrage** : ~2-3 secondes
- **Temps de réponse** : < 500ms
- **Taille de l'image** : ~150 MB
- **Workers Gunicorn** : 2

## 🏷️ Tags Disponibles

| Tag | Description |
|-----|-------------|
| `latest` | Dernière version stable |
| `1.0.0` | Version 1.0.0 |
| `dev` | Version développement |

## 📚 Documentation

- **GitHub** : https://github.com/ranaivmi/flask-api
- **Guide Docker Hub** : Voir DOCKER-HUB-GUIDE.md
- **Collection Postman** : Incluse dans le repo

## 🛠️ Développement

### Build Local

```bash
git clone https://github.com/ranaivmi/flask-api.git
cd flask-api
docker-compose build
docker-compose up -d
```

### Tests

```bash
# Avec Postman
Importer Flask-API-Tests.postman_collection.json

# Avec curl
curl http://localhost:8080/api/health
```

## 🆘 Support

- **Issues** : https://github.com/ranaivmi/flask-api/issues
- **Email** : mickael.ranaivoarisoa@gmail.com
- **Documentation** : Voir les guides dans le repo

## 📝 Changelog

### v1.0.0 (2025-12-16)
- ✅ Release initiale
- ✅ API REST complète
- ✅ Interface web
- ✅ Docker + Nginx
- ✅ Tests automatiques
- ✅ Documentation complète

## 📄 Licence

MIT License - Voir LICENSE dans le repo

## 👤 Auteur

**Mickael Ranaivoarisoa**
- GitHub: [@ranaivmi](https://github.com/ranaivmi)
- Email: mickael.ranaivoarisoa@gmail.com

---

**⭐ Si vous aimez ce projet, n'hésitez pas à lui donner une étoile sur GitHub !**