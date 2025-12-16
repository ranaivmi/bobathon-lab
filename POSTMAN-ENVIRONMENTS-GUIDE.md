# 🌍 Guide des Environnements Postman

## 📋 Vue d'Ensemble

Ce projet inclut **2 environnements Postman** pour tester votre API Flask sur différents serveurs :

- 🏠 **Local** : Pour tester sur votre machine locale (localhost:8080)
- 🔧 **Dev** : Pour tester sur un serveur distant de développement

---

## 📥 Import des Environnements

### Étape 1 : Ouvrir Postman

Ouvrez **Postman Web** ou **Postman Desktop**

### Étape 2 : Accéder aux Environnements

1. Cliquez sur **"Environments"** (icône ⚙️ dans la barre latérale gauche)
2. Ou cliquez sur le menu déroulant en haut à droite (à côté de l'œil 👁️)

### Étape 3 : Importer les Fichiers

**Option A : Glisser-Déposer**
1. Cliquez sur **"Import"**
2. Glissez-déposez les fichiers :
   - `Local.postman_environment.json`
   - `Dev.postman_environment.json`
3. Cliquez sur **"Import"**

**Option B : Sélection de Fichiers**
1. Cliquez sur **"Import"**
2. Cliquez sur **"Choose Files"**
3. Sélectionnez les 2 fichiers `.postman_environment.json`
4. Cliquez sur **"Import"**

### Étape 4 : Vérification

Vous devriez maintenant voir :
```
Environments
  ├─ 🏠 Local
  └─ 🔧 Dev
```

---

## 🎯 Utilisation des Environnements

### Sélectionner un Environnement

1. **En haut à droite** de Postman
2. Cliquez sur le **menu déroulant** (affiche "No Environment" par défaut)
3. Sélectionnez :
   - **Local** → Teste sur `http://localhost:8080`
   - **Dev** → Teste sur `https://dev-api.example.com`

### Voir les Variables

1. Cliquez sur l'**icône œil** 👁️ à côté du sélecteur d'environnement
2. Vous verrez les variables actives :
   ```
   base_url: http://localhost:8080
   environment: local
   api_path: /api
   ```

---

## 🔧 Configuration de l'Environnement Dev

### Modifier l'URL du Serveur Dev

1. **Ouvrez l'environnement Dev** :
   - Environments → Dev → Cliquez sur "Dev"

2. **Modifiez la variable `base_url`** :
   ```
   Avant : https://dev-api.example.com
   Après : https://votre-serveur-dev.com
   ```

3. **Sauvegardez** (Ctrl+S ou Cmd+S)

### Exemples d'URLs Dev

```bash
# Serveur distant
https://dev-api.monsite.com

# Serveur avec port personnalisé
http://192.168.1.100:8080

# Serveur Heroku
https://mon-api-flask.herokuapp.com

# Serveur AWS
https://api.dev.aws.example.com

# Serveur avec sous-domaine
https://dev.api.monentreprise.fr
```

---

## 📊 Variables Disponibles

### Variables Communes aux 2 Environnements

| Variable | Description | Exemple |
|----------|-------------|---------|
| `base_url` | URL de base de l'API | `http://localhost:8080` |
| `environment` | Nom de l'environnement | `local` ou `dev` |
| `api_path` | Chemin de base de l'API | `/api` |

### Utilisation dans les Requêtes

Les requêtes utilisent automatiquement ces variables :

```
GET {{base_url}}/api/health
GET {{base_url}}/api/users
POST {{base_url}}/api/users
```

---

## 🚀 Workflow de Test

### 1. Tests Locaux (Développement)

```bash
# 1. Démarrez votre serveur local
./docker-start.sh

# 2. Dans Postman, sélectionnez "Local"
# 3. Exécutez votre collection
# 4. Tous les tests ciblent localhost:8080
```

### 2. Tests sur Serveur Dev

```bash
# 1. Assurez-vous que votre serveur dev est accessible
# 2. Dans Postman, sélectionnez "Dev"
# 3. Exécutez votre collection
# 4. Tous les tests ciblent votre serveur distant
```

### 3. Comparaison des Résultats

```bash
# Exécutez les tests sur Local
→ Notez les résultats

# Exécutez les tests sur Dev
→ Comparez avec Local

# Identifiez les différences
→ Performances, données, comportement
```

---

## 🎨 Personnalisation Avancée

### Ajouter des Variables Supplémentaires

**Exemple : Ajouter une clé API**

1. Ouvrez l'environnement (Local ou Dev)
2. Cliquez sur **"Add Variable"**
3. Ajoutez :
   ```
   Key: api_key
   Value: votre-cle-api-secrete
   Type: secret (pour masquer la valeur)
   ```
4. Utilisez dans vos requêtes :
   ```
   Header: Authorization: Bearer {{api_key}}
   ```

### Variables par Environnement

**Local** :
```json
{
  "base_url": "http://localhost:8080",
  "api_key": "dev-key-123",
  "timeout": "5000"
}
```

**Dev** :
```json
{
  "base_url": "https://dev-api.com",
  "api_key": "prod-key-xyz",
  "timeout": "10000"
}
```

---

## 🔒 Sécurité

### ⚠️ Bonnes Pratiques

✅ **À Faire** :
- Utilisez `type: "secret"` pour les clés API
- Ne commitez PAS les fichiers d'environnement avec des secrets
- Créez un `.env.example` pour documenter les variables requises
- Partagez les environnements sans les secrets

❌ **À Éviter** :
- Ne mettez pas de secrets en clair dans Git
- Ne partagez pas vos clés API dans les environnements
- N'utilisez pas les mêmes clés pour Local et Dev

### Fichier .gitignore

Ajoutez à votre `.gitignore` :
```
# Environnements Postman avec secrets
*.postman_environment.json
!Local.postman_environment.json
!Dev.postman_environment.json
```

---

## 📝 Exemple Complet

### Scénario : Tester l'API sur Local puis Dev

```bash
# 1. Démarrer le serveur local
./docker-start.sh

# 2. Dans Postman
Sélectionner : Local
Exécuter : Collection "Flask API Tests"
Résultat : ✅ 19/19 tests passés

# 3. Déployer sur le serveur Dev
git push origin dev
# (Votre CI/CD déploie automatiquement)

# 4. Dans Postman
Sélectionner : Dev
Exécuter : Collection "Flask API Tests"
Résultat : ✅ 19/19 tests passés

# 5. Comparer
Local : 7.36s
Dev : 8.52s (légèrement plus lent, normal pour un serveur distant)
```

---

## 🆘 Dépannage

### Problème : "Could not get any response"

**Cause** : Le serveur n'est pas accessible

**Solutions** :
1. Vérifiez que le serveur est démarré
2. Vérifiez l'URL dans l'environnement
3. Testez l'URL dans un navigateur
4. Vérifiez le firewall/pare-feu

### Problème : "{{base_url}} not resolved"

**Cause** : Aucun environnement sélectionné

**Solution** :
1. Sélectionnez un environnement (Local ou Dev)
2. Vérifiez que la variable `base_url` existe

### Problème : Tests échouent sur Dev mais pas sur Local

**Causes possibles** :
- Données différentes en base
- Versions différentes de l'API
- Configuration réseau
- Latence réseau

**Solution** :
1. Comparez les réponses
2. Vérifiez les logs du serveur Dev
3. Ajustez les timeouts si nécessaire

---

## 🎯 Commandes Rapides avec Bob

Une fois les environnements importés, vous pouvez utiliser Bob :

```bash
# Lister les environnements
"Liste mes environnements Postman"

# Tester avec un environnement spécifique
"Exécute ma collection Flask API Tests avec l'environnement Local"
"Exécute ma collection Flask API Tests avec l'environnement Dev"

# Comparer les résultats
"Compare les résultats entre Local et Dev"
```

---

## 📚 Ressources

- [Documentation Postman Environments](https://learning.postman.com/docs/sending-requests/managing-environments/)
- [Variables Postman](https://learning.postman.com/docs/sending-requests/variables/)
- [Collection Runner](https://learning.postman.com/docs/running-collections/intro-to-collection-runs/)

---

## ✅ Checklist

- [ ] Fichiers d'environnement importés dans Postman
- [ ] URL du serveur Dev configurée
- [ ] Variables testées (clic sur l'œil 👁️)
- [ ] Collection modifiée pour utiliser `{{base_url}}`
- [ ] Tests exécutés sur Local ✅
- [ ] Tests exécutés sur Dev ✅
- [ ] Résultats comparés

**Vos environnements sont prêts ! 🎉**