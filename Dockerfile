# --- 4 : Utilisation d'une image de base obsolète contenant des failles de sécurité (CVE)
FROM python:3.8-slim 

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask boto3

EXPOSE 5000

CMD [ "python", "app.py" ]