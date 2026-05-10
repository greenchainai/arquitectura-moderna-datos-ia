# Patrones híbridos

## Patrón 1

```text
Bronze / Raw → Data Vault o Integration Layer → Silver / Curated → Kimball Marts → Semantic Layer / BI / IA / Predicción
```

## Patrón 2

```text
Bronze → Silver normalizado estilo enterprise → Gold dimensional → Features predictivas / Data products
```

## Patrón 3

```text
Raw → Data Vault para historificación → Kimball para BI → Tablas feature-ready para ML → Data products para compartir
```
