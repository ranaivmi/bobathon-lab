# 🐍 Serveur Web de Test Flask

Serveur web léger pour tests et développement, basé sur Flask + SQLite.

## 📋 Informations

- **Emplacement**: `/Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test`
- **Framework**: Flask (Python)
- **Base de données**: SQLite
- **Port**: 5000
- **URL**: http://localhost:5000

## 🚀 Installation Rapide

### Prérequis
- Python 3.x (déjà installé sur macOS)
- pip3

### Installation

```bash
# 1. Se placer dans le répertoire
cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement virtuel
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

## 🎯 Démarrage

### Option 1 : Script automatique (recommandé)
```bash
./start.sh
```

### Option 2 : Démarrage manuel
```bash
cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test
source venv/bin/activate
python3 app.py
```

Le serveur démarre sur **http://localhost:5000**

## 🛑 Arrêt du Serveur

Appuyez sur `Ctrl + C` dans le terminal

## 📡 API Endpoints

### Utilisateurs

| Méthode | Endpoint | Description | Body |
|---------|----------|-------------|------|
| GET | `/api/users` | Liste tous les utilisateurs | - |
| GET | `/api/users/<id>` | Récupère un utilisateur | - |
| POST | `/api/users` | Crée un utilisateur | `{"name": "...", "email": "..."}` |
| PUT | `/api/users/<id>` | Met à jour un utilisateur | `{"name": "...", "email": "..."}` |
| DELETE | `/api/users/<id>` | Supprime un utilisateur | - |

### Système

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/stats` | Statistiques du serveur |
| GET | `/api/health` | Health check |

## 🧪 Exemples d'utilisation

### Via curl

```bash
# Lister les utilisateurs
curl http://localhost:5000/api/users

# Créer un utilisateur
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jean Dupont","email":"jean@example.com"}'

# Récupérer un utilisateur
curl http://localhost:5000/api/users/1

# Mettre à jour un utilisateur
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jean Martin"}'

# Supprimer un utilisateur
curl -X DELETE http://localhost:5000/api/users/1

# Statistiques
curl http://localhost:5000/api/stats
```

### Via navigateur

Ouvrez simplement http://localhost:5000 pour accéder à l'interface web interactive.

## 📁 Structure du Projet

```
serveur-test/
├── app.py              # Application Flask principale
├── requirements.txt    # Dépendances Python
├── start.sh           # Script de démarrage
├── README.md          # Ce fichier
├── RUNBOOK.md         # Guide d'exploitation
├── venv/              # Environnement virtuel (créé à l'installation)
└── test.db            # Base de données SQLite (créée au premier démarrage)
```

## 🔧 Configuration

### Changer le port

Éditez `app.py`, ligne finale :
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Changez 5000
```

### Mode debug

Le mode debug est activé par défaut. Pour le désactiver en production :
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📊 Base de Données

### Emplacement
`/Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test/test.db`

### Structure

**Table: users**
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `email` (TEXT)
- `created_at` (TIMESTAMP)

### Réinitialiser la base

```bash
rm test.db
python3 app.py  # Recrée la base avec données de test
```

## 🐛 Dépannage

### Le serveur ne démarre pas

1. Vérifier que Python 3 est installé :
   ```bash
   python3 --version
   ```

2. Vérifier que l'environnement virtuel est activé :
   ```bash
   which python  # Doit pointer vers venv/bin/python
   ```

3. Réinstaller les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Port déjà utilisé

Si le port 5000 est occupé :
```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>
```

### Erreur de permissions

```bash
chmod +x start.sh
```

## 📚 Documentation Complète

Consultez le [RUNBOOK.md](RUNBOOK.md) pour :
- Procédures d'exploitation détaillées
- Gestion des incidents
- Maintenance et monitoring
- Sauvegarde et restauration

## 💡 Caractéristiques

- ✅ **Léger** : ~15 MB (venv + dépendances)
- ✅ **Non-intrusif** : Tout dans un dossier
- ✅ **Portable** : Copiez le dossier, ça fonctionne
- ✅ **API REST complète** : CRUD complet
- ✅ **Interface web** : Tests interactifs
- ✅ **SQLite** : Gère 50k+ enregistrements
- ✅ **Auto-documentation** : Interface web avec exemples

## 🔒 Sécurité

⚠️ **Ce serveur est conçu pour le développement/test uniquement !**

Pour la production :
- Désactiver le mode debug
- Ajouter l'authentification
- Utiliser HTTPS
- Configurer CORS correctement
- Utiliser une vraie base de données (PostgreSQL, MySQL)

## 📝 Licence

Projet de test - Usage libre

## 👤 Auteur

Créé pour : sithidet
Date : 16 décembre 2025
