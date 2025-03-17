# Utiliser l'image officielle de Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du projet
COPY . .

# Exposer le port 9000
EXPOSE 9000

# Lancer l'application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]
