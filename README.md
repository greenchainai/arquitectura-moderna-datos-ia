
# Arquitectura Moderna de Datos e IA

Repositorio complementario del libro **“Arquitectura Moderna de Datos e IA: Patrones, plataformas y decisiones inteligentes de extremo a extremo”**.

📘 Disponible en Amazon: [https://amzn.eu/d/0igDzMPz](https://amzn.eu/d/0igDzMPz)

Este repositorio contiene ejemplos técnicos, estructuras de carpetas, scripts y artefactos de apoyo utilizados para ilustrar los conceptos arquitectónicos del libro. El objetivo no es proporcionar una solución productiva cerrada, sino ofrecer una base práctica y didáctica para entender cómo se puede diseñar una arquitectura moderna de datos e IA de extremo a extremo.


# arquitectura-moderna-datos-ia
Ejemplos técnicos del libro “Arquitectura Moderna de Datos e IA”: datos, IA, dbt, GitOps, agentes, gobierno y arquitectura end-to-end.


## Objetivo del repositorio

El material incluido sirve como apoyo para explorar conceptos como:

- ingesta y transformación de datos;
- arquitectura raw, bronze, silver y gold;
- modelado analítico y patrones como Kimball, Inmon, Data Vault y Medallion;
- calidad, testing y observabilidad del dato;
- gobierno, contratos de datos y trazabilidad;
- Git, DataOps, CI/CD e infraestructura como código;
- preparación de datos para IA;
- RAG, embeddings, prompts y agentes IA;
- predicción y decision intelligence;
- espacios de datos y GAIA-X.

## Caso transversal

Los ejemplos se basan en un caso de **logística inteligente**, donde se trabaja con entidades como:

- clientes;
- pedidos;
- envíos;
- eventos de tracking;
- incidencias;
- rutas;
- transportistas;
- almacenes;
- documentos;
- emisiones de CO₂;
- decisiones y recomendaciones.

Este caso permite mostrar cómo un mismo dominio de datos puede evolucionar desde una estructura operacional inicial hasta modelos analíticos, datasets predictivos, activos para IA y posibles data products.

## Estructura del repositorio

```text
arquitectura-moderna-datos-ia/
├── 00_data_lab/
├── 01_end_to_end_architecture/
├── 02_ingestion_transformation/
├── 03_modeling_patterns/
├── 04_quality_serving/
├── 05_governance_incentives/
├── 06_ai_preparation/
├── 07_ai_agents/
├── 08_decision_intelligence/
├── 09_enterprise_architecture_gitops/
├── 10_data_spaces_gaiax/
├── docs/
├── README.md
└── SCRIPT_INDEX.md
````

## Contenido incluido

El repositorio incluye ejemplos en distintos formatos:

* scripts SQL;
* scripts Python;
* modelos y ejemplos dbt;
* configuraciones YAML;
* contratos y políticas en JSON;
* prompts versionados;
* definiciones de herramientas para agentes;
* ejemplos de reglas de calidad;
* ejemplos de reglas de decisión;
* estructuras Git/DataOps;
* documentación técnica de apoyo.

## Cómo utilizar este repositorio

Puedes utilizar este repositorio de tres formas:

1. **Como material de consulta**, revisando los ejemplos asociados a cada capítulo.
2. **Como laboratorio de aprendizaje**, adaptando los scripts y estructuras a tu propio entorno.
3. **Como punto de partida**, tomando ideas para diseñar tus propias arquitecturas de datos e IA.

Los ejemplos están pensados para facilitar la comprensión de los patrones explicados en el libro. Antes de llevar cualquier elemento a producción, deben revisarse y adaptarse a los requisitos reales de seguridad, rendimiento, gobierno, escalabilidad y cumplimiento de cada organización.

# Arquitectura Moderna de Datos e IA

Repositorio complementario del libro **Arquitectura Moderna de Datos e IA**.

📘 Disponible en Amazon: https://amzn.eu/d/0igDzMPz

## Requisitos orientativos

Algunos ejemplos pueden requerir herramientas como:

* Python 3.x;
* PostgreSQL u otra base relacional;
* dbt;
* entorno cloud o lakehouse;
* Git;
* herramientas de CI/CD;
* librerías Python para generación o procesamiento de datos.

Los requisitos concretos pueden variar según el ejemplo.

## Aviso importante

Este repositorio tiene un propósito **educativo y arquitectónico**.
Los ejemplos no representan una implementación productiva completa ni sustituyen el diseño específico que requiere cada organización.

Cada empresa debe adaptar los patrones a su contexto, volumen de datos, plataforma tecnológica, requisitos de seguridad, gobierno, privacidad, normativa y objetivos de negocio.

## Licencia

El código y los ejemplos técnicos de este repositorio se publican bajo licencia MIT.

El contenido editorial completo del libro, textos, diagramas, imágenes, portada, estructura narrativa y material publicado en la obra permanecen protegidos por copyright del autor.

## Autor

Repositorio creado por **Jorge Hernández**, Arquitecto de Soluciones especializado en arquitectura de datos, transformación digital, plataformas cloud e inteligencia artificial aplicada al negocio.


