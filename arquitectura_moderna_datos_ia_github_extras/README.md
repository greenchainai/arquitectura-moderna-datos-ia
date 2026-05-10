# Arquitectura Moderna de Datos e IA — Extras técnicos

Repositorio complementario del libro **Arquitectura Moderna de Datos e IA: Patrones, plataformas y decisiones inteligentes de extremo a extremo**.

Este repositorio no pretende ser un producto listo para producción. Su objetivo es acompañar el libro con ejemplos de arquitectura, SQL, Python, YAML, JSON, prompts y estructuras de proyecto que ayuden a comprender cómo se diseñan soluciones modernas de datos e IA.

## Caso transversal

El dominio usado es una plataforma de **logística inteligente** con entidades como Customer, Order, OrderLine, Shipment, TrackingEvent, Warehouse, Carrier, Incident, Route, SensorReading, Document, EmissionRecord, Partner y DecisionLog.

## Estructura

```text
00_data_lab/
01_end_to_end_architecture/
02_ingestion_transformation/
03_modeling_patterns/
04_quality_serving/
05_governance_incentives/
06_ai_preparation/
07_ai_agents/
08_decision_intelligence/
09_enterprise_architecture_gitops/
10_data_spaces_gaiax/
docs/
```

## Cómo usarlo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r 00_data_lab/requirements.txt
```

Los scripts son didácticos. Antes de usarlos en producción se deben revisar seguridad, secretos, permisos, validación, rendimiento, gobierno, auditoría y cumplimiento.
