#!/bin/bash

# Script de démarrage du serveur Flask
# Emplacement: /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test

echo "=================================================="
echo "🚀 Démarrage du serveur Flask"
echo "=================================================="

# Se placer dans le bon répertoire
cd /Users/sithidet/Desktop/01_En_Cours/Bob/serveur-test

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé!"
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    
    echo "📥 Installation des dépendances..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Installation terminée!"
else
    echo "✅ Environnement virtuel trouvé"
    source venv/bin/activate
fi

# Vérifier si les dépendances sont installées
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installation des dépendances manquantes..."
    pip install -r requirements.txt
fi

echo "=================================================="
echo "🐍 Lancement de l'application Flask..."
echo "=================================================="

# Lancer l'application
python3 app.py
