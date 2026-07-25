# Hands-On 8 — RESTful API Design Best Practices

Refactored the FastAPI implementation (chosen framework) to meet REST conventions.

## What changed vs Hands-On 7
- **Versioning**: all routes moved to `/api/v1/...` (see `main.py` comment for the
  URL-vs-header versioning trade-off)
- **PATCH added** alongside PUT: PUT = full replace (all fields required),
  PATCH = partial update (only supplied fields)
- **Pagination envelope**: `GET /api/v1/courses/?page=1&page_size=2` returns
  `{count, next, previous, results}` (DRF-style)
- **Filtering**: `?search=` performs a case-insensitive match on name/code
- **Location header**: every `POST` sets `Location: /api/v1/courses/{id}/`
- **Standardised errors** (`errors.py`): all 4xx/422 responses become
  `{"error": {"code", "message", "field"}}`

## How to run
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```
Try: `GET /api/v1/courses/?page=1&page_size=2`, then `?search=data`, then hit a
missing ID to see the standardised error envelope.
