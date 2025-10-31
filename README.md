# 🚕 NYC Taxi Data Pipeline

Ce workflow GitHub Actions automatise le pipeline de données de bout en bout, depuis l'initialisation de l'infrastructure Snowflake jusqu'à la production de tables et vues analytiques en utilisant python et dbt.
<br> <br>


## 📋 Prérequis

- Compte **Snowflake** avec droits **SECURITYADMIN** et **SYSADMIN**
- Dépôt **GitHub** avec **secrets configurés** (voir partie configuration)
- Accès sources de données NYC Taxi : **https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**
<br>


## 🏗️ Architecture Technique

- **Orchestration** : GitHub Actions
- **Data Warehouse** : Snowflake
- **Transformation** : dbt
- **Langage** : Python
<br>

## 📁 Structure du Projet
```bash
nyc-taxi-pipeline/
├── .github/workflows/nyc_taxi_pipeline.yml
│
├── snowflake_ingestion/
│ ├── sql
│ │ ├── 01_init/
│ │ ├── 02_scraping/
│ │ ├── 03_stage/
│ │ └── 04_load/
│ │
│ ├── 01_init_data_warehouse.py
│ ├── 02_scrape_links.py
│ ├── 03_upload_stage.py
│ └── 04_load_to_table.py
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
 
1. **Initialisation de l'environnement Snowflake** : <br>
Création de la base de données, du schéma, du data warehouse, de l'utilisateur, création et attribution des permissions via le rôle.

2. **Scraping** : <br>
Extraction des données sources via un script Python.

3. **Stockage temporaire** : <br>
Ingestion des données brutes dans un buffer ou un stage Snowflake avant traitement.

4. **Chargement des données** : <br>
Chargement des données brutes dans la table du du schéma RAW.

5. **Transformation avec dbt** : <br>
Nettoyage et préparation des données dans la table di schéma STAGING, puis modélisation dans les tables du schéma FINAL (dimensions, fait et vues agrégées).
<br>


## 📈 Monitoring et Qualité des données

- Logs détaillés dans GitHub Actions (personnalisation du niveau de log possible - voir partie Configuration Optionnelle)
- Table de métadonnées pour le suivi (scraped/staged/succes/failed)
- Alertes mail en cas d'échec et d'arrêt de job
- Gestion des doublons : vérification via métadonnées avant traitement.
<br>


## 🚀 Exécution Automatique (GitHub Actions)
Le pipeline s'exécute automatiquement **tous les 1 du mois à 10h**. <br>
Le pipeline peut aussi être déclenché manuellement. <br>
<br>


### ⚙️ Configuration
1. **Forkez** ce dépôt : https://github.com/EliasMez/nyc-taxi-pipeline


2. **Ajoutez les secrets OBLIGATOIRES :** `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_USER` | Nom d'utilisateur Snowflake |
| `SNOWFLAKE_PASSWORD` | Mot de passe utilisateur Snowflake |
| `SNOWFLAKE_ACCOUNT` | Identifiant du compte Snowflake |
| `PASSWORD_DEV` | Mot de passe de l'utilisateur de développement |


3. **Ajoutez les variables OPTIONNELLES :** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

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
<br>
<br>

### 🔐 Sécurité
- Les secrets sont chiffrés dans GitHub
- Rôle Snowflake avec permissions minimales nécessaires
<br>


### 🐛 Dépannage Rapide
- Échec connexion Snowflake : Vérifier les secrets GitHub
- Timeout scraping : Vérifier l'accès aux URLs sources
- Erreur dbt : Consulter les logs détaillés du job
