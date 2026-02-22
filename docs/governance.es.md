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

## 👥 Gestión de Accesos y Roles

El acceso al almacén se basa en el **principio de mínimo privilegio**: cada rol dispone únicamente de los derechos estrictamente necesarios para su función.

### Roles del sistema Snowflake

Predefinidos por la plataforma, utilizados únicamente durante la inicialización de la infraestructura:

| Rol | Uso |
|-----|-----|
| `SYSADMIN` | Crea el warehouse, la base de datos y los esquemas; otorga privilegios |
| `SECURITYADMIN` | Crea roles de negocio y cuentas de usuario |
| `ACCOUNTADMIN` | Configura el Time Travel |

### Roles de negocio

| Rol | Usuario | Acceso | Caso de uso |
|-----|---------|--------|-------------|
| **TRANSFORMER** | USER_DEV | Todos los esquemas | Pipeline ETL dbt e ingesta Python |
| **BI_ANALYST** | USER_BI_ANALYST | Lectura SCHEMA_FINAL (tablas + vistas) | Informes BI |
| **DATA_SCIENTIST** | USER_DATA_SCIENTIST | Lectura SCHEMA_STAGING + SCHEMA_FINAL (tablas) | Análisis exploratorio |
| **MART_CONSUMER** | USER_MART_CONSUMER | Lectura vistas SCHEMA_FINAL únicamente | Consumo de agregados analíticos |

## 📋 Indicadores de Servicio (SLA)

### SLA Snowflake (proveedor)

Dos umbrales de disponibilidad mensual se aplican simultáneamente:

| Umbral | Condición | Penalidades |
|--------|-----------|-------------|
| **99,9%** | Interrupción > 43 min o > 1% de errores | 10% (< 99,9%) → 25% (< 99,0%) → 50% (< 95,0%) |
| **99,99%** | Interrupciones cortas (4–43 min, > 10% errores) acumuladas > 43 min | Violación del umbral 99,9% |

### SLA del proyecto

| Indicador | Objetivo |
|-----------|---------|
| Duración del pipeline mensual | < 30 min |
| Tasa de éxito de carga | 100% |
| Tasa de éxito de pruebas dbt | 100% |
| Frescura de los datos | < 30 días |
| Resolución de incidentes P1 | < 48 h |

## 💾 Copias de Seguridad

El **Time Travel de Snowflake** (1 día en cuenta Standard) permite recuperar cambios recientes pero no constituye un backup: no se crea ninguna copia independiente. Las políticas siguientes aseguran una retención a largo plazo en copias separadas.

| Objeto | Frecuencia | Retención |
|--------|-----------|-----------|
| Base completa `NYC_TAXI_DW` | Mensual | 180 días |
| Tabla `YELLOW_TAXI_TRIPS_RAW` | Mensual | **730 días** (por defecto) |
| Esquema `FINAL` | Mensual | 90 días |

- **730 días** para la tabla RAW: datos fuente potencialmente irremplazables si el sitio NYC TLC no conserva el historial.
- **90 días** para el esquema FINAL: reconstruible desde RAW vía dbt.
- Duraciones configurables mediante variables `RAW_TABLE_BACKUP_POLICY_DAYS`, `FULL_BACKUP_POLICY_DAYS`, `FINAL_SCHEMA_BACKUP_POLICY_DAYS`.