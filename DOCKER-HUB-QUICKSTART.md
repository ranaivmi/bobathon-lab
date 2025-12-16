# 🚀 Docker Hub Quick Start

## ⚡ Push sur Docker Hub (2 minutes)

### Étape 1 : Se Connecter

```bash
docker login
```

**Identifiants** :
- Username : `ranaivmi`
- Password : Votre mot de passe Docker Hub

### Étape 2 : Exécuter le Script

```bash
./docker-push.sh
```

**C'est tout !** ✅

---

## 📦 Résultat

Votre image est maintenant disponible sur :

```
https://hub.docker.com/r/ranaivmi/flask-api
```

### Pull l'Image

```bash
docker pull ranaivmi/flask-api:latest
```

### Run l'Image

```bash
docker run -d -p 8080:80 ranaivmi/flask-api:latest
```

### Tester

```bash
curl http://localhost:8080/api/health
```

---

## 🎯 Commandes Utiles

```bash
# Voir les images locales
docker images | grep flask-api

# Voir les tags sur Docker Hub
docker search ranaivmi/flask-api

# Pull une version spécifique
docker pull ranaivmi/flask-api:1.0.0

# Supprimer les anciennes images locales
docker image prune -a
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **DOCKER-HUB-GUIDE.md** : Guide complet
- **DOCKER-HUB-README.md** : README pour Docker Hub

---

## ✅ Checklist

- [ ] Connecté à Docker Hub (`docker login`)
- [ ] Script exécuté (`./docker-push.sh`)
- [ ] Image visible sur Docker Hub
- [ ] Test pull réussi
- [ ] Test run réussi

**Votre image est en ligne ! 🎉**