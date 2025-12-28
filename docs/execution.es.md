# 💻 Inicio del Proyecto

## 📋 Requisitos Previos

- Cuenta de **Snowflake** con privilegios **SECURITYADMIN** y **SYSADMIN**
- Repositorio de **GitHub** con **secretos configurados** (ver sección de configuración)
- Acceso a las fuentes de datos de NYC Taxi: **https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**
<br>

## 🚀 Ejecución
- Automática: Cada día 1 del mes a las 10:00
- Manual: A través de la interfaz de GitHub Actions
<br>

## ⚙️ Configuración
1. **Haz un fork** de este repositorio: https://github.com/EliasMez/nyc-taxi-pipeline
<br>

2. **Añade los secretos OBLIGATORIOS:** `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secreto | Descripción |
|--------|-------------|
| `SNOWFLAKE_USER` | Nombre de usuario de Snowflake |
| `SNOWFLAKE_PASSWORD` | Contraseña del usuario de Snowflake |
| `SNOWFLAKE_ACCOUNT` | Identificador de la cuenta de Snowflake |
| `PASSWORD_DEV` | Contraseña del usuario de desarrollo |
| `PASSWORD_BI` | Contraseña de usuario Analista BI |
| `PASSWORD_DS` | Contraseña de usuario Científico de Datos |
| `PASSWORD_MC` | Contraseña de usuario Consumidor de Marts |
| `GH_RELEASE_TOKEN` | Token de GitHub para el versionado automático (necesario solo si usa el workflow Release) |
<br>

⚠️ **Workflow de Lanzamiento (Semantic Release)**
El workflow **Release** requiere un token de GitHub (`GH_RELEASE_TOKEN`) para funcionar.
Si este token no está definido, **el workflow fallará sistemáticamente** durante el paso de publicación.

**Opción 1**: Desactivar el workflow *Release*
Si no necesita el versionado automático de código: `Actions` → `Release` → **Disable workflow**

**Opción 2**: Crear un Personal Access Token (recomendado si mantiene el workflow)
1. Ve a: `Settings` → `Developer settings` → `Personal access tokens` → **Tokens (classic)**
2. Crea un token con permisos `repo`
3. Añádelo como secreto: `Settings` → `Secrets and variables` → `Actions` → **New repository secret**
   - Nombre: `GH_RELEASE_TOKEN`
   - Valor: *su token*
<br>

3. **Personaliza las variables OPCIONALES:** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `WH_NAME` | Nombre del almacén de datos | `NYC_WH` |
| `DW_NAME` | Nombre de la base de datos | `NYC_TAXI_DW` |
| `RAW_SCHEMA` | Esquema de datos crudos | `RAW` |
| `STAGING_SCHEMA` | Esquema de datos limpiados | `STAGING` |
| `FINAL_SCHEMA` | Esquema de datos finales | `FINAL` |
| `PARQUET_FORMAT` | Formato de archivo Parquet | `PARQUET_FORMAT` |
| `COMPUTE_SIZE` | Potencia de cálculo del almacén de datos | `X-SMALL` |
| `ROLE_TRANSFORMER` | Rol para las transformaciones | `TRANSFORMER` |
| `ROLE_BI_ANALYST` | Nombre del rol Analista BI | `ROLE_BI_ANALYST` |
| `ROLE_DATA_SCIENTIST` | Nombre del rol Científico de Datos | `ROLE_DATA_SCIENTIST` |
| `ROLE_MART_CONSUMER` | Nombre del rol Consumidor de Marts | `ROLE_MART_CONSUMER` |
| `USER_DEV` | Usuario de desarrollo | `USER_DEV` |
| `USER_BI_ANALYST` | Nombre de usuario Analista BI | `USER_BI_ANALYST` |
| `USER_DATA_SCIENTIST` | Nombre de usuario Científico de Datos | `USER_DATA_SCIENTIST` |
| `USER_MART_CONSUMER` | Nombre de usuario Consumidor de Marts | `USER_MART_CONSUMER` |
| `METADATA_TABLE` | Tabla de metadatos | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | Tabla de datos crudos | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | Tabla de staging | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | Nivel de registro | `INFO` |
| `SCRAPING_YEAR` | Fecha de inicio del scraping (>2000 y <año actual)| año actual |
| `TIMEZONE` | Zona horaria que define el desplazamiento respecto a UTC | `UTC` |
<br>

## 🔧 Solución Rápida de Problemas
- Fallo de conexión con Snowflake: Verificar los secretos de GitHub
- Timeout del scraping: Verificar el acceso a las URLs fuente
- Error de dbt: Consultar los registros detallados del job
- Cambie el valor de la variable `LOGGER_LEVEL` a `DEBUG` para ver registros detallados