# Guide de Sécurité - Bobathon Lab

## Vulnérabilités Corrigées

### 1. Injection SQL ✅
**Problème**: Construction dynamique de requêtes SQL avec f-strings
**Solution**: Utilisation exclusive de requêtes paramétrées avec `?` placeholders

### 2. Cross-Site Scripting (XSS) ✅
**Problème**: Utilisation de `render_template_string` sans échappement
**Solution**: 
- Validation stricte des entrées utilisateur
- Sanitisation de toutes les données
- En-têtes CSP (Content Security Policy)

### 3. Validation des Entrées ✅
**Problème**: Aucune validation des données utilisateur
**Solution**:
- Regex pour validation email et nom
- Fonction `sanitize_input()` pour nettoyer les entrées
- Limites de longueur strictes
- Vérification des doublons d'email

### 4. Rate Limiting ✅
**Problème**: Pas de protection contre les attaques par force brute
**Solution**: Flask-Limiter avec limites par endpoint:
- GET /api/users: 30/minute
- POST /api/users: 10/minute (création)
- PUT /api/users: 20/minute
- DELETE /api/users: 10/minute
- Limite globale: 200/jour, 50/heure

### 5. En-têtes de Sécurité HTTP ✅
**Problème**: Absence d'en-têtes de sécurité
**Solution**: Flask-Talisman avec:
- Content Security Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options
- Strict-Transport-Security (en production)

### 6. Exposition d'Informations Sensibles ✅
**Problème**: Chemins de fichiers et erreurs détaillées exposés
**Solution**:
- Messages d'erreur génériques en production
- Chemins système masqués (sauf en mode DEBUG)
- Logging sécurisé des erreurs
- Gestionnaires d'erreurs personnalisés

### 7. Mode DEBUG en Production ✅
**Problème**: DEBUG potentiellement activé en production
**Solution**: DEBUG forcé à False en environnement Docker

### 8. CORS Non Restreint ✅
**Problème**: CORS ouvert à tous les domaines
**Solution**: Configuration CORS avec origines autorisées via variable d'environnement

## Configuration Recommandée

### Variables d'Environnement (.env)

```bash
# Sécurité
SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_hex(32))">
DEBUG=False
ALLOWED_ORIGINS=https://votredomaine.com,https://www.votredomaine.com

# Application
PORT=5001
DB_PATH=/app/data/test.db
NGINX_PORT=8080

# Gunicorn
GUNICORN_WORKERS=2
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=60
```

### Génération de SECRET_KEY Sécurisée

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Bonnes Pratiques Implémentées

1. **Principe du Moindre Privilège**: Utilisateur non-root dans Docker
2. **Défense en Profondeur**: Multiples couches de sécurité
3. **Validation Stricte**: Toutes les entrées sont validées et nettoyées
4. **Logging Sécurisé**: Erreurs loggées sans exposer de données sensibles
5. **Limites de Ressources**: Taille maximale des requêtes (16MB)
6. **Isolation**: Réseau Docker isolé
7. **Health Checks**: Surveillance de l'état de l'application

## Tests de Sécurité Recommandés

### 1. Test d'Injection SQL
```bash
# Devrait échouer avec validation
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com OR 1=1"}'
```

### 2. Test de Rate Limiting
```bash
# Faire plus de 10 requêtes en 1 minute
for i in {1..15}; do
  curl -X POST http://localhost:8080/api/users \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"Test$i\",\"email\":\"test$i@test.com\"}"
done
```

### 3. Test de Validation Email
```bash
# Devrait échouer
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"invalid-email"}'
```

### 4. Test XSS
```bash
# Devrait être nettoyé/rejeté
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"<script>alert(1)</script>","email":"test@test.com"}'
```

## Checklist de Déploiement

- [ ] SECRET_KEY généré et configuré
- [ ] DEBUG=False en production
- [ ] ALLOWED_ORIGINS configuré avec domaines autorisés
- [ ] HTTPS activé (via Nginx/reverse proxy)
- [ ] Certificats SSL valides
- [ ] Logs configurés et surveillés
- [ ] Sauvegardes de la base de données
- [ ] Monitoring actif
- [ ] Rate limiting testé
- [ ] Validation des entrées testée

## Maintenance Continue

1. **Mises à jour régulières**: Garder les dépendances à jour
2. **Audit de sécurité**: Scanner régulièrement avec `safety` ou `bandit`
3. **Surveillance des logs**: Détecter les tentatives d'attaque
4. **Tests de pénétration**: Effectuer des tests réguliers
5. **Revue de code**: Vérifier les nouvelles fonctionnalités

## Outils de Sécurité Recommandés

```bash
# Scanner de vulnérabilités Python
pip install safety bandit

# Vérifier les dépendances
safety check

# Analyse statique du code
bandit -r app.py
```

## Contact Sécurité

Pour signaler une vulnérabilité de sécurité, veuillez contacter l'équipe de sécurité.

---
**Dernière mise à jour**: 2025-12-16
**Version**: 2.0 (Sécurisée)