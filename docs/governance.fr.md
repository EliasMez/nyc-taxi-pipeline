# 📈 Gouvernance des données

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 Monitoring
- Logs détaillés dans GitHub Actions.
- Alertes e-mail en cas d'échec ou d'annulation du workflow.
- Suivi de l'état via une table de métadonnées indiquant chaque étape (*scraped / staged / success / failed*).

## ✅ Qualité des données
- Tests **dbt** garantissant l'intégrité, la cohérence et la validité des données.
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

## 👥 Gestion des accès et des rôles

L'accès à l'entrepôt repose sur le **principe du moindre privilège** : chaque rôle dispose uniquement des droits strictement nécessaires à sa fonction.

### Rôles système Snowflake

Prédéfinis par la plateforme, utilisés uniquement lors de l'initialisation de l'infrastructure :

| Rôle | Utilisation |
|------|-------------|
| `SYSADMIN` | Création du warehouse, de la database et des schémas ; attribution des privilèges |
| `SECURITYADMIN` | Création des rôles métier et des comptes utilisateurs |
| `ACCOUNTADMIN` | Configuration du Time Travel |

### Rôles métier

| Rôle | Utilisateur | Accès | Cas d'usage |
|------|-------------|-------|-------------|
| **TRANSFORMER** | USER_DEV | Tous les schémas | Pipeline ETL dbt et ingestion Python |
| **BI_ANALYST** | USER_BI_ANALYST | Lecture SCHEMA_FINAL (tables + vues) | Rapports BI |
| **DATA_SCIENTIST** | USER_DATA_SCIENTIST | Lecture SCHEMA_STAGING + SCHEMA_FINAL (tables) | Analyse exploratoire |
| **MART_CONSUMER** | USER_MART_CONSUMER | Lecture vues SCHEMA_FINAL uniquement | Consommation des agrégats analytiques |

## 📋 Indicateurs de service (SLA)

### SLA Snowflake (fournisseur)

Deux seuils de disponibilité mensuelle s'appliquent simultanément :

| Seuil | Condition | Pénalités |
|-------|-----------|-----------|
| **99,9 %** | Panne > 43 min ou > 1 % d'erreurs | 10 % (< 99,9 %) → 25 % (< 99,0 %) → 50 % (< 95,0 %) |
| **99,99 %** | Pannes courtes (4–43 min, > 10 % d'erreurs) cumulées > 43 min | Violation du seuil 99,9 % |

### SLA projet

| Indicateur | Objectif |
|-----------|---------|
| Durée du pipeline mensuel | < 30 min |
| Taux de succès du chargement | 100 % |
| Taux de réussite des tests dbt | 100 % |
| Fraîcheur des données | < 30 jours |
| Résolution des incidents P1 | < 48 h |

## 💾 Sauvegardes

Le **Time Travel Snowflake** (1 jour sur compte Standard) permet de récupérer des modifications récentes mais ne constitue pas un backup : aucune copie indépendante n'est créée. Les politiques ci-dessous assurent une rétention longue durée sur des copies distinctes.

| Objet | Fréquence | Rétention |
|-------|-----------|-----------|
| Base complète `NYC_TAXI_DW` | Mensuelle | 180 jours |
| Table `YELLOW_TAXI_TRIPS_RAW` | Mensuelle | **730 jours** (par défaut) |
| Schéma `FINAL` | Mensuelle | 90 jours |

- **730 jours** pour la table RAW : données sources potentiellement irremplaçables si le site NYC TLC ne conserve plus l'historique.
- **90 jours** pour le schéma FINAL : reconstructible depuis RAW via dbt.
- Durées configurables via les variables `RAW_TABLE_BACKUP_POLICY_DAYS`, `FULL_BACKUP_POLICY_DAYS`, `FINAL_SCHEMA_BACKUP_POLICY_DAYS`.
