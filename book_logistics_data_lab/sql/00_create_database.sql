-- ============================================================
-- Book lab: Arquitectura Moderna de Datos e IA
-- Script: 00_create_database.sql
-- Dialect: PostgreSQL
-- Purpose: create the database used by the logistics case study.
--
-- Execute from a maintenance database, for example:
--   psql -U postgres -d postgres -f sql/00_create_database.sql
-- ============================================================

-- CREATE DATABASE cannot run inside a transaction block.
-- If the database already exists, this block will skip creation.
SELECT 'CREATE DATABASE logistics_ai_lab'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'logistics_ai_lab'
)\gexec

-- Optional: after this script, connect to the new database and run:
--   psql -U postgres -d logistics_ai_lab -f sql/01_create_schema_tables_indexes.sql
