# Secure CI/CD Pipeline 

> **AVERTISSEMENT** : Cette application contient des vulnérabilités **intentionnelles** à des fins éducatives.

## Vue d'ensemble

Pipeline CI/CD sécurisé qui détecte automatiquement les vulnérabilités d'une application Python volontairement vulnérable. Les résultats remontent dans l'onglet **Security** de GitHub via le format SARIF.

## Vulnérabilités démontrées

| # | Type | Fichier | Description |
|---|------|---------|-------------|
| 1 | SQL Injection | `app.py` | Concaténation directe de l'input utilisateur dans une requête SQL |
| 2 | RCE via `eval()` | `app.py` | Exécution de code arbitraire via l'entrée utilisateur |
| 3 | Secrets hardcodés | `app.py` | Clés AWS directement dans le code source |
| 4 | Image Docker obsolète | `Dockerfile` | `python:3.8-slim` avec des CVE connues |

## Pipeline de sécurité

```
Push / Pull Request
        │
        ├── Semgrep (SAST) ──────→ Détecte SQLi, eval(), mauvaises pratiques de code
        ├── Gitleaks (Secrets) ───→ Détecte les clés AWS hardcodées dans le code
        └── Trivy (Container) ────→ Détecte les CVE dans l'image Docker
                    │
                    └── Résultats → GitHub Security tab (format SARIF)
```

## Stack technique

| Outil | Rôle |
|-------|------|
| Python / Flask | Application vulnérable intentionnelle |
| Docker | Conteneurisation avec image obsolète (CVE) |
| GitHub Actions | Orchestration du pipeline CI/CD |
| Semgrep | SAST — analyse statique du code |
| Gitleaks | Détection de secrets dans le code et l'historique Git |
| Trivy | Scan de vulnérabilités CVE dans l'image Docker |

## Structure du projet

```
.
├── app.py                          # Application Flask vulnérable
├── Dockerfile                      # Image de base obsolète (intentionnel)
├── requirements.txt                # Dépendances Python
└── .github/
    └── workflows/
        └── devsecops.yml           # Pipeline GitHub Actions
```

## Résultats attendus

Après chaque push, GitHub Actions exécute les 3 scans en parallèle.  
Les findings apparaissent dans **Security → Code scanning alerts** du repository.

- **Semgrep** : détecte la SQLi et le `eval()` dangereux
- **Gitleaks** : détecte les clés AWS hardcodées
- **Trivy** : remonte les CVE CRITICAL/HIGH de `python:3.8-slim`
