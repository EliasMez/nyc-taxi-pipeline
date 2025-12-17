# NYC Taxi Data Pipeline

Este flujo de trabajo de GitHub Actions automatiza la canalización de datos de extremo a extremo, desde la inicialización de la infraestructura de Snowflake hasta la producción de tablas y vistas analíticas utilizando Python y dbt.

<br>
<a href="https://github.com/EliasMez/nyc-taxi-pipeline/">💻 Código fuente del proyecto</a>
<br>
<a href="https://eliasmez.github.io/nyc-taxi-pipeline/dbt">📚 Documentación **dbt** en línea</a>
<br>

## 📊 Fuente de Datos

[**Datos de Registro de Viajes de la TLC**](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - Comisión de Taxis y Limusinas de Nueva York

Los datos incluyen:

- Fechas/horas de recogida y entrega
- Ubicaciones GPS de los viajes
- Distancias, tarifas detalladas, tipos de pago
- Número de pasajeros reportado por el conductor

*Los datos son recopilados por proveedores de tecnología autorizados y proporcionados a la TLC. La TLC no garantiza la precisión de estos datos.*

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Los datos de origen son proporcionados por la [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) y sujetos a sus términos de uso.