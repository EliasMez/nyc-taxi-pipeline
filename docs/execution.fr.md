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
| `PASSWORD_BI` | Mot de passe utilisateur Analyste BI |
| `PASSWORD_DS` | Mot de passe utilisateur Data Scientist |
| `PASSWORD_MC` | Mot de passe utilisateur Consommateur Mart |
| `GH_RELEASE_TOKEN` | Token GitHub pour le versionnement automatique (nécessaire seulement si vous utilisez le workflow Release) |
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

3. **Personnalisez les variables OPTIONNELLES :** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `WH_NAME` | Nom du data warehouse | `NYC_WH` |
| `DW_NAME` | Nom de la base de données | `NYC_TAXI_DW` |
| `RAW_SCHEMA` | Schéma des données brutes | `RAW` |
| `STAGING_SCHEMA` | Schéma des données nettoyées | `STAGING` |
| `FINAL_SCHEMA` | Schéma des données finales | `FINAL` |
| `PARQUET_FORMAT` | Format de fichier Parquet | `PARQUET_FORMAT` |
| `COMPUTE_SIZE` | Puissance de calcul de l'entrepôt de données | `X-SMALL` |
| `ROLE_TRANSFORMER` | Rôle pour les transformations | `TRANSFORMER` |
| `ROLE_BI_ANALYST` | Nom du rôle Analyste BI | `ROLE_BI_ANALYST` |
| `ROLE_DATA_SCIENTIST` | Nom du rôle Data Scientist | `ROLE_DATA_SCIENTIST` |
| `ROLE_MART_CONSUMER` | Nom du rôle Consommateur Mart | `ROLE_MART_CONSUMER` |
| `USER_DEV` | Utilisateur de développement | `USER_DEV` |
| `USER_BI_ANALYST` | Nom d'utilisateur Analyste BI | `USER_BI_ANALYST` |
| `USER_DATA_SCIENTIST` | Nom d'utilisateur Data Scientist | `USER_DATA_SCIENTIST` |
| `USER_MART_CONSUMER` | Nom d'utilisateur Consommateur Mart | `USER_MART_CONSUMER` |
| `METADATA_TABLE` | Table de métadonnées | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | Table des données brutes | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | Table de staging | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | Niveau de logging | `INFO` |
| `SCRAPING_YEAR` | Date de début du scraping (>2000 et <année courante)| année courante |
| `TIMEZONE` | Fuseau horaire qui définit le décalage horaire par rapport à UTC | `UTC` |
| `RETENTION_DAYS` | Durée de conservation de l'historique des modifications des tables (Time Travel) (0-90) | `1` |
| `FULL_BACKUP_POLICY_DAYS` | Durée de conservation des sauvegardes complètes de la base de données | `180` |
| `RAW_TABLE_BACKUP_POLICY_DAYS` | Durée de conservation des sauvegardes de la table RAW | `730` |
| `FINAL_SCHEMA_BACKUP_POLICY_DAYS` | Durée de conservation des sauvegardes du schéma FINAL | `90` |

<br>

⚠️ Considérations importantes concernant RETENTION_DAYS:
Non applicable sur les **Tables temporaires** (supprimées en fin de session).
**Fail-safe** est une période de protection qui commence après l'expiration du Time Travel.
Elle n'est pas affectée par ce paramètre.

**Comportement des erreurs et plafonds**
*   ⚠️ **Plafonnement automatique (tables transitoires)** : Toute valeur de `RETENTION_DAYS` > 1 est traitée comme **1 jour**.
*   ❌ **Erreur de dépassement de limite** : Toute valeur de `RETENTION_DAYS` dépassant la **limite autorisée** pour le type de compte et de table génère une erreur.

**Compte Standard**
*   **Tables transitoires et permanentes** : `RETENTION_DAYS` = **0 ou 1 jour**.
*   **Fail-safe** : **7 jours** fixe après Time Travel.

**Comptes Enterprise, Business Critical et Virtual Private Snowflake**
*   **Tables transitoires** : `RETENTION_DAYS` = **0 ou 1 jour**.
*   **Tables permanentes** : `RETENTION_DAYS` = **0 à 90 jours**.
*   **Fail-safe** : **7 jours** après Time Travel. Peut être **étendu jusqu'à 90 jours** via un contrat spécifique avec Snowflake.
<br>


## 🔧 Dépannage Rapide
- Échec connexion Snowflake : Vérifier les secrets GitHub
- Timeout scraping : Vérifier l'accès aux URLs sources
- Erreur dbt : Consulter les logs détaillés du job
- Passer la valeur de la variable `LOGGER_LEVEL` à `DEBUG` pour voir les logs détaillés