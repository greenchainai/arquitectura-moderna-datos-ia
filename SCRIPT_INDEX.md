# Índice de scripts y artefactos técnicos

Este fichero sirve como guía rápida para localizar los ejemplos técnicos del repositorio complementario del libro **“Arquitectura Moderna de Datos e IA: Patrones, plataformas y decisiones inteligentes de extremo a extremo”**.

Los ejemplos están organizados por capítulos y tienen un propósito didáctico. No representan una solución productiva cerrada, sino una base para entender patrones de arquitectura, diseño de datos, IA, gobierno, GitOps y decision intelligence.

---

## 00_data_lab

Material base para generar y cargar datos sintéticos del caso de logística inteligente.

| Artefacto | Descripción |
|---|---|
| `sql/00_create_database.sql` | Script inicial para crear la base de datos del laboratorio. |
| `sql/01_create_schema_tables_indexes.sql` | Creación de tablas principales, constraints e índices del modelo logístico. |
| `sql/02_smoke_test_counts.sql` | Consultas básicas para validar que la carga de datos funciona. |
| `scripts/common_synthetic_generator.py` | Generador común de datos sintéticos. |
| `scripts/01_generate_files.py` | Genera ficheros CSV o Parquet para simular ingesta. |
| `scripts/02_load_postgres_from_csv.py` | Carga ficheros CSV en PostgreSQL. |
| `scripts/03_generate_and_load_postgres.py` | Genera datos sintéticos y los carga directamente en PostgreSQL. |

---

## 01_end_to_end_architecture

Artefactos relacionados con la arquitectura lógica de referencia.

| Artefacto | Descripción |
|---|---|
| `README.md` | Explicación del flujo end-to-end del dato. |
| `architecture_flow.md` | Descripción del recorrido: fuentes, ingesta, transformación, gobierno, IA, decisión y feedback. |

---

## 02_ingestion_transformation

Ejemplos de ingesta, transformación inicial y estructura Git/DataOps.

| Artefacto | Descripción |
|---|---|
| `python/api_ingestion_example.py` | Ejemplo de ingesta desde una API. |
| `sql/raw_tables.sql` | Definición conceptual de tablas raw. |
| `sql/staging_tables.sql` | Definición conceptual de tablas staging. |
| `sql/raw_to_staging_transform.sql` | Transformación desde raw hacia staging. |
| `dbt/stg_tracking_events.sql` | Modelo dbt de staging para eventos de tracking. |
| `dbt/schema.yml` | Tests y documentación dbt para modelos staging. |
| `git_repository_structure.md` | Estructura sugerida de repositorio Git para DataOps. |

---

## 03_modeling_patterns

Ejemplos de modelado Kimball, Inmon, Data Vault y Medallion.

| Artefacto | Descripción |
|---|---|
| `sql/kimball_star_schema.sql` | Ejemplo de modelo dimensional para logística. |
| `sql/fact_shipments.sql` | Tabla de hechos para análisis de envíos. |
| `sql/dimensions.sql` | Dimensiones principales: cliente, transportista, ruta, fecha y almacén. |
| `sql/data_vault_hubs.sql` | Ejemplos de hubs para Data Vault. |
| `sql/data_vault_links.sql` | Ejemplos de links para Data Vault. |
| `sql/data_vault_satellites.sql` | Ejemplos de satellites para Data Vault. |
| `docs/hybrid_patterns.md` | Explicación de patrones híbridos aplicados al caso logístico. |

---

## 04_quality_serving

Ejemplos de calidad, observabilidad, serving layer y semantic layer.

| Artefacto | Descripción |
|---|---|
| `sql/quality_checks.sql` | Consultas SQL para validar nulos, duplicados, relaciones y fechas. |
| `dbt/schema_quality_tests.yml` | Tests dbt para calidad de datos. |
| `sql/shipments_enriched.sql` | Vista o tabla de serving con envíos enriquecidos. |
| `sql/delivery_kpis_daily.sql` | Cálculo de KPIs diarios de entrega. |
| `semantic_models/delivery_kpis.yml` | Ejemplo conceptual de definición semántica de métricas. |
| `docs/quality_matrix.md` | Matriz de calidad por capa: raw, staging, silver, gold e IA. |

---

## 05_governance_incentives

Artefactos de gobierno, contratos de datos, ownership y políticas.

| Artefacto | Descripción |
|---|---|
| `json/orders.contract.json` | Ejemplo de contrato de datos para pedidos. |
| `json/shipments.contract.json` | Ejemplo de contrato de datos para envíos. |
| `json/access_policy.json` | Ejemplo de política de acceso. |
| `sql/governance_metadata_tables.sql` | Tablas conceptuales para catálogo, ownership, contratos y reglas. |
| `docs/raci_matrix.md` | Matriz de responsabilidades para gobierno del dato. |
| `docs/incentives_and_game_theory.md` | Notas sobre incentivos, cooperación y teoría de juegos aplicada al dato. |

---

## 06_ai_preparation

Ejemplos para preparación de conocimiento, RAG, embeddings y versionado de prompts.

| Artefacto | Descripción |
|---|---|
| `python/embedding_pipeline_example.py` | Pseudoflujo para generación de embeddings. |
| `json/document_metadata_example.json` | Ejemplo de metadatos enriquecidos para documentos. |
| `yaml/chunking_config.yml` | Configuración conceptual de chunking. |
| `yaml/embedding_config.yml` | Configuración conceptual de embeddings. |
| `prompts/logistics_assistant/system_prompt_v1.md` | Prompt inicial para asistente logístico. |
| `prompts/logistics_assistant/system_prompt_v2.md` | Versión mejorada del prompt con restricciones empresariales. |
| `prompts/logistics_assistant/evaluation_cases.yml` | Casos de evaluación para el asistente. |
| `docs/rag_architecture.md` | Explicación del patrón RAG aplicado al caso logístico. |

---

## 07_ai_agents

Ejemplos de agentes IA, tool calling, guardrails, trazabilidad y evaluación.

| Artefacto | Descripción |
|---|---|
| `python/logistics_agent_pseudocode.py` | Pseudocódigo de agente logístico con tool calling. |
| `json/tools.json` | Definición conceptual de herramientas disponibles para el agente. |
| `json/guardrails.json` | Política de guardrails para controlar comportamiento del agente. |
| `json/tool_invocation_log.json` | Ejemplo de registro trazable de herramienta invocada. |
| `yaml/evaluation_cases.yml` | Casos de evaluación para validar comportamiento del agente. |
| `agents/logistics_operations_agent/agent_config.yml` | Configuración conceptual del agente de operaciones logísticas. |
| `agents/logistics_operations_agent/system_prompt.md` | Prompt del agente. |
| `agents/logistics_operations_agent/README.md` | Descripción del agente y sus responsabilidades. |
| `docs/agent_governance.md` | Recomendaciones de gobierno para agentes empresariales. |

---

## 08_decision_intelligence

Ejemplos de predicción, reglas de decisión, decision log y feedback.

| Artefacto | Descripción |
|---|---|
| `python/delay_prediction_example.py` | Ejemplo simple de predicción de retraso. |
| `python/recommend_action.py` | Regla de decisión para recomendar acciones operativas. |
| `sql/decision_model_tables.sql` | Tablas conceptuales para predicción, recomendaciones, decisiones y feedback. |
| `sql/decision_log.sql` | Ejemplo de estructura para registrar decisiones. |
| `yaml/decision_rules.yml` | Reglas de decisión expresadas en YAML. |
| `docs/closed_loop_analytics.md` | Explicación del ciclo cerrado: dato, decisión, acción y feedback. |

---

## 09_enterprise_architecture_gitops

Ejemplos de arquitectura enterprise, GitOps, CI/CD e infraestructura como código.

| Artefacto | Descripción |
|---|---|
| `docs/platform_mapping.md` | Mapeo entre problema, patrón y herramienta. |
| `docs/fabric_centric_architecture.md` | Flujo conceptual Fabric-centric. |
| `docs/snowflake_architecture.md` | Flujo conceptual Snowflake-centric. |
| `docs/databricks_architecture.md` | Flujo conceptual Databricks/lakehouse. |
| `docs/gitops_and_iac.md` | Explicación de GitOps e infraestructura como código. |
| `yaml/ci_cd_pipeline.yml` | Ejemplo conceptual de pipeline CI/CD. |
| `infra/terraform/example_main.tf` | Ejemplo conceptual de Terraform. |
| `docs/repository_structure.md` | Estructura de carpetas recomendada para Git. |

---

## 10_data_spaces_gaiax

Ejemplos conceptuales sobre data products, contratos, políticas y espacios de datos.

| Artefacto | Descripción |
|---|---|
| `json/shipment_co2_data_product.json` | Ejemplo de data product para emisiones CO₂ de envíos. |
| `json/usage_contract.json` | Contrato conceptual de uso de datos. |
| `json/partner_access_policy.json` | Política de acceso para partners. |
| `json/edc_policy_example.json` | Ejemplo conceptual de política estilo EDC. |
| `docs/api_vs_dataspace.md` | Comparativa entre API tradicional y data space. |
| `docs/gaiax_dataspace_overview.md` | Resumen conceptual de GAIA-X y espacios de datos. |

---

## docs

Documentación transversal del repositorio.

| Artefacto | Descripción |
|---|---|
| `docs/architecture_overview.md` | Visión general de la arquitectura del caso logístico. |
| `docs/data_model_overview.md` | Descripción del modelo de datos transversal. |
| `docs/security_overview.md` | Seguridad como capa transversal de la arquitectura. |
| `docs/how_to_use_this_repo.md` | Recomendaciones para usar los ejemplos del repositorio. |

---

## Recomendaciones de uso

1. Empieza por `00_data_lab` si quieres trabajar con datos sintéticos.
2. Revisa `02_ingestion_transformation` para entender el flujo raw/staging.
3. Consulta `03_modeling_patterns` para comparar Kimball, Data Vault y Medallion.
4. Usa `04_quality_serving` para entender calidad, KPIs y serving.
5. Explora `06_ai_preparation` y `07_ai_agents` para IA, RAG y agentes.
6. Revisa `08_decision_intelligence` para conectar predicción, recomendación y decisión.
7. Consulta `09_enterprise_architecture_gitops` para GitOps, CI/CD e infraestructura.
8. Finaliza con `10_data_spaces_gaiax` para data products y espacios de datos.

---

## Nota importante

Los ejemplos son didácticos y deben adaptarse antes de usarse en entornos productivos.  
Cada organización debe ajustar seguridad, rendimiento, gobierno, permisos, escalabilidad, cumplimiento normativo y arquitectura cloud según su contexto real.
```
