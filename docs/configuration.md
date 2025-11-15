## **Forker**
Forkez ce dépôt : https://github.com/EliasMez/nyc-taxi-pipeline
<br>

## **Ajouter les secrets**
Ajoutez les secrets OBLIGATOIRES : `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_USER` | Nom d'utilisateur Snowflake |
| `SNOWFLAKE_PASSWORD` | Mot de passe utilisateur Snowflake |
| `SNOWFLAKE_ACCOUNT` | Identifiant du compte Snowflake |
| `PASSWORD_DEV` | Mot de passe de l'utilisateur de développement |

## **Ajouter les variables**
Ajoutez les variables OPTIONNELLES : `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

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