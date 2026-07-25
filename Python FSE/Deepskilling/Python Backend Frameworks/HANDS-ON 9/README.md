# Hands-On 9 — Authentication & Security: JWT, OAuth2 & OWASP

## What's inside
- `security.py` — bcrypt password hashing (`get_password_hash`/`verify_password`)
  and JWT create/decode helpers (30-min expiry)
- `models.py` — `User` model (email, hashed_password, is_active)
- `auth_routes.py` — `POST /api/v1/auth/register/` (409 on duplicate email),
  `POST /api/v1/auth/login/` (returns a JWT), plus a note on OAuth2 Authorization
  Code flow vs. this simple JWT login
- `deps.py` — `get_current_user` dependency that validates the JWT (401 if invalid/expired)
- `main.py` — CORS configured for `http://localhost:3000`; `POST`/`DELETE`/`PATCH`
  on `/api/v1/courses/` now require a valid Bearer token; `GET` stays public

## How to run
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```
1. `POST /api/v1/auth/register/` with `{"email": "...", "password": "..."}`
2. `POST /api/v1/auth/login/` → copy `access_token`
3. In Postman, set `Authorization: Bearer <token>` and try `POST /api/v1/courses/`
   — without the header you should get `401 Unauthorized`
