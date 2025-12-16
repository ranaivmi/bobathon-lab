from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import sqlite3
import os
import re
from datetime import datetime
from dotenv import load_dotenv
import secrets

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration CORS sécurisée
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:*').split(',')
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

# Configuration de sécurité
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# En-têtes de sécurité HTTP (désactivé en développement local)
IS_DOCKER = os.path.exists('/.dockerenv') or os.getenv('DOCKER_ENV') == 'true'
if IS_DOCKER:
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
    Talisman(app,
             force_https=False,  # Nginx gère HTTPS
             content_security_policy=csp,
             content_security_policy_nonce_in=['script-src'])

# Configuration depuis les variables d'environnement
DB_PATH = os.getenv('DB_PATH', 'test.db')
PORT = int(os.getenv('PORT', 5001))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true' and not IS_DOCKER  # Jamais en production
NGINX_PORT = os.getenv('NGINX_PORT', '80')

DISPLAY_URL = f"http://localhost:{NGINX_PORT}" if IS_DOCKER else f"http://localhost:{PORT}"
DISPLAY_PATH = os.getenv('DISPLAY_PATH', os.getcwd())

# Validation des entrées
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
NAME_REGEX = re.compile(r'^[a-zA-Z0-9\s\-\'\.]{2,100}$')

def validate_email(email):
    """Valide le format d'un email"""
    if not email or not isinstance(email, str):
        return False
    return EMAIL_REGEX.match(email) is not None

def validate_name(name):
    """Valide le format d'un nom"""
    if not name or not isinstance(name, str):
        return False
    return NAME_REGEX.match(name) is not None

def sanitize_input(text, max_length=200):
    """Nettoie et limite la longueur d'une entrée utilisateur"""
    if not text or not isinstance(text, str):
        return ""
    # Supprimer les caractères de contrôle et limiter la longueur
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    return text[:max_length].strip()

# Initialiser la base de données
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Ajouter quelques données de test
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ('Alice Dupont', 'alice@example.com'),
            ('Bob Martin', 'bob@example.com'),
            ('Claire Dubois', 'claire@example.com')
        ]
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', test_data)
    
    conn.commit()
    conn.close()

# Page d'accueil avec interface simple
HOME_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Serveur de Test Flask</title>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 900px; 
            margin: 50px auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 30px; }
        .endpoint { 
            background: white; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .method { 
            color: #27ae60; 
            font-weight: bold;
            display: inline-block;
            min-width: 60px;
        }
        .method.post { color: #e67e22; }
        .method.delete { color: #e74c3c; }
        .method.put { color: #3498db; }
        code { 
            background: #34495e; 
            color: #ecf0f1; 
            padding: 2px 6px; 
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        button {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #2980b9;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .info-box {
            background: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 3px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            color: #7f8c8d;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>🐍 Serveur de Test Flask</h1>

    <div class="stats" id="stats">
        <div class="stat-card">
            <div class="stat-value" id="userCount">-</div>
            <div class="stat-label">Utilisateurs</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">SQLite</div>
            <div class="stat-label">Base de données</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">Flask</div>
            <div class="stat-label">Framework</div>
        </div>
    </div>
    
    <h2>📡 API Endpoints</h2>
    
    <div class="endpoint">
        <span class="method">GET</span> <code>/api/users</code>
        <p>Récupère la liste complète des utilisateurs</p>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> <code>/api/users/&lt;id&gt;</code>
        <p>Récupère un utilisateur spécifique par son ID</p>
    </div>
    
    <div class="endpoint">
        <span class="method post">POST</span> <code>/api/users</code>
        <p>Crée un nouvel utilisateur</p>
        <code>{"name": "Nom", "email": "email@example.com"}</code>
    </div>
    
    <div class="endpoint">
        <span class="method put">PUT</span> <code>/api/users/&lt;id&gt;</code>
        <p>Met à jour un utilisateur existant</p>
        <code>{"name": "Nouveau nom", "email": "newemail@example.com"}</code>
    </div>
    
    <div class="endpoint">
        <span class="method delete">DELETE</span> <code>/api/users/&lt;id&gt;</code>
        <p>Supprime un utilisateur</p>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> <code>/api/stats</code>
        <p>Statistiques du serveur et de la base de données</p>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> <code>/api/health</code>
        <p>Vérification de l'état du serveur (health check)</p>
    </div>
    
    <h2>🧪 Tests Interactifs</h2>
    
    <button onclick="loadUsers()">📋 Charger les utilisateurs</button>
    <button onclick="getStats()">📊 Voir les statistiques</button>
    <button onclick="createTestUser()">➕ Créer un utilisateur test</button>
    <button onclick="clearResults()">🗑️ Effacer les résultats</button>
    
    <h3>Résultats:</h3>
    <pre id="result">Cliquez sur un bouton pour tester l'API...</pre>
    
    <script>
        // Charger les stats au démarrage
        getStats();
        
        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('userCount').textContent = data.length;
            } catch (error) {
                document.getElementById('result').textContent = 'Erreur: ' + error.message;
            }
        }
        
        async function getStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('userCount').textContent = data.total_users;
            } catch (error) {
                document.getElementById('result').textContent = 'Erreur: ' + error.message;
            }
        }
        
        async function createTestUser() {
            try {
                const timestamp = Date.now();
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: 'Test User ' + timestamp,
                        email: 'test' + timestamp + '@example.com'
                    })
                });
                const data = await response.json();
                document.getElementById('result').textContent = 'Utilisateur créé:\n' + JSON.stringify(data, null, 2);
                getStats(); // Rafraîchir les stats
            } catch (error) {
                document.getElementById('result').textContent = 'Erreur: ' + error.message;
            }
        }
        
        function clearResults() {
            document.getElementById('result').textContent = 'Résultats effacés. Cliquez sur un bouton pour tester l\'API...';
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Flask Test Server'
    })

@app.route('/api/users', methods=['GET'])
@limiter.limit("30 per minute")
def get_users():
    """Récupère tous les utilisateurs"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY created_at DESC')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(users)
    except sqlite3.Error as e:
        app.logger.error(f"Database error in get_users: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des utilisateurs'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in get_users: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
@limiter.limit("60 per minute")
def get_user(user_id):
    """Récupère un utilisateur par ID"""
    try:
        if user_id < 1:
            return jsonify({'error': 'ID invalide'}), 400
            
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return jsonify(dict(user))
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    except sqlite3.Error as e:
        app.logger.error(f"Database error in get_user: {e}")
        return jsonify({'error': 'Erreur lors de la récupération de l\'utilisateur'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in get_user: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

@app.route('/api/users', methods=['POST'])
@limiter.limit("10 per minute")
def create_user():
    """Crée un nouvel utilisateur"""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Données invalides. Requis: name, email'}), 400
        
        # Validation et nettoyage des entrées
        name = sanitize_input(data['name'], 100)
        email = sanitize_input(data['email'], 200)
        
        if not validate_name(name):
            return jsonify({'error': 'Nom invalide. Utilisez uniquement des lettres, chiffres, espaces et tirets (2-100 caractères)'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Format d\'email invalide'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Cet email est déjà utilisé'}), 409
        
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': user_id,
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
    except sqlite3.Error as e:
        app.logger.error(f"Database error in create_user: {e}")
        return jsonify({'error': 'Erreur lors de la création de l\'utilisateur'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in create_user: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@limiter.limit("20 per minute")
def update_user(user_id):
    """Met à jour un utilisateur"""
    try:
        if user_id < 1:
            return jsonify({'error': 'ID invalide'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Validation et construction sécurisée de la requête
        updates = []
        params = []
        
        if 'name' in data:
            name = sanitize_input(data['name'], 100)
            if not validate_name(name):
                conn.close()
                return jsonify({'error': 'Nom invalide'}), 400
            updates.append('name = ?')
            params.append(name)
            
        if 'email' in data:
            email = sanitize_input(data['email'], 200)
            if not validate_email(email):
                conn.close()
                return jsonify({'error': 'Format d\'email invalide'}), 400
            # Vérifier si l'email est déjà utilisé par un autre utilisateur
            cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?', (email, user_id))
            if cursor.fetchone():
                conn.close()
                return jsonify({'error': 'Cet email est déjà utilisé'}), 409
            updates.append('email = ?')
            params.append(email)
        
        if not updates:
            conn.close()
            return jsonify({'error': 'Aucune donnée valide à mettre à jour'}), 400
        
        params.append(user_id)
        # Construction sécurisée de la requête (pas d'injection SQL possible)
        query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Utilisateur mis à jour avec succès',
            'id': user_id
        })
    except sqlite3.Error as e:
        app.logger.error(f"Database error in update_user: {e}")
        return jsonify({'error': 'Erreur lors de la mise à jour de l\'utilisateur'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in update_user: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_user(user_id):
    """Supprime un utilisateur"""
    try:
        if user_id < 1:
            return jsonify({'error': 'ID invalide'}), 400
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Utilisateur supprimé avec succès',
            'id': user_id
        })
    except sqlite3.Error as e:
        app.logger.error(f"Database error in delete_user: {e}")
        return jsonify({'error': 'Erreur lors de la suppression de l\'utilisateur'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in delete_user: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

@app.route('/api/stats', methods=['GET'])
@limiter.limit("30 per minute")
def get_stats():
    """Statistiques du serveur"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total = cursor.fetchone()[0]
        
        # Taille de la base de données
        db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        
        conn.close()
        
        # Ne pas exposer les chemins complets en production
        stats = {
            'total_users': total,
            'database_size_mb': round(db_size / (1024 * 1024), 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Informations supplémentaires uniquement en mode développement
        if DEBUG:
            stats['database_path'] = os.path.abspath(DB_PATH)
            stats['server_path'] = os.getcwd()
        
        return jsonify(stats)
    except sqlite3.Error as e:
        app.logger.error(f"Database error in get_stats: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des statistiques'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in get_stats: {e}")
        return jsonify({'error': 'Erreur serveur interne'}), 500

# Gestionnaire d'erreurs personnalisés
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Ressource non trouvée'}), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Erreur serveur interne'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Trop de requêtes. Veuillez réessayer plus tard.'}), 429

if __name__ == '__main__':
    print("=" * 60)
    print("🐍 SERVEUR DE TEST FLASK")
    print("=" * 60)
    print("🔧 Initialisation de la base de données...")
    init_db()
    print("✅ Base de données prête!")
    print(f"📁 Base de données: {DB_PATH}")
    print("=" * 60)
    print("🚀 Démarrage du serveur...")
    print(f"📍 Interface web: http://localhost:{PORT}")
    print(f"📡 API: http://localhost:{PORT}/api/")
    print(f"🐛 Mode debug: {DEBUG}")
    if not DEBUG:
        print("🔒 Sécurité: Rate limiting activé")
        print("🔒 Sécurité: Validation des entrées activée")
    print("=" * 60)
    print("💡 Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 60)
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
