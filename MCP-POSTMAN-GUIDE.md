# 🚀 Guide d'Utilisation du Serveur MCP Postman

Guide complet pour tester votre API Flask avec le serveur MCP Postman et Bob.

---

## ✅ Installation Terminée

Le serveur MCP Postman est maintenant installé et configuré dans Bob !

### Ce qui a été fait :
- ✅ Package npm installé : `@postman/postman-mcp-server`
- ✅ Configuration MCP ajoutée dans Bob
- ✅ Clé API Postman configurée

---

## 📋 Prochaines Étapes

### Étape 1 : Créer une Collection Postman

1. **Allez sur [Postman](https://www.postman.com/)**
2. **Connectez-vous** avec votre compte
3. **Créez une nouvelle collection** :
   - Cliquez sur "New" → "Collection"
   - Nommez-la : **"Flask API Tests"**

### Étape 2 : Ajouter les Requêtes de Test

Ajoutez ces requêtes à votre collection :

#### 🟢 Health Check
```
Method: GET
URL: http://localhost:8080/api/health
Name: Health Check
```

#### 🟢 Get All Users
```
Method: GET
URL: http://localhost:8080/api/users
Name: Get All Users
```

#### 🟢 Get User by ID
```
Method: GET
URL: http://localhost:8080/api/users/1
Name: Get User by ID
```

#### 🟡 Create User
```
Method: POST
URL: http://localhost:8080/api/users
Name: Create User
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "name": "Test User",
  "email": "test@example.com"
}
```

#### 🟢 Get Stats
```
Method: GET
URL: http://localhost:8080/api/stats
Name: Get Stats
```

### Étape 3 : Sauvegarder la Collection

Cliquez sur **"Save"** pour enregistrer votre collection.

---

## 🎮 Utilisation avec Bob

### Redémarrer Bob

**IMPORTANT :** Vous devez redémarrer Bob pour qu'il charge le nouveau serveur MCP.

1. Fermez complètement Bob
2. Relancez Bob
3. Le serveur MCP Postman sera automatiquement chargé

### Vérifier que le Serveur MCP est Actif

Une fois Bob redémarré, vous devriez voir dans la section "Connected MCP Servers" :
- **postman** (avec les outils disponibles)

---

## 💬 Commandes à Utiliser avec Bob

Une fois votre collection créée et Bob redémarré, vous pouvez utiliser ces commandes :

### Lister vos Collections
```
"Liste mes collections Postman"
"Montre-moi mes workspaces Postman"
```

### Exécuter des Tests
```
"Exécute la requête Health Check de ma collection Flask API Tests"
"Lance le test Get All Users"
"Teste l'endpoint de création d'utilisateur"
```

### Gérer les Collections
```
"Crée une nouvelle collection appelée Tests API"
"Ajoute une requête GET à ma collection"
"Montre-moi les détails de ma collection Flask API Tests"
```

---

## 🔍 Exemple de Workflow Complet

### 1. Démarrer votre API Flask
```bash
cd /Users/mickaelranaivoarisoa/Desktop/bobathon-lab
docker compose up -d
```

### 2. Vérifier que l'API fonctionne
```bash
curl http://localhost:8080/api/health
```

### 3. Utiliser Bob pour Tester
```
Vous : "Exécute le test Health Check de ma collection Flask API Tests"

Bob : *[utilise le serveur MCP Postman]*
      ✅ Health Check réussi
      Status: 200
      Response: {
        "status": "healthy",
        "timestamp": "2025-12-16T14:48:00",
        "service": "Flask Test Server"
      }
```

---

## 🛠️ Outils MCP Postman Disponibles

Le serveur MCP Postman vous donne accès à ces outils :

### Collections
- `getCollections` - Liste toutes vos collections
- `getCollection` - Récupère une collection spécifique
- `createCollection` - Crée une nouvelle collection
- `updateCollection` - Met à jour une collection
- `deleteCollection` - Supprime une collection

### Requêtes
- `getRequests` - Liste les requêtes d'une collection
- `createRequest` - Ajoute une requête à une collection
- `updateRequest` - Modifie une requête
- `deleteRequest` - Supprime une requête

### Workspaces
- `getWorkspaces` - Liste vos workspaces
- `getWorkspace` - Récupère un workspace spécifique
- `createWorkspace` - Crée un nouveau workspace

### Environnements
- `getEnvironments` - Liste vos environnements
- `createEnvironment` - Crée un nouvel environnement
- `updateEnvironment` - Met à jour un environnement

---

## 🎯 Cas d'Usage Avancés

### Test Automatisé Complet
```
"Lance tous les tests de ma collection Flask API Tests et donne-moi un rapport"
```

### Création de Collection Automatique
```
"Crée une collection Postman avec des tests pour tous les endpoints de mon API Flask"
```

### Synchronisation avec le Code
```
"Mets à jour ma collection Postman avec les nouveaux endpoints que j'ai ajoutés"
```

---

## 🐛 Dépannage

### Le serveur MCP ne se charge pas

1. **Vérifiez l'installation :**
```bash
npm list -g @postman/postman-mcp-server
```

2. **Vérifiez la configuration :**
```bash
cat "/Users/mickaelranaivoarisoa/Library/Application Support/IBM Bob/User/globalStorage/ibm.bob-code/settings/mcp_settings.json"
```

3. **Redémarrez Bob complètement**

### Erreur d'authentification Postman

1. Vérifiez que votre clé API est valide sur [Postman API Keys](https://postman.postman.co/settings/me/api-keys)
2. Régénérez une nouvelle clé si nécessaire
3. Mettez à jour le fichier `mcp_settings.json`

### Les requêtes échouent

1. **Vérifiez que votre API Docker est démarrée :**
```bash
docker compose ps
curl http://localhost:8080/api/health
```

2. **Vérifiez les URLs dans Postman :**
   - Utilisez `http://localhost:8080` (pas `http://localhost`)
   - Vérifiez les chemins d'API

---

## 📊 Architecture Complète

```
┌─────────────────────────────────────────┐
│  Vous                                   │
│  "Teste mon API"                        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Bob + MCP Postman                      │
│  - Récupère la collection               │
│  - Exécute les requêtes localement      │
└──────────────┬──────────────────────────┘
               │
               ├─────────────────────────────┐
               │                             │
               ▼                             ▼
┌──────────────────────────┐  ┌─────────────────────────┐
│  Postman Cloud API       │  │  Votre API Flask        │
│  - Stocke collections    │  │  (Docker localhost:8080)│
│  - Renvoie définitions   │  │  - Traite requêtes      │
└──────────────────────────┘  └─────────────────────────┘
```

---

## 🎓 Ressources

- [Documentation Postman MCP Server](https://github.com/postmanlabs/postman-mcp-server)
- [Postman Learning Center](https://learning.postman.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## ✅ Checklist de Démarrage

- [x] Serveur MCP Postman installé
- [x] Configuration MCP ajoutée à Bob
- [x] Clé API Postman configurée
- [ ] Collection Postman créée avec les tests
- [ ] Bob redémarré
- [ ] Premier test exécuté avec succès

---

## 🎉 Prêt à Utiliser !

Votre serveur MCP Postman est maintenant configuré et prêt à l'emploi.

**Prochaine étape :** 
1. Créez votre collection Postman avec les requêtes de test
2. Redémarrez Bob
3. Commencez à tester votre API avec des commandes naturelles !

**Exemple de première commande :**
```
"Liste mes collections Postman"
```

Bonne exploration des capacités de Bob ! 🚀