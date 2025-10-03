# 🚕 NYC Taxi Data Pipeline

Pipeline d'ingestion automatique des données Yellow Taxi de New York vers Snowflake.
<br> <br>

## 📋 Prérequis

- Compte **Snowflake**
- Dépôt **GitHub**
<br>


## 📊 Flux de traitement
- **Table principale** : `yellow_taxi_trips_raw` - créée dynamiquement avec schéma inféré automatiquement + colonne filename
- **Table métadonnées** : `file_loading_metadata` - suit le statut de chaque fichier traité (succès/échec)
- **Gestion des doublons** : vérification via métadonnées avant traitement
<br>


## 🚀 Méthode 1 : Exécution Automatique (GitHub Actions)
Le pipeline s'exécute automatiquement **tous les 10 du mois à 2h**.

### ⚙️ Configuration
1. **Forkez** ce dépôt
2. **Ajoutez les secrets :** `Settings` > `Secrets and variables` > `Actions` > `New repository secret`

| Secret | Description |
| :--- | :--- |
| `SNOWFLAKE_USER` | Utilisateur Snowflake |
| `SNOWFLAKE_PASSWORD` | Mot de passe Snowflake |
| `SNOWFLAKE_ACCOUNT` | Compte Snowflake |
| `WH_NAME` | Warehouse |
| `DW_NAME` | Database |
| `RAW_SCHEMA_NAME` | Schéma |

3. **Exécution automatique du workflow**
<br>


## 🚀 Méthode 2 : Exécution Locale
**Cloner et se positionner**
```bash
git clone https://github.com/EliasMez/nyc-taxi-pipeline.git
cd nyc-taxi-pipeline
```

**Environnement virtuel à la racine**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate  # Windows
```

**Fichier `.env` à la racine avec les variables ci-dessous**
```bash
SNOWFLAKE_USER=votre_utilisateur_snowflake
SNOWFLAKE_PASSWORD=votre_mot_de_passe_snowflake
SNOWFLAKE_ACCOUNT=votre_compte_snowflake
WH_NAME=NYC_WH
DW_NAME=NYC_TAXI_DW
RAW_SCHEMA_NAME=RAW
```

**Installer les dépendances et exécuter**
```bash
cd snowflake_ingestion
pip install -r requirements.txt
python snowflake_pipeline.py
```
<br>


## 🚨 Amélioration possible
**Problème identifié**
- Avec autocommit=True, risque d'incohérence si l'UPDATE échoue après le COPY INTO.
**Solution en possible**
- Migration vers transactions manuelles avec rollback si erreur pour garantir l'atomicité des opérations.
