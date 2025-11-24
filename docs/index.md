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