from flask import Flask, request
import sqlite3
import boto3 # Utilisé pour simuler la connexion AWS avec les clés hardcodées

app = Flask(__name__)

# --- 1. Concaténation directement (SQL Injection) ---
@app.route("/search")
def search():
    user_input = request.args.get("q")
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()

# VULNERABILITE : 
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    cursor.execute(query)
    return str(cursor.fetchall())


# --- 2. Remote Code Execution (RCE) via eval() ---
@app.route("/calculator")
def calculator():
    # L'utilisateur envoie une expression, par exemple : ?expr=2*5
    user_expr = request.args.get("expr") 

    try: 
        # VULNERABILITE : DANGER ABSOLU : eval() exécute aveuglément l'input comme du code Python
        result = eval(user_expr)
        return f"Résultat du calcul : {result}"
    except Exception as e: 
        return f"Erreur : {str(e)}"
    

# --- 3. Secret Hardcodé ( AWS Access Keys ) --- 
# VULNERABILITE : Stocker des identifiants sensibles directement dans le code source
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7R89X2TB"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCY98ZTR45MLK"

@app.route("/backups")
def get_backups():
    try:
        # Simulation d'une connexion à AWS S3 en utilisant les clés hardcodées ci-dessus
        s3 = boto3.client(
            "s3",
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
        return "Connexion réussie au Bucket S3 de production (Simulée)"
    except Exception as e: 
        return f"Erreur de connexion : {str(e)}"
    
if __name__ == "__main__":
    app.run(debug = True, port = 5000)


