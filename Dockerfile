# Stage 1: Builder
FROM python:3.11-slim as builder

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Créer un environnement virtuel et installer les dépendances
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn python-dotenv

# Stage 2: Runtime
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="sithidet"
LABEL description="Flask Test Server with SQLite"
LABEL version="1.0"

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 flaskuser && \
    mkdir -p /app/data && \
    chown -R flaskuser:flaskuser /app

# Définir le répertoire de travail
WORKDIR /app

# Copier l'environnement virtuel depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Copier les fichiers de l'application
COPY --chown=flaskuser:flaskuser app.py .
COPY --chown=flaskuser:flaskuser docker-entrypoint.sh .

# Rendre le script d'entrée exécutable
RUN chmod +x docker-entrypoint.sh

# Définir les variables d'environnement
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    DB_PATH=/app/data/test.db \
    PORT=5001

# Exposer le port
EXPOSE 5001

# Changer vers l'utilisateur non-root
USER flaskuser

# Volume pour la persistance des données
VOLUME ["/app/data"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/api/health')" || exit 1

# Point d'entrée
ENTRYPOINT ["./docker-entrypoint.sh"]

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]