# 🚀 Instructions pour Pousser sur Docker Hub

## ⚠️ Action Requise : Connexion Docker Hub

Vous devez vous connecter à Docker Hub avant de pousser l'image.

---

## 📋 Étapes à Suivre

### 1️⃣ Se Connecter à Docker Hub

Ouvrez un terminal et exécutez :

```bash
docker login
```

**Entrez vos identifiants** :
```
Username: ranaivmi
Password: [votre mot de passe Docker Hub]
```

**Confirmation attendue** :
```
Login Succeeded
```

---

### 2️⃣ Exécuter le Script de Push

Une fois connecté, exécutez :

```bash
./docker-push.sh
```

**Le script va** :
1. ✅ Vérifier la connexion Docker Hub
2. ✅ Build l'image Flask
3. ✅ Tag avec `ranaivmi/flask-api:latest`
4. ✅ Tag avec `ranaivmi/flask-api:1.0.0`
5. ✅ Push sur Docker Hub
6. ✅ Afficher le résumé

**Durée estimée** : 2-3 minutes

---

## 🔑 Si Vous N'avez Pas de Compte Docker Hub

### Créer un Compte (Gratuit)

1. Aller sur : https://hub.docker.com/signup
2. Remplir le formulaire :
   - Username : `ranaivmi`
   - Email : Votre email
   - Password : Choisir un mot de passe
3. Vérifier votre email
4. Revenir à l'étape 1 ci-dessus

---

## 🔒 Utiliser un Token (Plus Sécurisé)

### Créer un Token d'Accès

1. Aller sur : https://hub.docker.com/settings/security
2. Cliquer sur "New Access Token"
3. Nom : `flask-api-push`
4. Permissions : `Read, Write, Delete`
5. Copier le token (il ne sera affiché qu'une fois !)

### Se Connecter avec le Token

```bash
docker login -u ranaivmi -p [VOTRE_TOKEN]
```

Ou de manière plus sécurisée :

```bash
echo "[VOTRE_TOKEN]" | docker login -u ranaivmi --password-stdin
```

---

## 📊 Après le Push

### Vérifier sur Docker Hub

Votre image sera visible sur :
```
https://hub.docker.com/r/ranaivmi/flask-api
```

### Tester le Pull

```bash
# Pull l'image
docker pull ranaivmi/flask-api:latest

# Run l'image
docker run -d -p 8080:80 ranaivmi/flask-api:latest

# Tester
curl http://localhost:8080/api/health
```

**Réponse attendue** :
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T15:00:00Z"
}
```

---

## 🎯 Commandes Complètes

### Workflow Complet

```bash
# 1. Connexion
docker login

# 2. Push
./docker-push.sh

# 3. Vérification
docker pull ranaivmi/flask-api:latest
docker run -d -p 8080:80 --name test-api ranaivmi/flask-api:latest
sleep 3
curl http://localhost:8080/api/health

# 4. Nettoyage
docker stop test-api
docker rm test-api
```

---

## 🆘 Dépannage

### Erreur : "denied: requested access to the resource is denied"

**Cause** : Pas connecté ou mauvais identifiants

**Solution** :
```bash
docker logout
docker login
```

### Erreur : "no basic auth credentials"

**Cause** : Session expirée

**Solution** :
```bash
docker login
```

### Erreur : "unauthorized: incorrect username or password"

**Cause** : Identifiants incorrects

**Solution** :
1. Vérifier le username : `ranaivmi`
2. Vérifier le mot de passe
3. Ou utiliser un token d'accès

---

## ✅ Checklist

- [ ] Compte Docker Hub créé (si nécessaire)
- [ ] Connecté avec `docker login`
- [ ] Script exécuté : `./docker-push.sh`
- [ ] Image visible sur Docker Hub
- [ ] Test pull réussi
- [ ] Test run réussi

---

## 📞 Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. Vérifiez que Docker est installé : `docker --version`
2. Vérifiez la connexion : `docker info | grep Username`
3. Consultez les logs : `docker-push.sh` affiche des messages détaillés
4. Consultez DOCKER-HUB-GUIDE.md pour plus de détails

---

## 🎉 Une Fois Terminé

Votre image sera accessible depuis n'importe où :

```bash
# N'importe qui peut pull votre image
docker pull ranaivmi/flask-api:latest

# Et la run
docker run -d -p 8080:80 ranaivmi/flask-api:latest
```

**Votre API sera déployable en une seule commande ! 🚀**

---

**Prêt ?** Exécutez maintenant :

```bash
docker login
./docker-push.sh