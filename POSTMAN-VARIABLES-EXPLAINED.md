# 🔧 Variables Postman - Explication Complète

## 🤔 Quelle est la Différence ?

### 📦 Variables de Collection vs 🌍 Variables d'Environnement

| Aspect | Variables de Collection | Variables d'Environnement |
|--------|------------------------|---------------------------|
| **Portée** | Toute la collection | Sélection manuelle |
| **Changement** | Modifier la collection | Changer d'environnement (1 clic) |
| **Usage** | Valeurs par défaut | Valeurs spécifiques à l'env |
| **Priorité** | Basse | Haute (écrase la collection) |
| **Exemple** | `api_path: /api` | `base_url: localhost` ou `prod.com` |

---

## 🎯 Votre Configuration Actuelle

### Dans la Collection (Flask-API-Tests.postman_collection.json)

```json
"variable": [
  {
    "key": "base_url",
    "value": "http://localhost:8080",
    "type": "string"
  },
  {
    "key": "api_path",
    "value": "/api",
    "type": "string"
  }
]
```

**Rôle** : Valeurs par défaut si aucun environnement n'est sélectionné

### Dans les Environnements

**Local.postman_environment.json** :
```json
{
  "key": "base_url",
  "value": "http://localhost:8080"
}
```

**Dev.postman_environment.json** :
```json
{
  "key": "base_url",
  "value": "https://dev-api.example.com"
}
```

**Rôle** : Écraser `base_url` selon l'environnement sélectionné

---

## 🔄 Ordre de Priorité

Postman résout les variables dans cet ordre (du plus prioritaire au moins) :

```
1. 🌍 Variables d'Environnement (sélectionné)
2. 📦 Variables de Collection
3. 🌐 Variables Globales
4. 💾 Variables de Données (CSV/JSON)
```

### Exemple Concret

**Collection** :
```json
base_url: "http://localhost:8080"
```

**Environnement Local** :
```json
base_url: "http://localhost:8080"
```

**Environnement Dev** :
```json
base_url: "https://dev-api.example.com"
```

**Résultat** :
```
Aucun environnement sélectionné → http://localhost:8080 (collection)
Environnement "Local" sélectionné → http://localhost:8080 (env)
Environnement "Dev" sélectionné → https://dev-api.example.com (env)
```

---

## 🎨 Bonnes Pratiques

### ✅ Variables de Collection

**Utilisez pour** :
- Valeurs **constantes** (ne changent jamais)
- Valeurs **par défaut** (fallback)
- Valeurs **communes** à tous les environnements

**Exemples** :
```json
{
  "api_path": "/api",           // Toujours /api
  "api_version": "v1",          // Toujours v1
  "timeout": "5000",            // Timeout par défaut
  "content_type": "application/json"
}
```

### ✅ Variables d'Environnement

**Utilisez pour** :
- Valeurs **variables** selon l'environnement
- URLs **différentes** (local, dev, prod)
- Clés API **différentes**
- Configurations **spécifiques**

**Exemples** :
```json
{
  "base_url": "http://localhost:8080",  // Change selon env
  "api_key": "dev-key-123",             // Différent par env
  "database": "dev_db",                 // Différent par env
  "debug": "true"                       // Différent par env
}
```

---

## 🔍 Cas d'Usage Réels

### Scénario 1 : API Path Constant

**Collection** :
```json
{
  "api_path": "/api"
}
```

**Requêtes** :
```
{{base_url}}{{api_path}}/users
{{base_url}}{{api_path}}/health
```

**Résultat** :
```
Local : http://localhost:8080/api/users
Dev   : https://dev-api.com/api/users
```

### Scénario 2 : Versions Différentes

**Collection** :
```json
{
  "api_version": "v1"
}
```

**Environnement Dev** :
```json
{
  "api_version": "v2"  // Override pour tester v2
}
```

**Requêtes** :
```
{{base_url}}/{{api_version}}/users
```

**Résultat** :
```
Local : http://localhost:8080/v1/users (collection)
Dev   : https://dev-api.com/v2/users (env override)
```

### Scénario 3 : Authentification

**Collection** :
```json
{
  "auth_type": "Bearer"
}
```

**Environnement Local** :
```json
{
  "api_key": "dev-key-123"
}
```

**Environnement Prod** :
```json
{
  "api_key": "prod-key-xyz"
}
```

**Requêtes** :
```
Header: Authorization: {{auth_type}} {{api_key}}
```

**Résultat** :
```
Local : Authorization: Bearer dev-key-123
Prod  : Authorization: Bearer prod-key-xyz
```

---

## 🛠️ Modification des Variables

### Modifier les Variables de Collection

**Option 1 : Via Postman**
```
Collection → ... → Edit → Variables
```

**Option 2 : Via le Fichier JSON**
```json
"variable": [
  {
    "key": "nouvelle_variable",
    "value": "nouvelle_valeur"
  }
]
```

### Modifier les Variables d'Environnement

**Option 1 : Via Postman**
```
Environments → Sélectionner env → Modifier
```

**Option 2 : Via le Fichier JSON**
```json
{
  "values": [
    {
      "key": "base_url",
      "value": "https://nouvelle-url.com"
    }
  ]
}
```

---

## 🎯 Recommandations pour Votre Projet

### Variables à Mettre dans la Collection

```json
{
  "api_path": "/api",              // Constant
  "content_type": "application/json", // Constant
  "timeout": "5000"                // Par défaut
}
```

### Variables à Mettre dans les Environnements

```json
// Local
{
  "base_url": "http://localhost:8080",
  "environment": "local",
  "debug": "true"
}

// Dev
{
  "base_url": "https://dev-api.example.com",
  "environment": "dev",
  "debug": "true"
}

// Production
{
  "base_url": "https://api.example.com",
  "environment": "production",
  "debug": "false"
}
```

---

## 🔒 Variables Secrètes

### Type "secret"

```json
{
  "key": "api_key",
  "value": "super-secret-key",
  "type": "secret",  // Masqué dans l'interface
  "enabled": true
}
```

**Avantages** :
- ✅ Valeur masquée (****)
- ✅ Non visible dans les logs
- ✅ Sécurisé pour le partage d'écran

**Utilisation** :
```
Header: X-API-Key: {{api_key}}
```

---

## 📊 Tableau Récapitulatif

| Variable | Type | Valeur Local | Valeur Dev | Où la Mettre ? |
|----------|------|--------------|------------|----------------|
| `base_url` | URL | `localhost:8080` | `dev-api.com` | 🌍 Environnement |
| `api_path` | Path | `/api` | `/api` | 📦 Collection |
| `api_key` | Secret | `dev-key` | `prod-key` | 🌍 Environnement |
| `timeout` | Number | `5000` | `5000` | 📦 Collection |
| `environment` | String | `local` | `dev` | 🌍 Environnement |
| `api_version` | String | `v1` | `v1` | 📦 Collection |

---

## 🎓 Exercice Pratique

### Ajoutez une Variable de Timeout

**1. Dans la Collection** (valeur par défaut) :
```json
{
  "key": "request_timeout",
  "value": "5000"
}
```

**2. Dans l'Environnement Dev** (override) :
```json
{
  "key": "request_timeout",
  "value": "10000"  // Plus long pour serveur distant
}
```

**3. Utilisez dans les Tests** :
```javascript
pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(
        parseInt(pm.environment.get("request_timeout"))
    );
});
```

**Résultat** :
```
Local : Timeout < 5000ms
Dev   : Timeout < 10000ms (serveur distant plus lent)
```

---

## 💡 Astuces Pro

### 1. Variables Dynamiques

Postman offre des variables dynamiques :
```
{{$timestamp}}     // 1702742400
{{$randomInt}}     // 42
{{$guid}}          // uuid
{{$randomEmail}}   // test@example.com
```

### 2. Variables Calculées

Dans les scripts :
```javascript
// Pre-request Script
pm.environment.set("full_url", 
    pm.environment.get("base_url") + 
    pm.collectionVariables.get("api_path")
);
```

### 3. Variables Conditionnelles

```javascript
// Test Script
if (pm.environment.get("environment") === "production") {
    pm.test("Response time is fast", function () {
        pm.expect(pm.response.responseTime).to.be.below(200);
    });
} else {
    pm.test("Response time is acceptable", function () {
        pm.expect(pm.response.responseTime).to.be.below(1000);
    });
}
```

---

## ✅ Checklist de Compréhension

- [ ] Je comprends la différence entre variables de collection et d'environnement
- [ ] Je sais quand utiliser chaque type
- [ ] Je connais l'ordre de priorité
- [ ] Je peux modifier les variables
- [ ] Je sais utiliser les variables secrètes
- [ ] Je peux créer des variables dynamiques

---

## 🎯 Résumé en 3 Points

1. **Collection** = Valeurs par défaut et constantes
2. **Environnement** = Valeurs spécifiques qui changent
3. **Environnement écrase Collection** (priorité plus haute)

**Votre configuration est optimale ! 🎉**