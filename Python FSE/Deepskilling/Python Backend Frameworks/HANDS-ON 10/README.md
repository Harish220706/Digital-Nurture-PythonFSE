# Hands-On 10 — Microservices Architecture: Concepts & Decomposition

## Service decomposition

| Service | Responsibility | Endpoints it owns | Database it owns |
|---|---|---|---|
| Course Service (5001) | Department & Course CRUD | `/api/courses/*` | its own courses store |
| Student Service (5002) | Student CRUD, enrollment | `/api/students/*` | its own students store |
| Auth Service (concept) | Registration, login, token validation | `/api/auth/*` | users store |
| Notification Service (concept) | Email confirmations | internal / async | none (stateless) |

This exercise implements **Course Service** and **Student Service** as two
independent Flask apps (each with its own in-memory/SQLite data — no shared
database), plus a minimal **API Gateway** that proxies requests to the
correct service.

## How to run (3 terminals)
```bash
pip install -r requirements.txt

# terminal 1
cd course_service && python app.py     # http://localhost:5001

# terminal 2
cd student_service && python app.py    # http://localhost:5002

# terminal 3
cd gateway && python app.py            # http://localhost:5000
```

Test the full flow through the gateway:
```bash
curl -X POST http://localhost:5000/api/students/1/enroll \
     -H "Content-Type: application/json" \
     -d '{"course_id": 1}'
```
The gateway routes to Student Service, which calls Course Service to verify
the course exists. Stop Course Service and repeat the call — Student Service
catches the `ConnectionError` and Student Service/gateway return `503`.

## Sync vs async inter-service communication
Synchronous HTTP calls (as used here) are simple but create **tight
coupling** — if Course Service is down, enrollment fails outright. A
message queue (RabbitMQ, Kafka) **decouples** services: Student Service
could publish an "enrollment requested" event and continue immediately,
with Course Service (or a saga/orchestrator) processing it later. The
trade-off is **eventual consistency** — the enrollment isn't confirmed
immediately, so the system needs a way to handle/report failures
asynchronously. Use a queue when services can tolerate a delay and you
want resilience to a downstream service being temporarily unavailable;
use direct HTTP when the caller genuinely needs an immediate answer.
