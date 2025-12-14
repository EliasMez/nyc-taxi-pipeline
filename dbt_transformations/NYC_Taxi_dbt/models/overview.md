{% docs __overview__ %}
# NYC Taxi Data Pipeline - Documentation dbt

Bienvenue dans la documentation dbt du projet **NYC Taxi Data Pipeline**.
Ce projet a pour objectif de transformer les données brutes de la TLC (Taxi & Limousine Commission de New York) en tables analytiques prêtes pour l’analyse et le reporting.
- 📚 [Documentation globale du projet](https://eliasmez.github.io/nyc-taxi-pipeline/)
- 💻 [Code source du projet](https://github.com/EliasMez/nyc-taxi-pipeline/)



## Rôle de dbt

Le workflow dbt transforme les données de la **couche raw** vers la **couche staging** qui contient :
- Le seed `taxi_zone_lookup` importé
- La table `stg_taxi_trips` des données brutes nettoyées
- La table intermédiaire `int_trip_metrics` de métriques calculées

puis vers la **couche finale** qui contient :
- **Dimensions**
- **Faits**  
- **Marts analytiques**

Chaque modèle dbt est documenté ici, avec son emplacement dans le pipeline, sa description, et son lien avec les autres modèles.



## Navigation dans la documentation

- **Project Tab** : explorez la structure de votre projet dbt et accédez à la documentation de chaque modèle  
- **Database Tab** : visualisez les relations entre tables/faits/dimensions comme dans un explorateur de base de données  
- **Graph Exploration** : consultez le graphe de dépendances pour suivre le lineage des modèles en cliquant sur l’icône située **en bas à droite de l’écran**

Pour plus d’informations sur dbt et son fonctionnement, consultez [la documentation officielle de dbt](https://docs.getdbt.com/).

---

{% enddocs %}





{% docs __source_raw__ %}

## Source de données – Raw

Les données sources proviennent du **TLC Trip Record Data** (New York City Taxi & Limousine Commission).

Elles contiennent notamment :
- Dates et heures de prise en charge et de dépose  
- Localisations GPS des trajets  
- Distances parcourues  
- Tarifs détaillés et types de paiement  
- Nombre de passagers

Les données sont collectées par des fournisseurs technologiques autorisés et fournies à la TLC.  
La TLC ne garantit pas l’exactitude des données.

{% enddocs %}



{% docs __dbt_utils__ %}

## dbt_utils

Le package **dbt_utils** est utilisé dans ce projet **pour ses macros de test avancées**, notamment `accepted_range` qui vérifie que les valeurs d'une colonne sont dans une plage attendue.

{% enddocs %}



{% docs __dbt_expectations__ %}

## dbt_expectations

Le package **dbt_expectations** est utilisé pour implémenter des tests de qualité de données avancés.

Il permet notamment de :
- Vérifier la complétude des données
- Contrôler les valeurs attendues
- Détecter les anomalies statistiques
- Renforcer la fiabilité des modèles analytiques

Ces tests assurent la qualité des dimensions, faits et marts produits.

{% enddocs %}



{% docs __dbt_date__ %}

## dbt_date

Le package **dbt_date** fournit des macros pour la manipulation des dates et des périodes temporelles.

Les dimensions date et time sont construites manuellement à partir des timestamps des données sources afin de refléter uniquement les valeurs réellement observées.

Le package dbt_date est installé mais non utilisé ici — la logique est implémentée en SQL pur car elle répond aux besoins des marts temporels (daily, weekly, monthly, hourly, yearly) sans nécessiter de calendrier complet artificiel.

{% enddocs %}





