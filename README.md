# 🛡️ Secure CI/CD Pipeline - DevSecOps Lab

> ⚠️ **AVERTISSEMENT** : Cette application contient des vulnérabilités **intentionnelles** à des fins éducatives. Ne pas déployer en l'état.

## Tableau de bord de sécurité

![Total Alerts](/docs/images/total_alerts_badge.png)

*L'infrastructure centralise un total de **304 alertes actives** consolidées au format SARIF dans l'onglet Security de GitHub.*

---

## Contexte du Projet

Projet réalisé en complément des parcours **TryHackMe Secure Software Development** et **CI/CD Security**, dans une démarche de mise en pratique du DevSecOps.

**L'objectif** : Coder une petite application Flask volontairement vulnérable (eval sur input, injection SQL, secrets hardcodés, image Docker obsolète) et construire un pipeline GitHub Actions capable de tout détecter automatiquement avant un éventuel déploiement.

**Le principe appliqué** : **Shift Left** — détecter les failles dès le commit, pas après la mise en production.

---

## Pipeline de Sécurité

Les 3 scanners s'exécutent en parallèle à chaque `push` pour minimiser le temps total du pipeline. Pipeline complet exécuté avec succès en seulement **47 secondes**.

Push / Pull Request
│
├── Semgrep (SAST) ──────→ Détecte SQLi, eval(), mauvaises pratiques
├── Gitleaks (Secrets) ───→ Détecte les clés AWS hardcodées et l'historique
└── Trivy (Container) ────→ Détecte les CVE de l'image Docker
│
└── Résultats → GitHub Security tab (format SARIF)


![Pipeline Status](/docs/images/pipeline_complet.png)

*Visualisation du succès de l'orchestration parallèle sous GitHub Actions.*

---

## Stack Technique

| Outil | Rôle |
|-------|------|
| **Python / Flask** | Application vulnérable intentionnelle |
| **Docker** | Conteneurisation avec image obsolète (CVE) |
| **GitHub Actions** | Orchestration automatisée du pipeline CI/CD |
| **Semgrep** | SAST — Analyse statique du code source applicatif |
| **Gitleaks** | Détection de secrets dans le code et l'historique Git |
| **Trivy** | Container Scanning — Scan de vulnérabilités CVE dans l'image Docker |
| **SARIF** | Format standardisé de remontée des findings dans GitHub Security |

---

## Vulnérabilités Démontrées

| # | Type | Fichier | Description |
|---|------|---------|-------------|
| **1** | SQL Injection | `app.py` | Concaténation directe de l'input utilisateur dans une requête SQL |
| **2** | RCE via `eval()` | `app.py` | Exécution de code arbitraire via l'entrée utilisateur |
| **3** | Secrets hardcodés | `app.py` | Clés AWS directement dans le code source |
| **4** | Image Docker obsolète | `Dockerfile` | Base `python:3.8-slim` avec des CVE connues |
| **5** | Mode debug Flask | `app.py` | Mode Debug activé, exposant la console interactive |

---

## Détail des Scans & Résultats

### 1. Semgrep — SAST sur le code Flask
Semgrep remonte **6 findings ouverts** dans le panneau *Code scanning*:
* Injection `eval()` sur input utilisateur (Error)
* Injection SQL par concaténation de strings (Error)
* Mode debug Flask activé
* Token AWS hardcodé
* Format string directement retourné
* User-eval supplémentaire

![Semgrep Findings](/docs/images/semgrep_alertes.png)

*Aperçu des alertes de sécurité de niveau applicatif identifiées par Semgrep.*

### 2. Gitleaks — Secrets dans l'historique Git
Détection et extraction de **2 secrets critiques** avec traçabilité complète : hash du commit, identité de l'auteur, date, fichier et lignes exactes (36 et 37). Un atout indispensable pour un workflow d'Incident Response efficace.

![Gitleaks Dashboard](/docs/images/gitleaks_resume.png)

*Rapport d'interception Gitleaks détaillant l'exposition des clés AWS.*

### 3. Trivy — Container Scanning
Plus de **290 vulnérabilités** remontées sur l'image Docker `python:3.8-slim`, dont des CVE critiques d'exécution de code à distance (RCE) et de corruption de mémoire (*heap buffer overflow*) sur `openssl` ainsi que des débordements d'entiers (*integer overflow*) sur `sqlite`. C'est la démonstration directe de l'impact de la dette technique sur l'infrastructure.

![Trivy CVE List](/docs/images/trivy_cve.png)

*Extrait des vulnérabilités de niveau OS et paquets systèmes déterrées par Trivy.*

---

## Focus DevSecOps : La Défense en Profondeur

Un point clé de ce laboratoire est la mise en évidence de la **complémentarité des outils**. Lors de l'exposition des credentials AWS, la faille a été interceptée par **3 couches de défense distinctes** :
1. **Gitleaks** dans l'historique des commits Git.
2. **Semgrep** dans la logique du code source Python (`app.py`).
3. **Trivy** au sein même du système de fichiers du conteneur Docker lors du build (Alertes #303 et #304).

Cette redondance d'analyse applique concrètement le principe de **défense en profondeur**, empêchant tout secret d'atteindre la production.

---

## Compétences mises en pratique

Ce projet valide les acquis pratiques des modules **TryHackMe** suivants :
* **Secure Software Development** : Intro to DevSecOps, SDLC, SSDLC.
* **Pipeline & Projets CI/CD** : Security of the Pipeline, Intro to Pipeline Automation, Source Code Security, CI/CD and Build Security.
* **Security in the Pipeline** : Dependency Management, SAST, DAST, Mother's Secret.

---

## Avertissement légal

Cette application est volontairement vulnérable et destinée à un usage strictement éducatif. 

---

Fait par Joshua Prevost · 2026