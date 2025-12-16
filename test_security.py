#!/usr/bin/env python3
"""
Script de test de sécurité pour Bobathon Lab
Teste les vulnérabilités corrigées et les mesures de sécurité
"""

import requests
import json
import time
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)

# Configuration
BASE_URL = "http://localhost:8080"  # Modifier selon votre configuration
API_URL = f"{BASE_URL}/api"

def print_test(test_name):
    """Affiche le nom du test"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}TEST: {test_name}")
    print(f"{Fore.CYAN}{'='*60}")

def print_success(message):
    """Affiche un message de succès"""
    print(f"{Fore.GREEN}✓ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"{Fore.RED}✗ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"{Fore.YELLOW}ℹ {message}")

def test_sql_injection():
    """Test de protection contre l'injection SQL"""
    print_test("Protection contre l'injection SQL")
    
    # Tentatives d'injection SQL
    payloads = [
        {"name": "Test", "email": "test@test.com' OR '1'='1"},
        {"name": "Test'; DROP TABLE users; --", "email": "test@test.com"},
        {"name": "Test", "email": "test@test.com' UNION SELECT * FROM users--"},
    ]
    
    for payload in payloads:
        try:
            response = requests.post(f"{API_URL}/users", json=payload, timeout=5)
            if response.status_code == 400:
                print_success(f"Injection SQL bloquée: {payload['email'][:50]}")
            else:
                print_error(f"Injection SQL non bloquée: {response.status_code}")
        except Exception as e:
            print_error(f"Erreur lors du test: {e}")

def test_xss_protection():
    """Test de protection contre XSS"""
    print_test("Protection contre XSS")
    
    xss_payloads = [
        {"name": "<script>alert('XSS')</script>", "email": "test@test.com"},
        {"name": "<img src=x onerror=alert('XSS')>", "email": "test@test.com"},
        {"name": "Test", "email": "<script>alert('XSS')</script>@test.com"},
    ]
    
    for payload in xss_payloads:
        try:
            response = requests.post(f"{API_URL}/users", json=payload, timeout=5)
            if response.status_code == 400:
                print_success(f"XSS bloqué: {payload['name'][:50]}")
            else:
                print_info(f"Réponse: {response.status_code} - Vérifier le nettoyage")
        except Exception as e:
            print_error(f"Erreur lors du test: {e}")

def test_input_validation():
    """Test de validation des entrées"""
    print_test("Validation des entrées utilisateur")
    
    invalid_inputs = [
        {"name": "", "email": "test@test.com"},  # Nom vide
        {"name": "Test", "email": "invalid-email"},  # Email invalide
        {"name": "A" * 200, "email": "test@test.com"},  # Nom trop long
        {"name": "Test123!@#$%", "email": "test@test.com"},  # Caractères invalides
        {"name": "Test", "email": ""},  # Email vide
    ]
    
    for payload in invalid_inputs:
        try:
            response = requests.post(f"{API_URL}/users", json=payload, timeout=5)
            if response.status_code == 400:
                print_success(f"Entrée invalide rejetée: {str(payload)[:50]}")
            else:
                print_error(f"Entrée invalide acceptée: {response.status_code}")
        except Exception as e:
            print_error(f"Erreur lors du test: {e}")

def test_rate_limiting():
    """Test de limitation de taux"""
    print_test("Rate Limiting")
    
    print_info("Envoi de 15 requêtes rapides (limite: 10/minute)...")
    blocked_count = 0
    success_count = 0
    
    for i in range(15):
        try:
            payload = {
                "name": f"RateTest{i}",
                "email": f"ratetest{i}@test.com"
            }
            response = requests.post(f"{API_URL}/users", json=payload, timeout=5)
            
            if response.status_code == 429:
                blocked_count += 1
            elif response.status_code == 201:
                success_count += 1
            
            time.sleep(0.1)  # Petit délai entre les requêtes
        except Exception as e:
            print_error(f"Erreur lors du test: {e}")
    
    print_info(f"Requêtes réussies: {success_count}")
    print_info(f"Requêtes bloquées: {blocked_count}")
    
    if blocked_count > 0:
        print_success("Rate limiting fonctionne correctement")
    else:
        print_error("Rate limiting ne fonctionne pas")

def test_email_uniqueness():
    """Test de l'unicité des emails"""
    print_test("Unicité des emails")
    
    email = f"unique_test_{int(time.time())}@test.com"
    payload = {"name": "UniqueTest", "email": email}
    
    try:
        # Première création
        response1 = requests.post(f"{API_URL}/users", json=payload, timeout=5)
        if response1.status_code == 201:
            print_success("Premier utilisateur créé")
            
            # Tentative de duplication
            time.sleep(1)  # Attendre pour éviter le rate limiting
            response2 = requests.post(f"{API_URL}/users", json=payload, timeout=5)
            if response2.status_code == 409:
                print_success("Duplication d'email bloquée (409 Conflict)")
            else:
                print_error(f"Duplication d'email non bloquée: {response2.status_code}")
        else:
            print_error(f"Échec de création du premier utilisateur: {response1.status_code}")
    except Exception as e:
        print_error(f"Erreur lors du test: {e}")

def test_security_headers():
    """Test des en-têtes de sécurité HTTP"""
    print_test("En-têtes de sécurité HTTP")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        headers = response.headers
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'Content-Security-Policy',
        ]
        
        for header in security_headers:
            if header in headers:
                print_success(f"{header}: {headers[header]}")
            else:
                print_info(f"{header}: Non présent (peut être géré par Nginx)")
    except Exception as e:
        print_error(f"Erreur lors du test: {e}")

def test_error_handling():
    """Test de la gestion des erreurs"""
    print_test("Gestion des erreurs")
    
    try:
        # Test 404
        response = requests.get(f"{API_URL}/nonexistent", timeout=5)
        if response.status_code == 404:
            data = response.json()
            if 'error' in data and 'Ressource non trouvée' in data['error']:
                print_success("Erreur 404 gérée correctement")
            else:
                print_error("Message d'erreur 404 incorrect")
        
        # Test utilisateur inexistant
        response = requests.get(f"{API_URL}/users/99999", timeout=5)
        if response.status_code == 404:
            print_success("Utilisateur inexistant géré correctement")
        
        # Test données invalides
        response = requests.post(f"{API_URL}/users", json={}, timeout=5)
        if response.status_code == 400:
            print_success("Données invalides gérées correctement")
    except Exception as e:
        print_error(f"Erreur lors du test: {e}")

def test_valid_user_creation():
    """Test de création d'utilisateur valide"""
    print_test("Création d'utilisateur valide")
    
    timestamp = int(time.time())
    payload = {
        "name": f"Valid User {timestamp}",
        "email": f"valid{timestamp}@test.com"
    }
    
    try:
        response = requests.post(f"{API_URL}/users", json=payload, timeout=5)
        if response.status_code == 201:
            data = response.json()
            print_success(f"Utilisateur créé avec succès: ID {data.get('id')}")
            return data.get('id')
        else:
            print_error(f"Échec de création: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Erreur lors du test: {e}")
        return None

def run_all_tests():
    """Exécute tous les tests de sécurité"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}TESTS DE SÉCURITÉ - BOBATHON LAB")
    print(f"{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.YELLOW}URL de base: {BASE_URL}")
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Serveur accessible")
        else:
            print_error("Serveur non accessible")
            return
    except Exception as e:
        print_error(f"Impossible de se connecter au serveur: {e}")
        print_info("Assurez-vous que le serveur est démarré")
        return
    
    # Exécuter les tests
    test_sql_injection()
    time.sleep(1)
    
    test_xss_protection()
    time.sleep(1)
    
    test_input_validation()
    time.sleep(1)
    
    test_email_uniqueness()
    time.sleep(1)
    
    test_security_headers()
    time.sleep(1)
    
    test_error_handling()
    time.sleep(1)
    
    test_valid_user_creation()
    time.sleep(1)
    
    test_rate_limiting()  # En dernier car il fait beaucoup de requêtes
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}TESTS TERMINÉS")
    print(f"{Fore.MAGENTA}{'='*60}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n{Fore.RED}Erreur fatale: {e}")

# Made with Bob
