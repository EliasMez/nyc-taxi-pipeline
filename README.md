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
├── .github/workflows/nyc_taxi_pipeline.yml # Définition du pipeline CI/CD
│
├── snowflake_ingestion/
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
Création de la base de données (DW_NAME), des schémas (RAW_SCHEMA, STAGING_SCHEMA, FINAL_SCHEMA), du warehouse (WH_NAME), de l'utilisateur (USER_DEV) et attribution des permissions via le rôle ROLE_TRANSFORMER.

2. **Scraping** : <br>
Extraction des données sources via un script Python.

3. **Stockage temporaire** : <br>
Déposition des données brutes dans un buffer ou un stage Snowflake avant traitement.

4. **Chargement dans RAW_SCHEMA** : <br>
Ingestion des données brutes dans les tables du schéma RAW_SCHEMA pour conservation et traçabilité.

5. **Transformation avec dbt** : <br>
Nettoyage et préparation des données (RAW_SCHEMA → STAGING_SCHEMA), puis modélisation analytique dans FINAL_SCHEMA (tables dim_*, fact_*, et vues agrégées par heure/jour).

- **Gestion des doublons** : vérification via métadonnées avant traitement. <br>
<br>


## 📈 Monitoring et Qualité des données

- Logs détaillés dans GitHub Actions
- Table de métadonnées pour le suivi (scraped/staged/succes/failed)
- Alertes mail en cas d'échec de job
- Gestion des doublons : vérification via métadonnées avant traitement
<br>


## 🚀 Exécution Automatique (GitHub Actions)
Le pipeline s'exécute automatiquement **tous les 10 du mois à 2h**. <br>
Le pipeline peut aussi être déclenché manuellement. <br>
<br>


### ⚙️ Configuration
1. **Forkez** ce dépôt
 ```bash
 git clone https://github.com/EliasMez/nyc-taxi-pipeline.git
 ```
2. **Ajoutez les secrets :** `Settings` > `Secrets and variables` > `Actions` > `New repository secret`

| Secret | Description |
| :------------------- | :----------------------------------------------- |
| `SNOWFLAKE_USER`     | Nom d’utilisateur pour se connecter à Snowflake. |
| `SNOWFLAKE_PASSWORD` | Mot de passe associé à l’utilisateur Snowflake.  |
| `SNOWFLAKE_ACCOUNT`  | Identifiant du compte Snowflake.                 |
| `WH_NAME`            | Nom de l’entrepôt (warehouse) Snowflake.          |
| `DW_NAME`           | Nom de la base de données Snowflake.              |
| `RAW_SCHEMA`        | Nom du schéma contenant les données brutes.       |
| `STAGING_SCHEMA`    | Nom du schéma pour les données en transformation.|
| `FINAL_SCHEMA`      | Nom du schéma contenant les données finales.     |
| `PARQUET_FORMAT`    | Nom du format de fichier Parquet.                |
| `ROLE_TRANSFORMER`  | Rôle pour transformer les données.               |
| `USER_DEV`          | Nom d’utilisateur de développement.               |
| `PASSWORD_DEV`      | Mot de passe de l’utilisateur de développement.   |
<br>


### 🔐 Sécurité
- Les secrets sont chiffrés dans GitHub
- Rôle Snowflake avec permissions minimales nécessaires
<br>


### 🐛 Dépannage Rapide
- Échec connexion Snowflake : Vérifier les secrets GitHub
- Timeout scraping : Vérifier l'accès aux URLs sources
- Erreur dbt : Consulter les logs détaillés du job
