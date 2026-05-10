# Arquitectura Snowflake-centric

```text
Raw / staging desde ficheros o integraciones
    ↓
Transformaciones SQL
    ↓
Marts dimensionales
    ↓
delivery_kpis
    ↓
emissions_kpi
    ↓
shipment_delay_features
    ↓
Consumo BI / modelos predictivos / agentes
```
