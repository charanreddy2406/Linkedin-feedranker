#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://localhost:8000}"
USER_ID="${USER_ID:-1}"

echo "1) feed before engagement:"
curl -s "$BASE/feed?user_id=$USER_ID&limit=5" | python3 -m json.tool

echo "2) posting engagement on post 104 (was lower-ranked, older):"
for i in 1 2 3; do
  curl -s -X POST "$BASE/events/engagement" \
    -H 'content-type: application/json' \
    -d '{"user_id":1,"post_id":104,"event_type":"like"}' > /dev/null
done

echo "   waiting for the consumer to materialize aggregates..."
sleep 3

echo "3) feed after engagement (post 104 should rank higher):"
curl -s "$BASE/feed?user_id=$USER_ID&limit=5" | python3 -m json.tool
