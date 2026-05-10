# Arquitectura Moderna de Datos e IA — Logistics Synthetic Data Lab

Este kit genera un modelo operacional sintético para el caso transversal del libro:
**Proyecto de logística inteligente**.

Incluye:

- SQL PostgreSQL para crear base de datos, tablas, constraints, índices y vistas iniciales.
- Generador Python de datos sintéticos.
- Exportador a CSV y Parquet.
- Cargador Python a PostgreSQL usando `COPY`.

## 1. Estructura

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
├─ requirements.txt
└─ README.md
```

## 2. Modelo incluido

Tablas principales:

- `customers`
- `partners`
- `warehouses`
- `carriers`
- `routes`
- `orders`
- `order_lines`
- `shipments`
- `tracking_events`
- `incidents`
- `sensor_readings`
- `documents`
- `emission_records`
- `decision_log`

Vistas iniciales:

- `v_shipments_enriched`
- `v_delivery_kpis_daily`

## 3. Crear la base de datos PostgreSQL

```bash
psql -U postgres -d postgres -f sql/00_create_database.sql
psql -U postgres -d logistics_ai_lab -f sql/01_create_schema_tables_indexes.sql
```

## 4. Preparar entorno Python

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows PowerShell
pip install -r requirements.txt
```

## 5. Generar ficheros CSV

```bash
python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 5000
```

Generará:

```text
data/output/csv/customers.csv
data/output/csv/orders.csv
data/output/csv/shipments.csv
...
```

## 6. Generar CSV y Parquet

```bash
python scripts/01_generate_files.py --output-dir data/output --format both --n-orders 5000
```

Nota: Parquet requiere `pyarrow` o `fastparquet`.

## 7. Cargar CSV en PostgreSQL

Configura variables de entorno:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=logistics_ai_lab
export PGUSER=postgres
export PGPASSWORD=postgres
```

En Windows PowerShell:

```powershell
$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGDATABASE="logistics_ai_lab"
$env:PGUSER="postgres"
$env:PGPASSWORD="postgres"
```

Carga los datos:

```bash
python scripts/02_load_postgres_from_csv.py --input-dir data/output/csv --truncate
```

## 8. Generar y cargar en un solo paso

```bash
python scripts/03_generate_and_load_postgres.py --output-dir data/output --n-orders 5000 --truncate
```

## 9. Validar carga

```bash
psql -U postgres -d logistics_ai_lab -f sql/02_smoke_test_counts.sql
```

## 10. Escala recomendada para pruebas

Pequeña:

```bash
python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 1000
```

Media:

```bash
python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 10000
```

Mayor volumen:

```bash
python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 100000
```

Para 100k órdenes conviene revisar memoria local y tamaño de ficheros, especialmente `tracking_events` y `documents`.

## 11. Uso en el libro

Este modelo está pensado para evolucionar después hacia:

- raw / bronze / silver / gold
- modelo dimensional Kimball
- Data Vault
- datasets para predicción
- datasets documentales para RAG
- trazabilidad de agentes IA
- data products para GAIA-X / data spaces
