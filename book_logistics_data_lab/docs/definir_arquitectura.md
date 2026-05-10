He preparado el kit inicial para el **proyecto de logística inteligente** del libro.

Lo he montado en formato laboratorio técnico, con:

* SQL para **PostgreSQL**
* creación de base de datos, esquema, tablas, constraints, índices y vistas iniciales
* script Python para generar datos sintéticos
* script Python para exportar a **CSV y Parquet**
* script Python para cargar CSV en PostgreSQL
* dataset de ejemplo pequeño en CSV para validar la estructura
* README con instrucciones de ejecución

Puedes descargarlo aquí:

[Descargar kit de datos sintéticos logística](sandbox:/mnt/data/book_logistics_data_lab.zip)

## Contenido principal

```text
book_logistics_data_lab/
├─ sql/
│  ├─ 00_create_database.sql
│  ├─ 01_create_schema_tables_indexes.sql
│  └─ 02_smoke_test_counts.sql
├─ scripts/
│  ├─ common_synthetic_generator.py
│  ├─ 01_generate_files.py
│  ├─ 02_load_postgres_from_csv.py
│  └─ 03_generate_and_load_postgres.py
├─ data_sample/
│  └─ csv/
├─ requirements.txt
└─ README.md
```

## Tablas incluidas

El modelo cubre las entidades núcleo que definimos para el libro:

* `customers`
* `partners`
* `warehouses`
* `carriers`
* `routes`
* `orders`
* `order_lines`
* `shipments`
* `tracking_events`
* `incidents`
* `sensor_readings`
* `documents`
* `emission_records`
* `decision_log`

También incluí dos vistas iniciales útiles:

* `v_shipments_enriched`
* `v_delivery_kpis_daily`

## Ejecución rápida

Crear base de datos:

```bash
psql -U postgres -d postgres -f sql/00_create_database.sql
psql -U postgres -d logistics_ai_lab -f sql/01_create_schema_tables_indexes.sql
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Generar CSV:

```bash
python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 5000
```

Generar CSV y Parquet:

```bash
python scripts/01_generate_files.py --output-dir data/output --format both --n-orders 5000
```

Cargar en PostgreSQL:

```bash
python scripts/02_load_postgres_from_csv.py --input-dir data/output/csv --truncate
```

Validar carga:

```bash
psql -U postgres -d logistics_ai_lab -f sql/02_smoke_test_counts.sql
```

## Nota importante

He usado **PostgreSQL** como base inicial porque encaja muy bien para el laboratorio del libro y después podremos evolucionarlo hacia:

* raw / bronze / silver / gold
* dbt
* modelo dimensional
* Data Vault
* Snowflake
* Databricks
* Fabric
* datasets para IA
* predicción
* agentes
* GAIA-X / data products compartibles

