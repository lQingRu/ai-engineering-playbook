# Backend and database

Apply to APIs, jobs, integrations, schemas, and stored data.

## Owned policy

- Preserve supported caller and data contracts. Plan a compatible transition when a contract changes.
- Protect data invariants across failures, retries, and concurrent work where applicable.
- Plan rollout, validation, and recovery for migrations. Account for existing data and staggered deployment where relevant.

## External guidance

Use version-matched framework, database, and migration-tool documentation. For published HTTP contracts, use the project's chosen [OpenAPI version](https://spec.openapis.org/). For PostgreSQL work, consult the [deployed version's documentation](https://www.postgresql.org/docs/) and `supabase-postgres-best-practices` where applicable.

## Project decisions and verification

Establish compatibility expectations, migration ownership, and recovery requirements. Verify affected contracts and invariants, and exercise migrations against representative existing data.
