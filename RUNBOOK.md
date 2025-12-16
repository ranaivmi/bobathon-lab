# 📘 RUNBOOK - Serveur Web Flask

Guide d'exploitation et de gestion du serveur web de test Flask.

---

## 📑 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Démarrage et Arrêt](#démarrage-et-arrêt)
3. [Monitoring et Surveillance](#monitoring-et-surveillance)
4. [Gestion de la Base de Données](#gestion-de-la-base-de-données)
5. [Maintenance](#maintenance)
6. [Dépannage](#dépannage)
7. [Sauvegarde et Restauration](#sauvegarde-et-restauration)
8. [Procédures d'Urgence](#procédures-durgence)
9. [Logs et Diagnostics](#logs-et-diagnostics)
10. [Checklist Opérationnelle](#checklist-opérationnelle)

---

## 🎯 Vue d'ensemble

### Informations Système

| Élément | Valeur |
|---------|--------|
| **Nom du service** | Serveur Flask Test |
| **Emplacement** | `/Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test` |
| **Framework** | Flask 3.0.0 |
| **Base de données** | SQLite (test.db) |
| **Port** | 5000 |
| **URL** | http://localhost:5000 |
| **Environnement** | Développement/Test |

### Architecture

```
┌─────────────────────────────────────┐
│   Navigateur / Client HTTP          │
└──────────────┬──────────────────────┘
               │ HTTP (port 5000)
               ▼
┌─────────────────────────────────────┐
│   Flask Application (app.py)        │
│   - Routes API REST                 │
│   - Interface Web                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SQLite Database (test.db)         │
│   - Table: users                    │
└─────────────────────────────────────┘
```

### Composants

1. **app.py** : Application Flask principale
2. **test.db** : Base de données SQLite
3. **venv/** : Environnement virtuel Python
4. **start.sh** : Script de démarrage automatisé

---

## 🚀 Démarrage et Arrêt

### Démarrage Standard

#### Méthode 1 : Script automatique (Recommandé)

```bash
cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test
./start.sh
```

**Ce que fait le script :**
- Vérifie l'existence de l'environnement virtuel
- Crée l'environnement si nécessaire
- Active l'environnement virtuel
- Installe/vérifie les dépendances
- Lance l'application

#### Méthode 2 : Démarrage manuel

```bash
cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test
source venv/bin/activate
python3 app.py
```

### Vérification du Démarrage

1. **Console** : Vérifier les messages de démarrage
   ```
   ✅ Base de données prête!
   🚀 Démarrage du serveur...
   📍 Accédez à: http://localhost:5000
   ```

2. **Health Check** :
   ```bash
   curl http://localhost:5000/api/health
   ```
   
   Réponse attendue :
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-12-16T10:00:00",
     "service": "Flask Test Server"
   }
   ```

3. **Interface Web** : Ouvrir http://localhost:5000

### Arrêt du Serveur

#### Arrêt Normal

Dans le terminal où le serveur tourne :
```bash
Ctrl + C
```

#### Arrêt Forcé

Si le serveur ne répond pas :

```bash
# Trouver le processus
lsof -i :5000

# Exemple de sortie :
# COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# Python  12345  user    3u  IPv4  0x...      0t0  TCP *:5000 (LISTEN)

# Tuer le processus
kill -9 12345
```

#### Script d'arrêt automatique

Créer un fichier `stop.sh` :
```bash
#!/bin/bash
PID=$(lsof -ti :5000)
if [ -n "$PID" ]; then
    echo "🛑 Arrêt du serveur (PID: $PID)..."
    kill -9 $PID
    echo "✅ Serveur arrêté"
else
    echo "ℹ️  Aucun serveur en cours d'exécution"
fi
```

### Redémarrage

```bash
# Arrêt
Ctrl + C

# Attendre 2 secondes
sleep 2

# Redémarrage
./start.sh
```

---

## 📊 Monitoring et Surveillance

### Vérifications de Santé

#### 1. Health Check Automatique

```bash
# Script de monitoring simple
while true; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health)
    if [ "$STATUS" -eq 200 ]; then
        echo "✅ $(date): Serveur OK"
    else
        echo "❌ $(date): Serveur KO (Code: $STATUS)"
    fi
    sleep 60  # Vérifier toutes les minutes
done
```

#### 2. Statistiques du Serveur

```bash
curl http://localhost:5000/api/stats | python3 -m json.tool
```

Informations retournées :
- Nombre total d'utilisateurs
- Taille de la base de données
- Chemin de la base
- Timestamp

### Métriques à Surveiller

| Métrique | Commande | Seuil d'alerte |
|----------|----------|----------------|
| **Disponibilité** | `curl http://localhost:5000/api/health` | Code ≠ 200 |
| **Taille DB** | `ls -lh test.db` | > 100 MB |
| **Nombre d'utilisateurs** | `curl http://localhost:5000/api/stats` | > 45000 |
| **Utilisation CPU** | `top -pid $(lsof -ti :5000)` | > 80% |
| **Utilisation Mémoire** | `ps aux \| grep python` | > 500 MB |

### Monitoring Continu

Créer un script `monitor.sh` :

```bash
#!/bin/bash

LOG_FILE="monitoring.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Health check
    HEALTH=$(curl -s http://localhost:5000/api/health)
    
    # Stats
    STATS=$(curl -s http://localhost:5000/api/stats)
    USERS=$(echo $STATS | python3 -c "import sys, json; print(json.load(sys.stdin)['total_users'])")
    DB_SIZE=$(echo $STATS | python3 -c "import sys, json; print(json.load(sys.stdin)['database_size_mb'])")
    
    # Log
    echo "$TIMESTAMP | Users: $USERS | DB: ${DB_SIZE}MB | Status: OK" >> $LOG_FILE
    
    sleep 300  # Toutes les 5 minutes
done
```

---

## 🗄️ Gestion de la Base de Données

### Informations Base de Données

- **Type** : SQLite
- **Fichier** : `test.db`
- **Emplacement** : `/Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test/test.db`
- **Capacité recommandée** : 50 000 enregistrements

### Opérations Courantes

#### 1. Consulter la Base

```bash
# Installer sqlite3 si nécessaire
brew install sqlite3

# Ouvrir la base
sqlite3 test.db

# Commandes SQLite utiles :
.tables                    # Lister les tables
.schema users             # Voir la structure
SELECT COUNT(*) FROM users;  # Compter les utilisateurs
SELECT * FROM users LIMIT 10;  # Voir 10 utilisateurs
.quit                     # Quitter
```

#### 2. Exporter les Données

```bash
# Export CSV
sqlite3 test.db <<EOF
.headers on
.mode csv
.output users_export.csv
SELECT * FROM users;
.quit
EOF

# Export SQL
sqlite3 test.db .dump > backup.sql
```

#### 3. Importer des Données

```bash
# Import SQL
sqlite3 test.db < backup.sql

# Import CSV
sqlite3 test.db <<EOF
.mode csv
.import users_import.csv users
.quit
EOF
```

#### 4. Réinitialiser la Base

```bash
# Sauvegarder d'abord
cp test.db test.db.backup

# Supprimer
rm test.db

# Redémarrer l'application (recrée la base)
python3 app.py
```

#### 5. Optimiser la Base

```bash
sqlite3 test.db "VACUUM;"
```

### Maintenance de la Base

#### Vérification de l'Intégrité

```bash
sqlite3 test.db "PRAGMA integrity_check;"
```

Résultat attendu : `ok`

#### Statistiques de la Base

```bash
sqlite3 test.db <<EOF
SELECT 
    COUNT(*) as total_users,
    MIN(created_at) as first_user,
    MAX(created_at) as last_user
FROM users;
.quit
EOF
```

---

## 🔧 Maintenance

### Maintenance Quotidienne

**Durée estimée : 5 minutes**

```bash
# 1. Vérifier le statut
curl http://localhost:5000/api/health

# 2. Vérifier les stats
curl http://localhost:5000/api/stats

# 3. Vérifier la taille de la base
ls -lh test.db

# 4. Vérifier les logs (si activés)
tail -n 50 monitoring.log
```

### Maintenance Hebdomadaire

**Durée estimée : 15 minutes**

```bash
# 1. Sauvegarder la base
cp test.db backups/test_$(date +%Y%m%d).db

# 2. Optimiser la base
sqlite3 test.db "VACUUM;"

# 3. Vérifier l'intégrité
sqlite3 test.db "PRAGMA integrity_check;"

# 4. Nettoyer les anciennes sauvegardes (garder 30 jours)
find backups/ -name "test_*.db" -mtime +30 -delete

# 5. Vérifier l'espace disque
df -h /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test
```

### Maintenance Mensuelle

**Durée estimée : 30 minutes**

```bash
# 1. Mettre à jour les dépendances
source venv/bin/activate
pip list --outdated
pip install --upgrade flask flask-cors

# 2. Analyser les performances
sqlite3 test.db "ANALYZE;"

# 3. Exporter les données (archive)
sqlite3 test.db .dump > archives/backup_$(date +%Y%m).sql
gzip archives/backup_$(date +%Y%m).sql

# 4. Vérifier les permissions
ls -la test.db
chmod 644 test.db  # Si nécessaire

# 5. Tester tous les endpoints
curl http://localhost:5000/api/users
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/health
```

### Mise à Jour de l'Application

```bash
# 1. Arrêter le serveur
Ctrl + C

# 2. Sauvegarder
cp test.db test.db.backup
cp app.py app.py.backup

# 3. Mettre à jour le code (si nécessaire)
# Éditer app.py

# 4. Tester
python3 app.py

# 5. Vérifier
curl http://localhost:5000/api/health
```

---

## 🐛 Dépannage

### Problèmes Courants

#### 1. Le serveur ne démarre pas

**Symptôme** : Erreur au lancement de `./start.sh` ou `python3 app.py`

**Diagnostic** :
```bash
# Vérifier Python
python3 --version

# Vérifier l'environnement virtuel
ls -la venv/

# Vérifier les dépendances
source venv/bin/activate
pip list
```

**Solutions** :

a) Recréer l'environnement virtuel :
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

b) Vérifier les permissions :
```bash
chmod +x start.sh
chmod 644 app.py
```

#### 2. Port 5000 déjà utilisé

**Symptôme** : `Address already in use`

**Diagnostic** :
```bash
lsof -i :5000
```

**Solutions** :

a) Tuer le processus existant :
```bash
kill -9 $(lsof -ti :5000)
```

b) Changer le port dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Utiliser 5001
```

#### 3. Erreur de base de données

**Symptôme** : `database is locked` ou erreurs SQL

**Diagnostic** :
```bash
sqlite3 test.db "PRAGMA integrity_check;"
```

**Solutions** :

a) Fermer toutes les connexions :
```bash
# Redémarrer le serveur
Ctrl + C
./start.sh
```

b) Réparer la base :
```bash
# Sauvegarder
cp test.db test.db.corrupt

# Exporter et réimporter
sqlite3 test.db .dump > temp.sql
rm test.db
sqlite3 test.db < temp.sql
```

c) Restaurer depuis une sauvegarde :
```bash
cp backups/test_YYYYMMDD.db test.db
```

#### 4. Erreur 404 sur les endpoints

**Symptôme** : `404 Not Found` sur `/api/users`

**Diagnostic** :
```bash
# Vérifier que le serveur tourne
curl http://localhost:5000/api/health

# Vérifier les routes
grep "@app.route" app.py
```

**Solutions** :

a) Vérifier l'URL :
```bash
# Correct
curl http://localhost:5000/api/users

# Incorrect
curl http://localhost:5000/users  # Manque /api/
```

b) Redémarrer le serveur

#### 5. Performances lentes

**Symptôme** : Réponses lentes (> 2 secondes)

**Diagnostic** :
```bash
# Taille de la base
ls -lh test.db

# Nombre d'enregistrements
sqlite3 test.db "SELECT COUNT(*) FROM users;"

# Utilisation CPU/Mémoire
top -pid $(lsof -ti :5000)
```

**Solutions** :

a) Optimiser la base :
```bash
sqlite3 test.db "VACUUM;"
sqlite3 test.db "ANALYZE;"
```

b) Nettoyer les anciennes données :
```bash
sqlite3 test.db "DELETE FROM users WHERE created_at < date('now', '-1 year');"
```

c) Ajouter des index (si nécessaire) :
```bash
sqlite3 test.db "CREATE INDEX idx_email ON users(email);"
```

### Codes d'Erreur HTTP

| Code | Signification | Action |
|------|---------------|--------|
| 200 | OK | Aucune action |
| 201 | Créé | Aucune action |
| 400 | Requête invalide | Vérifier le format JSON |
| 404 | Non trouvé | Vérifier l'URL et l'ID |
| 500 | Erreur serveur | Consulter les logs, redémarrer |

---

## 💾 Sauvegarde et Restauration

### Stratégie de Sauvegarde

#### Sauvegarde Manuelle

```bash
# Créer le dossier de sauvegarde
mkdir -p backups

# Sauvegarde simple
cp test.db backups/test_$(date +%Y%m%d_%H%M%S).db

# Sauvegarde avec export SQL
sqlite3 test.db .dump > backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Sauvegarde Automatique

Créer un script `backup.sh` :

```bash
#!/bin/bash

BACKUP_DIR="/Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_FILE="test.db"

# Créer le dossier si nécessaire
mkdir -p "$BACKUP_DIR"

# Sauvegarde
cp "$DB_FILE" "$BACKUP_DIR/test_$TIMESTAMP.db"

# Compression
gzip "$BACKUP_DIR/test_$TIMESTAMP.db"

# Nettoyer les sauvegardes > 30 jours
find "$BACKUP_DIR" -name "test_*.db.gz" -mtime +30 -delete

echo "✅ Sauvegarde créée: test_$TIMESTAMP.db.gz"
```

Rendre exécutable :
```bash
chmod +x backup.sh
```

Automatiser avec cron :
```bash
# Éditer crontab
crontab -e

# Ajouter (sauvegarde quotidienne à 2h du matin)
0 2 * * * /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test/backup.sh
```

### Restauration

#### Restauration depuis une sauvegarde .db

```bash
# 1. Arrêter le serveur
Ctrl + C

# 2. Sauvegarder l'état actuel
cp test.db test.db.before_restore

# 3. Restaurer
cp backups/test_YYYYMMDD_HHMMSS.db test.db

# Ou si compressé
gunzip -c backups/test_YYYYMMDD_HHMMSS.db.gz > test.db

# 4. Redémarrer
./start.sh

# 5. Vérifier
curl http://localhost:5000/api/stats
```

#### Restauration depuis un export SQL

```bash
# 1. Arrêter le serveur
Ctrl + C

# 2. Sauvegarder l'état actuel
cp test.db test.db.before_restore

# 3. Supprimer la base actuelle
rm test.db

# 4. Restaurer depuis SQL
sqlite3 test.db < backups/backup_YYYYMMDD_HHMMSS.sql

# 5. Redémarrer
./start.sh

# 6. Vérifier
curl http://localhost:5000/api/stats
```

### Politique de Rétention

| Type | Fréquence | Rétention | Emplacement |
|------|-----------|-----------|-------------|
| **Quotidienne** | Tous les jours à 2h | 7 jours | `backups/` |
| **Hebdomadaire** | Dimanche à 2h | 4 semaines | `backups/weekly/` |
| **Mensuelle** | 1er du mois à 2h | 12 mois | `archives/` |

---

## 🚨 Procédures d'Urgence

### Incident Critique : Serveur Inaccessible

**Temps de résolution cible : 5 minutes**

1. **Vérifier le processus**
   ```bash
   lsof -i :5000
   ```

2. **Redémarrer le serveur**
   ```bash
   cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test
   ./start.sh
   ```

3. **Vérifier la santé**
   ```bash
   curl http://localhost:5000/api/health
   ```

4. **Si échec, restaurer depuis sauvegarde**
   ```bash
   cp backups/test_latest.db test.db
   ./start.sh
   ```

### Incident Majeur : Corruption de Base de Données

**Temps de résolution cible : 15 minutes**

1. **Arrêter le serveur**
   ```bash
   kill -9 $(lsof -ti :5000)
   ```

2. **Sauvegarder l'état corrompu**
   ```bash
   cp test.db test.db.corrupted_$(date +%Y%m%d_%H%M%S)
   ```

3. **Tenter une réparation**
   ```bash
   sqlite3 test.db .dump > temp_recovery.sql
   rm test.db
   sqlite3 test.db < temp_recovery.sql
   ```

4. **Si échec, restaurer la dernière sauvegarde**
   ```bash
   cp backups/test_$(ls -t backups/ | head -1) test.db
   ```

5. **Redémarrer et vérifier**
   ```bash
   ./start.sh
   curl http://localhost:5000/api/stats
   ```

### Incident Mineur : Performances Dégradées

**Temps de résolution cible : 10 minutes**

1. **Vérifier les ressources**
   ```bash
   top -pid $(lsof -ti :5000)
   ```

2. **Optimiser la base**
   ```bash
   sqlite3 test.db "VACUUM;"
   ```

3. **Redémarrer le serveur**
   ```bash
   Ctrl + C
   ./start.sh
   ```

### Escalade

Si les procédures ci-dessus échouent :

1. **Documenter le problème**
   - Capturer les messages d'erreur
   - Noter l'heure et les actions effectuées
   - Sauvegarder les logs

2. **Contacter le support**
   - Email : support@example.com
   - Téléphone : +33 X XX XX XX XX

---

## 📋 Logs et Diagnostics

### Logs de l'Application

Par défaut, Flask affiche les logs dans la console.

#### Activer les logs dans un fichier

Modifier `app.py` :

```python
import logging
from logging.handlers import RotatingFileHandler

# Configuration des logs
if not app.debug:
    file_handler = RotatingFileHandler('flask.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask startup')
```

#### Consulter les logs

```bash
# Logs en temps réel
tail -f flask.log

# Dernières 100 lignes
tail -n 100 flask.log

# Rechercher des erreurs
grep ERROR flask.log

# Logs d'aujourd'hui
grep "$(date +%Y-%m-%d)" flask.log
```

### Diagnostics Système

#### Vérifier l'état du système

```bash
# Processus Python
ps aux | grep python

# Utilisation du port
lsof -i :5000

# Espace disque
df -h /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test

# Mémoire disponible
vm_stat

# Charge système
uptime
```

#### Tests de Connectivité

```bash
# Test local
curl http://localhost:5000/api/health

# Test avec timeout
curl --max-time 5 http://localhost:5000/api/health

# Test verbose
curl -v http://localhost:5000/api/health
```

---

## ✅ Checklist Opérationnelle

### Checklist de Démarrage

- [ ] Vérifier que Python 3 est installé
- [ ] Se placer dans le bon répertoire
- [ ] Activer l'environnement virtuel
- [ ] Vérifier les dépendances
- [ ] Lancer l'application
- [ ] Vérifier le health check
- [ ] Tester l'interface web
- [ ] Vérifier les API endpoints

### Checklist Quotidienne

- [ ] Vérifier que le serveur est accessible
- [ ] Consulter les statistiques
- [ ] Vérifier la taille de la base de données
- [ ] Vérifier l'espace disque disponible

### Checklist Hebdomadaire

- [ ] Effectuer une sauvegarde manuelle
- [ ] Optimiser la base de données (VACUUM)
- [ ] Vérifier l'intégrité de la base
- [ ] Nettoyer les anciennes sauvegardes
- [ ] Tester tous les endpoints API

### Checklist Mensuelle

- [ ] Mettre à jour les dépendances Python
- [ ] Créer une archive mensuelle
- [ ] Analyser les performances
- [ ] Réviser les logs
- [ ] Tester la procédure de restauration

### Checklist Avant Arrêt

- [ ] Vérifier qu'aucune opération n'est en cours
- [ ] Effectuer une sauvegarde
- [ ] Arrêter proprement le serveur (Ctrl+C)
- [ ] Vérifier que le port est libéré
- [ ] Documenter la raison de l'arrêt

---

## 📞 Contacts et Support

### Informations de Contact

| Rôle | Nom | Contact |
|------|-----|---------|
| **Administrateur** | sithidet | - |
| **Support Technique** | - | - |

### Ressources Utiles

- **Documentation Flask** : https://flask.palletsprojects.com/
- **Documentation SQLite** : https://www.sqlite.org/docs.html
- **Python Documentation** : https://docs.python.org/3/

---

## 📝 Historique des Modifications

| Date | Version | Auteur | Modifications |
|------|---------|--------|---------------|
| 2025-12-16 | 1.0 | Bob | Création initiale du runbook |

---

## 📄 Annexes

### Annexe A : Commandes Rapides

```bash
# Démarrage
./start.sh

# Arrêt
Ctrl + C

# Health check
curl http://localhost:5000/api/health

# Stats
curl http://localhost:5000/api/stats

# Sauvegarde
cp test.db backups/test_$(date +%Y%m%d).db

# Restauration
cp backups/test_YYYYMMDD.db test.db

# Optimisation
sqlite3 test.db "VACUUM;"

# Logs
tail -f flask.log
```

### Annexe B : Variables d'Environnement

Aucune variable d'environnement requise pour cette installation.

### Annexe C : Ports et Protocoles

| Port | Protocole | Usage |
|------|-----------|-------|
| 5000 | HTTP | API REST et Interface Web |

---

**Fin du Runbook**

*Document maintenu par : sithidet*  
*Dernière mise à jour : 16 décembre 2025*
