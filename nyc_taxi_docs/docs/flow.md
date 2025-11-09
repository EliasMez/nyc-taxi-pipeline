## Flux de traitement
 
1. **Initialisation de l'environnement Snowflake** : <br>
Création de la base de données, du schéma, du data warehouse, de l'utilisateur, création et attribution des permissions via le rôle.

2. **Scraping** : <br>
Extraction des données sources via un script Python.

3. **Stockage temporaire** : <br>
Ingestion des données brutes dans un buffer ou un stage Snowflake avant traitement.

4. **Chargement des données** : <br>
Chargement des données brutes dans la table du du schéma RAW.

5. **Installation des dépendances dbt** : <br>
Installation et mise à jour des packages dbt nécessaires.

6. **Transformation avec dbt** : <br>
Nettoyage et préparation des données dans la table du schéma STAGING, puis modélisation dans les tables du schéma FINAL (dimensions, faits et vues agrégées).

7. **Tests dbt** : <br>
Exécution des tests de qualité des données et de cohérence des modèles.