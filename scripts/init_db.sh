#!/usr/bin/env bash
set -euo pipefail

DB_URL="${DATABASE_URL:-postgresql://feed:feed@localhost:5432/feed}"

echo "applying migrations..."
for f in db/migrations/*.sql; do
    echo "  -> $f"
    psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$f"
done

echo "seeding..."
psql "$DB_URL" -v ON_ERROR_STOP=1 -f db/seed/seed.sql

echo "done."
