# CHANGELOG

<!-- version list -->

## v3.1.0 (2026-01-17)

### Bug Fixes

- **dbt**: Correction materialized: seed
  ([`b830826`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/b830826bd6094a619193fa0dca42b6ae98fdcb7e))

- **dbt**: Modif type de table
  ([`1f88733`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1f88733083c0a5bf6ebe781ac352e4be0be0ae86))

- **snowflake**: Final backup policy correction
  ([`074ab4f`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/074ab4ff8c8066b98cb16cd48eeb24646973c3c1))

- **sql**: Correction lintage sqlfluff et ajout .benchmarks au .gitignore
  ([`d4f0d85`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d4f0d85175282bdb2acc851345583c58502434a7))

- **sql**: Modification schema backup
  ([`61d9299`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/61d9299e878dbbf81c86dfab3b9d9b82394dac02))

- **workflow**: Correction sqlfluff affiche erreur lintage
  ([`9fa2c95`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/9fa2c95d6575f65f6cd8120357d8de9a99ba1d5f))

- **workflow**: Correction users variables name
  ([`2e4c92b`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2e4c92bedac32a9d1baf917c8937911968dfe433))

### Documentation

- **mkdocs**: Mise a jour de la doc ajout test docstrings et ajout variables
  ([`f18f892`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f18f89285d41f4cc97bb4b3d47abac6741b5c0b9))

### Features

- **snowflake**: Ajout du backup
  ([`adc8a7d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/adc8a7dff9953fbc8ddf59e264e8d4193b751bb9))

### Testing

- **snowflake**: Ajout des tests backup et correction import unused security
  ([`d78bac2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d78bac252fb4674036a1016bae90be05785a02f3))


## v3.0.0 (2026-01-12)

### Bug Fixes

- **dbt**: Corriger les types de table pour STG et FINAL
  ([`f94f872`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f94f872980b63ad44183f65d94c3196cdc286d1c))

- **snowflake**: Tables RAW PERMANENT to TRANSIENT et traduction des logs en anglais
  ([`f3270c7`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f3270c75c570e08aba58d165397a47f41d33df8d))

- **sql**: Correction lintage
  ([`f189b09`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f189b0932faa49ccca17cd20a01a407fb6da014c))

### Documentation

- **mkdocs**: Ajout retention et types de tables dans mkdocs
  ([`61c15de`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/61c15de617a673f0703b22723faa34950e5c21e4))

### Features

- **snowflake**: Mise en place de la retention
  ([`b4fc639`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/b4fc6390332120531f6bca17e74148f87bf9086d))

### Testing

- **snowflake**: Correction tests et traduction en anglais des docstrings et logs
  ([`6c12103`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/6c1210358efb7a8331a47ce6076e738275b90659))

### Breaking Changes

- **dbt**: Certaines tables des schémas 'STAGING' et 'FINAL' ont changé de type
  (TRANSIENT/PERMANENT). Vérifiez votre configuration.


## v2.2.0 (2026-01-01)

### Bug Fixes

- **snowflake**: Evolution de run_sql pour prendre en compte schema_
  ([`a41cef8`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/a41cef866e374e6c67cf7899edfcd6a4d790b443))

- **tests**: Correction pyhon tests et sqlfluff lintage
  ([`9ef3ee9`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/9ef3ee97421427c9cd97c6b05c3f2a9aaa0fe874))

### Chores

- **workflow**: Ajout des roles metiers dans les variables d'environnements et secrets du workflow
  ([`9c1cb88`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/9c1cb88685475d8a410080f2eed42b963951b9bf))

### Documentation

- **mkdocs**: Adaptation de mkdocs a l'ajout des roles et users metier
  ([`9af6c52`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/9af6c52eaaed4b5eeca5dce6af48ecdc5e79c126))

### Features

- **snowflake**: Ajout des roles metier dans le sql
  ([`f3c5c01`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f3c5c01c896ca625731febc3d3905c4790563e37))

- **workflow**: Variabilisation de COMPUTE_SIZE du warehouse
  ([`7a7cbe7`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/7a7cbe70172d2d19bbad1cf8608b4be1e93cca25))

### Refactoring

- **dbt**: Ingestion taxi_zone dans source
  ([`a62be65`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/a62be654ce96ab107aa3d0217dc2dc0c8ed0aeb1))

- **env**: Supresion SCHEMA_ devant RAW
  ([`bfb7c4d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/bfb7c4dbc2629b3dfaa7aa982d06b63f1260c4fd))

### Testing

- **dbt**: Ajout description et tests dim_date et dim_time
  ([`0daff0f`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/0daff0ff84c562a02087aba42b32c0672143f5bf))


## v2.1.2 (2025-12-21)

### Bug Fixes

- **workflow**: Ajout du declenchement de codeql sur push main en plus de on pr main pour declencher
  la maj du scan sur la branche par defaut
  ([`6f1a083`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/6f1a083d0d9eeb025d1d4b2718cfee8dd3edb94f))

### Chores

- **deps**: Bump filelock from 3.20.0 to 3.20.1
  ([`1537b88`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1537b88173bebdf534e2f640114712e45de47e33))

- **deps**: Bump urllib3 from 2.5.0 to 2.6.0
  ([`c8e615e`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/c8e615ee07bd30b977d7e5e6fba717b293b24148))


## v2.1.1 (2025-12-20)

### Bug Fixes

- **workflow**: Fetch tag release
  ([`ee7f680`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ee7f68092612e8f6260feb2af635716335afc981))

### Chores

- **snowflake**: Suppression import inutils
  ([`1a167af`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1a167af4e1361cbbd0234a0af71fe3cdcd5ab0dd))

### Documentation

- **dbt**: Traduction overview en anglais
  ([`6b04090`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/6b0409032a118b48cd4308dd9f0b6b5c064e6ab4))

- **README**: Reduction readme
  ([`811ac3d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/811ac3de599603888245756f0499a5227b122436))


## v2.1.0 (2025-12-20)

### Bug Fixes

- **docs**: Ajout du typing dans les fonctions python
  ([`4589a5f`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4589a5fabcd7392fa76b78c6eb4dd1d4c4c851e5))

- **workflow**: Correction deployment workflow sequentiel
  ([`6bd4c70`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/6bd4c708f43d2af41109403e2ff82288c7109f3b))

### Documentation

- **mkdocs**: Traduction bar de nav horizontal
  ([`8533ca7`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8533ca7576a252ed00394ca5e57cef664d76c589))

### Features

- **analytics**: Connexion a google analytics
  ([`17573fd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/17573fdf03fc3f7530e0c311557630747b3b6b91))

- **docs**: Ajout bouton luminosité mkdocs
  ([`a4c4b35`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/a4c4b35903b6b6fa6144febf52395c96a8ddeea1))

- **docs**: Ajout de dbt link dans la liste deroulante
  ([`74a2075`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/74a2075e6900ff0e2c739c3a705d9571d5afce6b))

- **docs**: Ajout des .md multilangues et metadata
  ([`5e3f9ce`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/5e3f9ce94dc64bec9f194a48ebe20394c34e5429))

- **docs**: Ajout des cookies
  ([`e894656`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/e894656501dfe9c8419c5eda2aa2390ae55b78b8))

- **docs**: Ajout reseaux et description docs
  ([`47d45ed`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/47d45edbeab5d559a9843f5e10dd1e893bf232a9))


## v2.0.0 (2025-12-14)

### Bug Fixes

- **dbt**: Correction dim time trasnfo
  ([`abcea47`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/abcea474efafdce680f9b4633a84b43ba53ee254))

- **dbt**: Lintage sql
  ([`b5a4697`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/b5a4697b00215899040016b93b6e796816e1bb96))

- **dtb**: Correction jour semaine
  ([`c971a4d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/c971a4db6e23c0aa83769a8b2acda173d5385cf3))

- **release**: Correction token
  ([`2416681`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2416681f11bfbc085fc92de11b04cf9689c7a7f9))

- **snowflake**: Correction pipeline load and tests
  ([`dcb25e5`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/dcb25e5d509f1c0e48ee1fb9ba8217251f530119))

- **workflow**: Correction token retour ancien token
  ([`9fe4193`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/9fe41935bfd0c728e33df7003f049ff2e1b222ec))

### Chores

- **pytest**: Correction import
  ([`8f38348`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8f383485d59daf38fe6e282ac0fa7a15d386caec))

- **pytest**: Correction import
  ([`99ecef3`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/99ecef3eae967e4fc23ade261708528ea7e0a073))

- **snowflake**: Ajout id table raw et sequence
  ([`c5c5b10`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/c5c5b103a196e4144cab4a03c421ac58969e5245))

- **workflow**: Modif token par defaut release
  ([`2b6bf89`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2b6bf89fc3770d4fe004dcfd16dcc624c8b2b191))

- **workflow**: Update version 3.10 release
  ([`d9ccfdf`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d9ccfdfa88d6685134fa386bdb4d9dd692c0e6e7))

### Continuous Integration

- **codeQL**: Ajout package security-extended
  ([`904237e`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/904237ecb86105ccee1d72840358ff3d533e1040))

- **codeQL**: Correction security import * et autres
  ([`ca3dd99`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ca3dd99446dbaa736f2da6415c21c9e1dadaa7e0))

### Documentation

- Ajout des docstrings et doctest
  ([`7496b77`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/7496b77655b67d6af03c3025d3997a221daedff7))

- **dbt**: Ajout description yml
  ([`f934827`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f934827317df56636af18ef03fb2620f8157f430))

- **dbt**: Personnalisation de dbt docs overview
  ([`1bb23d2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1bb23d25d84d0cb1145795528348fa88611a87d9))

- **mkdocs**: Ajout des docstrings dans mkdocs
  ([`3b723de`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/3b723dea53d346321316b815a3bdc52e0c1c0c90))

- **mkdocs**: Mise à jour mkdocs
  ([`d4e88f6`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d4e88f6e885cde2e4c5c275ab2737547ed88ab45))

- **mkdocs**: Mise à jour mkdocs
  ([`d2422d2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d2422d2f7dfc609006236880c9082fddfb394465))

- **README**: Adaptations
  ([`8000787`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8000787c5b55f87744a86b89aac352970304c1d9))

- **README**: Adaptations
  ([`5d27a30`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/5d27a30eb6ddcb137eb652380fc65373074afa24))

- **README**: Update README.md
  ([`fd6baff`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/fd6baffcd1fa3bb8a1d2a512aca9829592ae4912))

### Features

- Ajouter modèles dimensions et marts d'analyse
  ([`7249e26`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/7249e2611414deb268f6b55063f9e460520b0e0f))

- **pytests**: Ajout des tests pytest et modifs noms de fichiers
  ([`472c5b5`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/472c5b5ec8b6457a00ba0233bc8d6b696c0c4305))

- **workflow**: Ajout de l'automatisation du deploiement mkdocs
  ([`ad77dde`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ad77dde2c79f78efbe611d2e574cf845bddd6c76))

- **workflow**: Automatisation deployment dbt docs
  ([`3cfaf7d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/3cfaf7d733ca4b81855aecd896b72ba3f943953d))

- **workflow**: Automatisation fix lintage dbt sql
  ([`2700a70`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2700a70426351fe8811a3b364b561d0b3baeed7b))

- **workflow**: Variabilisation du timezone
  ([`932d614`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/932d6144c21f24a41aaad9377528da2597515108))

### Refactoring

- **stage**: Modif temp_file
  ([`8ab1ab7`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8ab1ab71e1c399286be847a97e1752db785a8172))

- **workflow**: Séparation de la logique de test du code du workflow principal
  ([`214cd7d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/214cd7df6d322b9af0951acbe2d02aba4f563645))

### Testing

- **pytest**: Ajout des tests complets
  ([`4fd68c9`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4fd68c9510cf6de6d1796903ec19b1d1b128e74e))


## v1.6.0 (2025-11-11)

### Chores

- **sql**: Modif lint correction sql
  ([`d2c2f59`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d2c2f5917579949b726474bdb89f551acf8c13d9))

### Features

- **workflow**: Ajout de sqlfluff
  ([`61615cf`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/61615cf3d121b1f62394f8c190bba6531c425400))


## v1.5.0 (2025-11-09)

### Bug Fixes

- **workflow**: Ajout pull request main release
  ([`920430e`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/920430ee1d94a768a588fa90701ec2f3166c4189))

### Chores

- **deps**: Agate version 1.9.1 compatible dbt_adaptater et dbt_common
  ([`16f303a`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/16f303a46e05e3f17ab08c9bc24d038c76d09a09))

- **deps**: Bump actions/checkout from 4 to 5
  ([`e68695f`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/e68695f5bada9b0c0820018048cf132a444feba2))

- **deps**: Bump actions/setup-python from 4 to 6
  ([`d51d388`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d51d388d4499b718862fb64122653663594b2382))

- **deps**: Bump agate from 1.9.1 to 1.13.0
  ([`f865815`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f865815432f8ea93604c2160aada20a5c4227aa3))

- **deps**: Bump attrs from 25.3.0 to 25.4.0
  ([`e9b76b0`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/e9b76b02453d6384d262f9e16bbbdc3baafe9976))

- **deps**: Bump boto3 from 1.40.45 to 1.40.68
  ([`1bf7d5b`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1bf7d5b10ac8dd49f24fe31300662bd52728a5ce))

- **deps**: Bump botocore from 1.40.45 to 1.40.68
  ([`2883b37`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2883b376bd06622cd3b29a9f21ae5bf136eb2caf))

- **deps**: Bump certifi from 2025.1.31 to 2025.10.5
  ([`4aafd09`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4aafd09d71a66759f559ed9bdd52765f5b1e2266))

- **deps**: Bump cffi from 1.17.1 to 2.0.0
  ([`f996eca`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f996eca997439d2cdf964209d9d6b138b79a607b))

- **deps**: Bump charset-normalizer from 3.4.3 to 3.4.4
  ([`fba1070`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/fba1070260934f47060c938ef9f25b9b747ff701))

- **deps**: Bump click from 8.1.8 to 8.3.0
  ([`ee6d727`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ee6d727acfc336e72148c23d28199ff98b14008c))

- **deps**: Bump cryptography from 46.0.0 to 46.0.3
  ([`3882ad9`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/3882ad9981ea75904b32cd4be1e8658af4e9c0d5))

- **deps**: Bump dbt-adapters from 1.17.2 to 1.18.0
  ([`954a384`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/954a38488da2cd629e5a0d0c4ce4b136d9ee08a5))

- **deps**: Bump dbt-common from 1.32.0 to 1.36.0
  ([`72639d9`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/72639d9fd0912084d467591a50cb7b226aaa9796))

- **deps**: Bump dbt-protos from 1.0.375 to 1.0.382
  ([`94057b2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/94057b213dba673d354c3dc6db5a0bd45ebee7ce))

- **deps**: Bump dbt-semantic-interfaces from 0.9.0 to 0.10.0
  ([`2a3d2a1`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2a3d2a1736f13d55a28760feae19478504cab6ed))

- **deps**: Bump dbt-snowflake from 1.10.2 to 1.10.3
  ([`6cfbedf`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/6cfbedfef2c70543a0369c8176f1f8d97767cac5))

- **deps**: Bump deprecated from 1.2.18 to 1.3.1
  ([`8265fb2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8265fb2b0db476d37bd744f2a56023ec47109687))

- **deps**: Bump filelock from 3.19.1 to 3.20.0
  ([`ec74aa0`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ec74aa0c302f3753370c95b446d82b50c86dcb11))

- **deps**: Bump idna from 3.10 to 3.11
  ([`4a9ce4b`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4a9ce4b8513079f41e07c4005374ce267a760dd2))

- **deps**: Bump isodate from 0.6.1 to 0.7.2
  ([`508d811`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/508d811faec2ab640f79e9661c1edc6b1202104a))

- **deps**: Bump markdown-it-py from 3.0.0 to 4.0.0
  ([`61dffbd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/61dffbd2ca51c0efe16ab4ccf0bc2b84c2aa9ec9))

- **deps**: Bump mashumaro from 3.14 to 3.17
  ([`3e2ae52`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/3e2ae5223fc4cf4d92f80c32fb3ee563514c2158))

- **deps**: Bump msgpack from 1.1.1 to 1.1.2
  ([`1fc5aa3`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1fc5aa36ff5e95e11fa285d1f9156a6716031174))

- **deps**: Bump networkx from 3.2.1 to 3.5
  ([`5c1d1a4`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/5c1d1a4d34faab4d6f8c885016e7636ec3510add))

- **deps**: Bump platformdirs from 4.4.0 to 4.5.0
  ([`0672e29`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/0672e29ff1c3cf8c730892377262d0cdbe557a7e))

- **deps**: Bump protobuf from 6.32.1 to 6.33.0
  ([`20c5346`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/20c5346f2cece8ed41cf8ede03d4b75929a6fe05))

- **deps**: Bump pydantic from 2.11.10 to 2.12.4
  ([`13823c5`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/13823c5be976a26ae43378747d19098e9cf1e351))

- **deps**: Bump pydantic-core from 2.33.2 to 2.41.5
  ([`2fc0ac8`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2fc0ac8d97d8122ace9ad2c52012b608c0a20049))

- **deps**: Bump python-dotenv from 1.1.1 to 1.2.1
  ([`feb4db9`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/feb4db91ba77ff49a4b426e52fe070dea686aa61))

- **deps**: Bump python-gitlab from 6.5.0 to 7.0.0
  ([`5dfee91`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/5dfee9100746d916cdd7c274cf56b3346199a2ec))

- **deps**: Bump referencing from 0.36.2 to 0.37.0
  ([`d3df6f1`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/d3df6f1e354316dbc6ceebb8dabcfed0c39a2bb5))

- **deps**: Bump rpds-py from 0.27.1 to 0.28.0
  ([`f5d71ae`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f5d71aefc6cf50730ad074a6c20f58f948438875))

- **deps**: Bump secretstorage from 3.3.3 to 3.4.0
  ([`ee419aa`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ee419aada61c4b1325ad5d04baa367011186d565))

- **deps**: Bump snowflake-connector-python from 3.17.4 to 4.0.0
  ([`b2f72ab`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/b2f72ab3927e844c7ebf953fd9054409e8de1b98))

- **deps**: Bump urllib3 from 1.26.20 to 2.5.0
  ([`87f66ef`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/87f66efa38e879dacb6430413eccb66b1235f888))

- **deps**: Bump wrapt from 1.17.3 to 2.0.1
  ([`74e7abd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/74e7abdac4307f157795cc63905bce2bd19e4be5))

- **deps**: Cffi 1.14.0
  ([`8d118fd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8d118fdc38fadf1501a28566414571682c4d9885))

- **deps**: Cffi 1.17.1
  ([`4fb75b6`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4fb75b6c0c6b862dd9e0c5f6ca6818bbb2e88030))

- **deps**: Cffi 1.9.0
  ([`1b79aa8`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1b79aa8fe5caefe7f47c837db2e2eb9bf78f0b4c))

- **deps**: Click 8.1.0
  ([`c10c406`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/c10c406ff71e53bd3c99ed3baea61fdb99e788fa))

- **deps**: Cryptography 46.0.0
  ([`2079586`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/2079586e66efedbe68c8d485904885ac2119aa8a))

- **deps**: Dbt-semantic-interfaces
  ([`1134361`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/1134361de317adc2852cf12d163ddcabb4fc9324))

- **deps**: Isodate version 0.6.1
  ([`b785709`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/b785709b1f48fa42202c29b84681958c5878e24b))

- **deps**: Mashumaro rollback version 3.14 conflict with dbt_adaptater
  ([`e06a118`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/e06a11855ad79456067f576805dc91e99e7306da))

- **deps**: Networkx 3.4.2
  ([`a9e51c7`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/a9e51c7fe07c671983a08602c1ee9894fa490a41))

- **deps**: Python version 3.10
  ([`4da43c2`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4da43c2c283868ed00fcda88ad7705ea4d9027cb))

- **deps**: Python-gitlab==6.5.0
  ([`86c0b70`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/86c0b702f45122f8b82cb22e2a62ea1338e103a9))

- **deps**: Retour 2025.1.31 certifi
  ([`063519b`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/063519be0d61b414769ecf87ffcf4fdcdd441641))

- **deps**: Snowflake-connector-python==3.17.4
  ([`23b603d`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/23b603d2e1d78803cf8872f6fb9d4f0ad93e4c0c))

- **workflow**: Changement de version python 3.11
  ([`726ad3e`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/726ad3e019eff0203ad45c2d94280b488a4b16ea))

### Documentation

- **mkdocs**: Ajout de mkdocs
  ([`ab985fe`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/ab985fe7596e7baf93f5b9b9e323391521f8b739))

### Features

- **workflow**: CodeQL ajout
  ([`dc0bba0`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/dc0bba0bf40b5f37e49403728b9b674d82f8fe7b))


## v1.4.0 (2025-11-07)

### Bug Fixes

- **workflows**: Correction interval dependabot
  ([`36781dd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/36781ddaed87b83461342c0134766c836725e412))

### Chores

- **workflow**: Release token name change
  ([`7cb5769`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/7cb576905a8b7aabcbdf6fb2b9e6e52dad749c40))

### Features

- **scraper**: Ajout de variable année scraping
  ([`8e212a8`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/8e212a8047c9c3d227bf8d9633b782f9d2682dc3))


## v1.3.1 (2025-11-07)

### Bug Fixes

- **workflows**: Correction interval dependabot
  ([`36781dd`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/36781ddaed87b83461342c0134766c836725e412))


## v1.3.0 (2025-11-07)

### Bug Fixes

- **workflow**: Remove workflow conditions and add failed stage/load reprocessing
  ([`310f2dc`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/310f2dcc0d9395f9865ab6c8b91d67bc71cb57dd))

### Features

- **dbt**: Set incremental materialization for fact_trips and staging tables
  ([`f4fcb8c`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/f4fcb8cd535edd7e6e723a04d1163ffd8ad0537b))

- **workflow**: Dependabot
  ([`7038073`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/703807379325c6596e0edfc79c3b4958e37dbc3b))


## v1.2.0 (2025-11-03)

### Bug Fixes

- **workflow**: Installation des dependances avant run
  ([`4b8ae4e`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/4b8ae4e15a68511a92b3e39a0c553c1627a0a090))

### Documentation

- **readme**: Mise à jour
  ([`3be01bc`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/3be01bc6d6a646a54de18dac79405fc0c097903f))

### Features

- **dbt**: Ajout des tests dbt
  ([`84e3a49`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/84e3a499fc79c3e17a666e168d91250118ecfeee))


## v1.1.0 (2025-10-30)

### Features

- **workflow**: Ajout de variables githubAction optionnelles pour l'utilisateur
  ([`869c8ef`](https://github.com/EliasMez/nyc-taxi-pipeline/commit/869c8efbca19ca94eec0ef71dca276f4384aeaed))


## v1.0.0 (2025-10-30)


## v0.1.0 (2025-10-30)

- Initial Release
