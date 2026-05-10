# 00 — Data Lab

Kit inicial para generar datos sintéticos del caso de logística inteligente y simular ingesta mediante CSV/Parquet.

## Ejecución rápida

```bash
createdb logistics_ai_lab
psql -d logistics_ai_lab -f sql/01_create_operational_schema.sql
python scripts/generate_synthetic_data.py --output-dir data/generated --n-orders 5000
python scripts/export_ingestion_files.py --input-dir data/generated --output-dir data/ingestion --format both
```
