# 📈 Gobernanza de Datos

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 Monitoreo
- Registros detallados en GitHub Actions.
- Alertas por correo electrónico en caso de falla o cancelación del flujo de trabajo.
- Seguimiento del estado a través de una tabla de metadatos que indica cada etapa (*raspado / almacenado provisionalmente / éxito / fallido*).

## ✅ Calidad de Datos
- Pruebas de **dbt** que garantizan la integridad, coherencia y validez de los datos.
- Gestión de duplicados mediante verificación sistemática de metadatos.

## 🧪 Calidad del Código
- Pruebas unitarias con **Pytest**.
- Validación SQL con **SQLFluff**.
- Cadenas de documentación y pruebas de documentación para la documentación de funciones.
- <a href="https://eliasmez.github.io/nyc-taxi-pipeline/docstrings/">📚 Documentación técnica</a>

## 🔐 Seguridad
- Secretos cifrados en los registros.
- Uso de **GitHub Secrets**.
- Permisos mínimos aplicados en Snowflake.
- Análisis estático con **CodeQL**.
- Actualizaciones de seguridad automatizadas a través de **Dependabot**.