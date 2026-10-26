def dedupe(candidates):
    seen = set()
    out = []
    for c in candidates:
        if c["post_id"] in seen:
            continue
        seen.add(c["post_id"])
        out.append(c)
    return out


def test_dedupe_keeps_first_occurrence():
    cands = [
        {"post_id": 1, "text": "followed"},
        {"post_id": 2, "text": "global"},
        {"post_id": 1, "text": "global-dupe"},
    ]
    out = dedupe(cands)
    assert [c["post_id"] for c in out] == [1, 2]
    assert out[0]["text"] == "followed"  # first-seen wins


def test_dedupe_preserves_order():
    cands = [{"post_id": i} for i in [3, 1, 2, 1, 3]]
    out = dedupe(cands)
    assert [c["post_id"] for c in out] == [3, 1, 2]
