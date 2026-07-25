# QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### Test cases by test level (Course Management API)

**Unit Testing** — test a single function in isolation
- Test: `validate_course_code(code)` returns `False` when the course code is empty or exceeds 10 characters, without touching the database or the API layer at all.

**Integration Testing** — test two components working together
- Test: `POST /api/courses/` correctly writes a new row to the `courses` table and the returned response body matches the row that was actually inserted into the database.

**System Testing** — full end-to-end flow
- Test: A client sends `POST /api/courses/` with valid JSON, the request passes through auth middleware → validation → business logic → database → response serialization, and the client receives a `201` with the complete course object, including a server-generated `id` and `created_at` timestamp.

**User Acceptance Testing (UAT)** — from the perspective of an actual college admin
- Test: A college admin logs into the admin portal, fills out the "Add New Course" form with a real course name and code, clicks Save, and confirms the course now appears in the course listing exactly as they expect it to — with no knowledge of the API underneath.

### Functional vs. Non-Functional classification
- Unit test above → **Functional** (does the validation function do what it should?)
- Integration test above → **Functional**
- System test above → **Functional**
- UAT test above → **Functional**
- **Non-Functional example**: Load test — `POST /api/courses/` must respond in under 300ms at the 95th percentile when 100 concurrent admins are creating courses simultaneously. This tests *how well* the system performs, not *whether* it works.

### Black-Box vs. White-Box Testing
- **Black-Box Testing**: The tester interacts only with inputs and outputs — they send a request to `POST /api/courses/` and check the response, with no visibility into how the endpoint is implemented internally.
- **White-Box Testing**: The tester has access to the source code and designs tests around internal logic paths — e.g., writing a unit test that specifically exercises the `if course_code in existing_codes:` branch inside the validation function.
- In practice: **QA testers typically perform Black-Box testing** (they validate behavior against requirements without needing to read the implementation). **Developers typically perform White-Box testing** (unit tests, code coverage, exercising internal branches) since they wrote the code and understand its structure.

### 3 Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-COURSE-001 | Create a course with valid data | User is authenticated as admin | 1. Send `POST /api/courses/` with valid `name`, `code`, `credits` 2. Read response | Response is `201 Created` with the new course object including a generated `id` | | |
| TC-COURSE-002 | Reject duplicate course code | A course with code `CS101` already exists | 1. Send `POST /api/courses/` with `code: "CS101"` again | Response is `400 Bad Request` with an error message stating the code already exists | | |
| TC-COURSE-003 | Reject request missing required field | User is authenticated as admin | 1. Send `POST /api/courses/` with `name` omitted | Response is `422 Unprocessable Entity` listing `name` as a required field | | |

## Task 2: Defect Lifecycle & Severity Classification

### Defect Lifecycle
```
New → Assigned → Open → Fixed → Retest → Verified → Closed
                   |
                   ├─→ Rejected   (defect is not reproducible, or is "working as designed")
                   └─→ Deferred   (valid defect, but fix postponed to a later release)
```
- **New**: Defect is logged by QA, not yet triaged.
- **Assigned**: A developer or team is assigned ownership.
- **Open**: Developer has acknowledged and is actively working on it.
- **Fixed**: Developer has committed a fix and marked it ready for retest.
- **Retest**: QA re-runs the original failing steps against the fix.
- **Verified**: QA confirms the fix resolves the issue with no regression.
- **Closed**: Defect is fully resolved and the ticket is archived.
- **Rejected**: QA/dev determines the reported behavior is not actually a defect (duplicate, by design, or not reproducible) — the ticket is closed without a code change.
- **Deferred**: The defect is valid but the team decides to postpone the fix to a future release (often due to low priority or release deadline pressure).

### Severity / Priority classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) `POST /api/courses/` returns 500 for all requests | **Critical** | **P1** | Core functionality is completely broken for every user — no course can be created at all. |
| (b) Course names >150 chars are silently truncated | **Medium** | **P3** | Data is silently corrupted (a real defect), but it doesn't crash the system or block usage — most course names are well under 150 characters. |
| (c) Typo in Swagger `/docs` description | **Low** | **P4** | Purely cosmetic, no functional impact whatsoever. |
| (d) Login intermittently returns 401 with correct credentials | **High** | **P1** | Individual occurrences may seem low-impact, but intermittent auth failures indicate deep instability and directly block users from logging in — hard to reproduce makes it urgent to fix before it worsens. |

### Defect Report — Bug (a)

| Field | Value |
|---|---|
| Defect ID | DEF-2026-0142 |
| Title | `POST /api/courses/` returns 500 Internal Server Error for all requests |
| Environment | Staging, Ubuntu 22.04, Python 3.11, PostgreSQL 15 |
| Build Version | v2.3.1-rc2 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Authenticate as admin. 2. Send `POST /api/courses/` with a valid JSON body (`name`, `code`, `credits`). 3. Observe the response. |
| Expected Result | `201 Created` with the newly created course object in the response body. |
| Actual Result | `500 Internal Server Error` with no course created, for every request regardless of payload. |
| Attachments | screenshot of 500 error |

### Severity vs. Priority — Real-World Example
**Severity** measures how badly the defect breaks the system. **Priority** measures how urgently it needs to be fixed relative to business needs — they are independent dimensions.

Example: A typo in the CEO's name on the admin dashboard's welcome banner has **Low Severity** (nothing is broken, no data is affected) but can have **High Priority** (it needs to be fixed immediately before the CEO sees it, for reputational/political reasons) — demonstrating that High Severity does not always mean High Priority, and vice versa.
