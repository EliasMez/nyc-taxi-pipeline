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