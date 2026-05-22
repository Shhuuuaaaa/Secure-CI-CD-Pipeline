# --- 4 : Utilisation d'une image de base obsolète contenant des failles de sécurité (CVE) ---
# VULNÉRABILITÉ : Utilisation d'un image de base obsolète (Python 3.8 n'est plus supporté)
FROM python:3.8-slim 

# CORRECTION : Utiliser une image de base moderne et activement maintenue
# FROM python:3.12-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask boto3

EXPOSE 5000

CMD [ "python", "app.py" ]