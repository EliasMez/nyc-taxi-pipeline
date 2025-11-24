# 📈 Gouvernance des données

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 Monitoring
- Logs détaillés dans GitHub Actions.  
- Alertes e-mail en cas d’échec ou d’annulation du workflow.  
- Suivi de l’état via une table de métadonnées indiquant chaque étape (*scraped / staged / success / failed*).

## ✅ Qualité des données
- Tests **dbt** garantissant l’intégrité, la cohérence et la validité des données.  
- Gestion des doublons via une vérification systématique des métadonnées.

## 🧪 Qualité du code
- Tests unitaires avec **Pytest**.  
- Validation SQL avec **SQLFluff**.  
- Docstrings et doctests pour la documentation des fonctions.  
- <a href="https://eliasmez.github.io/nyc-taxi-pipeline/docstrings/">📚 Documentation technique</a>

## 🔐 Sécurité
- Secrets chiffrés dans les logs.  
- Utilisation des **GitHub Secrets**.  
- Permissions minimales appliquées dans Snowflake.  
- Analyse statique avec **CodeQL**.  
- Mises à jour de sécurité automatisées via **Dependabot**.