## Architecture Technique

- **Orchestration** : GitHub Actions
- **Data Warehouse** : Snowflake
- **Transformation** : dbt
- **Langage** : Python


## Structure du Projet

```bash
nyc-taxi-pipeline/
├── .github/workflows/nyc_taxi_pipeline.yml
│
├── snowflake_ingestion/
│   ├── sql
│   │   ├── 01_init/
│   │   ├── 02_scraping/
│   │   ├── 03_stage/
│   │   └── 04_load/
│   │
│   ├── 01_init_data_warehouse.py
│   ├── 02_scrape_links.py
│   ├── 03_upload_stage.py
│   └── 04_load_to_table.py
│
└── dbt_transformations/
    └── NYC_Taxi_dbt/
        └── models/
            ├── staging/
            ├── final/
            └── marts/
```