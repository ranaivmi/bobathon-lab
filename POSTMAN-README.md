# 📮 Postman - Configuration Complète

## 📋 Vue d'Ensemble

Ce dossier contient une configuration Postman complète pour tester votre API Flask avec **plusieurs environnements**.

---

## 📦 Fichiers Disponibles

### 🎯 Collection

| Fichier | Description | Contenu |
|---------|-------------|---------|
| `Flask-API-Tests.postman_collection.json` | Collection de tests API | 7 requêtes avec tests automatiques |

### 🌍 Environnements

| Fichier | Environnement | URL par Défaut |
|---------|---------------|----------------|
| `Local.postman_environment.json` | Local | `http://localhost:8080` |
| `Dev.postman_environment.json` | Dev | `https://dev-api.example.com` |

### 📚 Documentation

| Fichier | Description |
|---------|-------------|
| `POSTMAN-QUICKSTART.md` | Guide de démarrage rapide (2 min) |
| `POSTMAN-ENVIRONMENTS-GUIDE.md` | Guide complet des environnements |
| `POSTMAN-IMPORT-GUIDE.md` | Guide d'import détaillé |
| `MCP-POSTMAN-GUIDE.md` | Utilisation avec Bob (MCP) |

---

## 🚀 Démarrage Rapide

### 1. Importer dans Postman

```bash
# Collection
Postman → Import → Flask-API-Tests.postman_collection.json

# Environnements
Postman → Environments → Import → Local.postman_environment.json
Postman → Environments → Import → Dev.postman_environment.json
```

### 2. Configurer l'URL Dev

```bash
Postman → Environments → Dev → Modifier base_url
```

### 3. Tester

```bash
# Local
Sélectionner "Local" → Run Collection → ✅ 19/19 tests

# Dev
Sélectionner "Dev" → Run Collection → ✅ 19/19 tests
```

---

## 🎯 Requêtes Disponibles

La collection contient **7 requêtes** testées :

| # | Requête | Méthode | Endpoint | Tests |
|---|---------|---------|----------|-------|
| 1 | Health Check | GET | `/api/health` | 3 tests |
| 2 | Get All Users | GET | `/api/users` | 3 tests |
| 3 | Get User by ID | GET | `/api/users/1` | 3 tests |
| 4 | Create User | POST | `/api/users` | 3 tests |
| 5 | Update User | PUT | `/api/users/1` | 2 tests |
| 6 | Get Stats | GET | `/api/stats` | 3 tests |
| 7 | Delete User | DELETE | `/api/users/{id}` | 2 tests |

**Total : 19 tests automatiques** ✅

---

## 🌍 Variables d'Environnement

### Variables Communes

Toutes les requêtes utilisent ces variables :

```javascript
{{base_url}}      // URL de base de l'API
{{environment}}   // Nom de l'environnement
{{api_path}}      // Chemin de base (/api)
{{new_user_id}}   // ID du dernier utilisateur créé (dynamique)
```

### Environnement Local

```json
{
  "base_url": "http://localhost:8080",
  "environment": "local",
  "api_path": "/api"
}
```

### Environnement Dev

```json
{
  "base_url": "https://dev-api.example.com",
  "environment": "dev",
  "api_path": "/api"
}
```

---

## 🔧 Personnalisation

### Ajouter un Nouvel Environnement

**Exemple : Créer un environnement "Staging"**

1. **Dupliquez** `Dev.postman_environment.json`
2. **Renommez** en `Staging.postman_environment.json`
3. **Modifiez** :
   ```json
   {
     "name": "Staging",
     "values": [
       {
         "key": "base_url",
         "value": "https://staging-api.example.com"
       },
       {
         "key": "environment",
         "value": "staging"
       }
     ]
   }
   ```
4. **Importez** dans Postman

### Ajouter des Variables

**Exemple : Ajouter une clé API**

```json
{
  "key": "api_key",
  "value": "votre-cle-secrete",
  "type": "secret",
  "enabled": true
}
```

Utilisez dans vos requêtes :
```
Header: Authorization: Bearer {{api_key}}
```

---

## 📊 Tests Automatiques

### Tests par Requête

Chaque requête inclut des tests JavaScript :

```javascript
// Exemple : Health Check
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has status field", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('status');
    pm.expect(jsonData.status).to.eql('healthy');
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### Exécution des Tests

**Via Postman** :
```bash
Collection → Run → Sélectionner environnement → Start Run
```

**Via Bob (MCP)** :
```bash
"Exécute ma collection Flask API Tests avec l'environnement Local"
```

**Via Newman (CLI)** :
```bash
newman run Flask-API-Tests.postman_collection.json \
  -e Local.postman_environment.json
```

---

## 🎨 Workflow Recommandé

### Développement Local

```bash
1. Démarrer le serveur local
   ./docker-start.sh

2. Sélectionner l'environnement "Local"

3. Développer et tester en continu
   - Modifier le code
   - Exécuter les tests
   - Vérifier les résultats

4. Commit quand tous les tests passent
```

### Déploiement Dev

```bash
1. Push vers la branche dev
   git push origin dev

2. Attendre le déploiement (CI/CD)

3. Sélectionner l'environnement "Dev"

4. Exécuter les tests
   - Vérifier que tout fonctionne
   - Comparer avec Local
   - Valider le déploiement
```

---

## 🔒 Sécurité

### ⚠️ Bonnes Pratiques

**À Faire** ✅ :
- Utilisez `type: "secret"` pour les clés API
- Documentez les variables requises
- Créez un `.env.example` pour les secrets
- Partagez les environnements sans secrets

**À Éviter** ❌ :
- Ne commitez pas les secrets dans Git
- Ne partagez pas vos clés API
- N'utilisez pas les mêmes clés pour tous les environnements

### Fichier .gitignore

```bash
# Environnements avec secrets
*.postman_environment.json
!Local.postman_environment.json
!Dev.postman_environment.json

# Ou créez des versions sans secrets
*-with-secrets.postman_environment.json
```

---

## 🆘 Dépannage

### Problème : Variables non résolues

**Symptôme** : `{{base_url}}` apparaît dans l'URL

**Solution** :
1. Vérifiez qu'un environnement est sélectionné
2. Cliquez sur l'œil 👁️ pour voir les variables
3. Vérifiez que `base_url` existe

### Problème : Tests échouent

**Symptôme** : Certains tests sont rouges ❌

**Solutions** :
1. Vérifiez que le serveur est démarré
2. Vérifiez l'URL de l'environnement
3. Comparez les réponses attendues vs reçues
4. Vérifiez les logs du serveur

### Problème : Import échoue

**Symptôme** : Erreur lors de l'import

**Solutions** :
1. Vérifiez le format JSON (validez sur jsonlint.com)
2. Utilisez Postman Desktop au lieu de Web
3. Essayez d'importer un fichier à la fois

---

## 📚 Documentation Complète

### Guides Disponibles

| Guide | Contenu | Temps de Lecture |
|-------|---------|------------------|
| **POSTMAN-QUICKSTART.md** | Démarrage rapide | 2 min |
| **POSTMAN-ENVIRONMENTS-GUIDE.md** | Guide complet | 10 min |
| **POSTMAN-IMPORT-GUIDE.md** | Import détaillé | 5 min |
| **MCP-POSTMAN-GUIDE.md** | Utilisation avec Bob | 5 min |

### Ordre de Lecture Recommandé

```
1. POSTMAN-QUICKSTART.md        ← Commencez ici !
2. POSTMAN-IMPORT-GUIDE.md      ← Si problème d'import
3. POSTMAN-ENVIRONMENTS-GUIDE.md ← Pour aller plus loin
4. MCP-POSTMAN-GUIDE.md         ← Pour utiliser avec Bob
```

---

## 🎯 Commandes Bob (MCP)

Une fois configuré, utilisez Bob pour automatiser :

```bash
# Lister les collections
"Liste mes collections Postman"

# Exécuter les tests
"Exécute ma collection Flask API Tests"
"Teste mon API avec l'environnement Local"
"Teste mon API avec l'environnement Dev"

# Comparer les résultats
"Compare les performances entre Local et Dev"

# Créer une nouvelle collection
"Crée une collection Postman pour tester l'API GitHub"
```

---

## 📈 Statistiques

### Collection

- **7 requêtes** HTTP
- **19 tests** automatiques
- **100%** de couverture des endpoints
- **~7-8 secondes** d'exécution (Local)

### Environnements

- **2 environnements** préconfigurés
- **3 variables** par environnement
- **Extensible** à l'infini

---

## ✅ Checklist de Configuration

- [ ] Collection importée dans Postman
- [ ] Environnement Local importé
- [ ] Environnement Dev importé
- [ ] URL Dev configurée
- [ ] Tests exécutés sur Local ✅
- [ ] Tests exécutés sur Dev ✅
- [ ] Documentation lue
- [ ] Bob configuré avec MCP Postman (optionnel)

---

## 🎉 Prêt à Utiliser !

Votre configuration Postman est complète et professionnelle :

✅ **Collection** avec variables  
✅ **Environnements** multiples  
✅ **Tests** automatiques  
✅ **Documentation** complète  
✅ **Intégration** Bob (MCP)  

**Bon testing ! 🚀**

---

## 📞 Support

Pour toute question :
1. Consultez les guides dans ce dossier
2. Vérifiez la documentation Postman officielle
3. Demandez à Bob : "Comment utiliser Postman avec ma collection ?"

---

**Dernière mise à jour** : 16 décembre 2025  
**Version** : 1.0.0