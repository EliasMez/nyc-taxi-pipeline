# NYC Taxi Data Pipeline

Ce workflow GitHub Actions automatise le pipeline de données de bout en bout, depuis l'initialisation de l'infrastructure Snowflake jusqu'à la production de tables et vues analytiques en utilisant python et dbt.
<br> <br>
<a href="https://eliasmez.github.io/nyc-taxi-pipeline">📚 Documentation complète en ligne</a>
<br>

## 📊 Source des Données

[**TLC Trip Record Data**](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - Commission des Taxis et Limousines de NYC

Les données incluent :

- Dates/heures de prise en charge et dépose
- Localisations GPS des trajets
- Distances, tarifs détaillés, types de paiement
- Nombre de passagers rapporté par le chauffeur

*Les données sont collectées par les fournisseurs technologiques autorisés et fournies à la TLC. La TLC ne garantit pas l'exactitude de ces données.*

## 📄 Licence

Ce projet est sous licence MIT. Les données source sont fournies par la [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) et soumises à leurs conditions d'utilisation.
<br>
<br>
<br>


# 🏛️ Architecture

## 🏗️ Architecture Technique

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)]()
[![Snowflake](https://img.shields.io/badge/Snowflake-Data_Warehouse-29B5E8?logo=snowflake&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)]()
[![dbt](https://img.shields.io/badge/dbt-Transformations-FF694B?logo=dbt&logoColor=white)]()

- **Orchestration** : GitHub Actions
- **Data Warehouse** : Snowflake
- **Transformation** : dbt
- **Langage** : Python
<br>

## 📁 Structure du Projet
```bash
nyc-taxi-pipeline/
├── .github/
│ ├── workflows/
│ │ ├── nyc_taxi_pipeline.yml
│ │ ├── codeql.yml
│ │ ├── python_code_tests.yml
│ │ ├── release.yml
│ │ └── sqlfluff.yml
│ │
│ └── dependabot.yml
│
├── docs/
│
├── snowflake_ingestion/
│ ├── init_data_warehouse.py
│ ├── scrape_links.py
│ ├── upload_stage.py
│ ├── load_to_table.py
│ │
│ ├── sql/
│ │ ├── init/
│ │ ├── scraping/
│ │ ├── stage/
│ │ └── load/
│ │
│ └── tests/
│
└── dbt_transformations/
  └── NYC_Taxi_dbt/
    └── models/
      ├── staging/
      ├── final/
      └── marts/
```
<br>


## 📊 Flux de traitement

### Pipeline Principal :

**NYC Taxi Data Pipeline**  
Pipeline d'ingestion exécuté mensuellement :
<br>

1. **Snowflake Infra Init**  
   Initialisation de l'infrastructure Snowflake (base, schémas, warehouse, rôle, utilisateur).
2. **Scrape Links**  
   Scraping et récupération des liens sources.
3. **Upload to Stage**  
   Upload des fichiers bruts dans le stage Snowflake.
4. **Load to Table**  
   Chargement des données dans la table du schéma RAW.
5. **Run dbt Transformations**  
   Transformations dbt (STAGING puis FINAL).
6. **Run dbt Tests**  
   Exécution des tests dbt pour valider les modèles.
   
### Pipelines Qualité

- **CodeQL Security Scan** <br> Analyse statique du code Python à l’aide de CodeQL afin de détecter des vulnérabilités sur chaque push ou pull request vers `dev` et `main`.
- **Dependabot Updates** <br> Mises à jour automatisées des dépendances Python et GitHub Actions selon une planification trimestrielle.
- **pages-build-deployment** <br> Déploiement automatique de la documentation du projet via GitHub Pages.
- **Python Code Tests** <br> Exécution des tests unitaires Pytest sur chaque push ou pull request vers `dev` et `main`.
- **Release** <br> Versioning automatique, génération du changelog et publication des releases via Python Semantic Release sur chaque push ou pull request vers `main`.
- **SQL Code Quality** <br> Linting automatique du code SQL (modèles dbt et scripts Snowflake) avec SQLFluff sur chaque push ou pull request vers `dev` et `main`.
<br>
<br>


# 💻 Démarrage du Projet

## 📋 Prérequis

- Compte **Snowflake** avec droits **SECURITYADMIN** et **SYSADMIN**
- Dépôt **GitHub** avec **secrets configurés** (voir partie configuration)
- Accès sources de données NYC Taxi : **https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**
<br>


## 🚀 Exécution
- Automatique : tous les 1 du mois à 10h
- Manuel : via GitHub Actions interface
<br>


## ⚙️ Configuration
1. **Forkez** ce dépôt : https://github.com/EliasMez/nyc-taxi-pipeline
<br>

2. **Ajoutez les secrets OBLIGATOIRES :** `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_USER` | Nom d'utilisateur Snowflake |
| `SNOWFLAKE_PASSWORD` | Mot de passe utilisateur Snowflake |
| `SNOWFLAKE_ACCOUNT` | Identifiant du compte Snowflake |
| `PASSWORD_DEV` | Mot de passe de l'utilisateur de développement |
<br>

3. **Personnalisez les variables OPTIONNELLES :** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `WH_NAME` | Nom du data warehouse | `NYC_WH` |
| `DW_NAME` | Nom de la base de données | `NYC_TAXI_DW` |
| `RAW_SCHEMA` | Schéma des données brutes | `RAW` |
| `STAGING_SCHEMA` | Schéma des données nettoyées | `STAGING` |
| `FINAL_SCHEMA` | Schéma des données finales | `FINAL` |
| `PARQUET_FORMAT` | Format de fichier Parquet | `PARQUET_FORMAT` |
| `ROLE_TRANSFORMER` | Rôle pour les transformations | `TRANSFORMER` |
| `USER_DEV` | Utilisateur de développement | `USER_DEV` |
| `METADATA_TABLE` | Table de métadonnées | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | Table des données brutes | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | Table de staging | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | Niveau de logging | `INFO` |
| `SCRAPING_YEAR` | Date de début du scraping (>2000 et <année courante)| année courante |
| `TIMEZONE` | Fuseau horaire qui définit le décalage horaire par rapport à UTC | `UTC` |
| `GH_RELEASE_TOKEN` | Token GitHub pour le versionnement automatique (nécessaire seulement si vous utilisez le workflow Release) | ⚠️ non défini |
<br>

⚠️ **Workflow Release (Semantic Release)**  
Le workflow **Release** nécessite un token GitHub (`GH_RELEASE_TOKEN`) pour fonctionner.  
Si ce token n’est pas défini, **le workflow échouera systématiquement** lors de l’étape de publication.

**Option 1** : Désactiver le workflow *Release*
Si vous n’avez pas besoin du versionnement automatique de code : `Actions` → `Release` → **Disable workflow**

**Option 2** : Créer un Personal Access Token (recommandé si vous gardez le workflow)
1. Allez dans :  `Settings` → `Developer settings` → `Personal access tokens` → **Tokens (classic)**  
2. Créez un token avec les permissions `repo`  
3. Ajoutez-le comme secret : `Settings` → `Secrets and variables` → `Actions` → **New repository secret**  
   - Nom : `GH_RELEASE_TOKEN`  
   - Valeur : *votre token*
<br>


## 🔧 Dépannage Rapide
- Échec connexion Snowflake : Vérifier les secrets GitHub
- Timeout scraping : Vérifier l'accès aux URLs sources
- Erreur dbt : Consulter les logs détaillés du job
- Passer la valeur de la variable `LOGGER_LEVEL` à `DEBUG` pour voir les logs détaillés
<br>
<br>


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




