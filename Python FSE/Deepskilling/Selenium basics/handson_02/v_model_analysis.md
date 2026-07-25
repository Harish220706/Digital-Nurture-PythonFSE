# SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### The V-Model

```
Requirements  ─────────────────────────────  Acceptance Testing
      \                                              /
       System Design ─────────────────  System Testing
              \                                /
               Architecture Design ── Integration Testing
                      \                    /
                       Module Design ─ Unit Testing
                              \        /
                               Coding
                          (bottom vertex)
```

Left side = development phases (top to bottom). Right side = corresponding testing phases (bottom to top), each verifying the deliverable produced by its paired development phase.

### Test artifact produced per phase

| SDLC Phase | Test Artifact Produced |
|---|---|
| Requirements | Acceptance Test Plan (defines what "done" looks like for the business) |
| System Design | System Test Plan (end-to-end scenarios covering the whole system) |
| Architecture Design | Integration Test Plan (how components/services are expected to interact) |
| Module Design | Unit Test Plan (test cases for individual functions/classes) |

### Entry & Exit Criteria per TDLC phase

**Unit Testing**
- Entry: Module design is complete; code compiles/builds successfully.
- Exit: All planned unit tests executed; code coverage meets the agreed threshold (e.g., 80%); no open critical defects at the unit level.

**Integration Testing**
- Entry: All required unit tests have passed; the components/services to be integrated are individually stable.
- Exit: All integration test cases executed; data flows correctly between integrated components; no open critical/high integration defects.

**System Testing**
- Entry: Integration testing is complete and signed off; the full system is deployed to a test environment resembling production.
- Exit: All planned system test cases executed; defect count below the agreed threshold; no open critical/high defects; system meets documented functional and non-functional requirements.

**Acceptance Testing (UAT)**
- Entry: System testing is complete and signed off; a UAT environment with representative data is available.
- Exit: Business stakeholders have executed and approved all acceptance criteria; sign-off is obtained to proceed to release.

### Two early QA engagement points (Course Management API project)
1. **Requirements review** — QA reviews user stories for the "create course" feature before any code is written, flagging ambiguous requirements (e.g., "what happens on a duplicate course code?") so they're clarified early rather than discovered as a bug later.
2. **Architecture/design review** — QA reviews the proposed API contract (endpoint shapes, status codes, error formats) during architecture design, catching testability issues (e.g., no way to reset test data between runs) before implementation begins.

## Task 2: Agile QA and Shift-Left Testing

### 3 problems with Waterfall's "test after development" approach
1. Defects found late are far more expensive to fix — a requirements misunderstanding discovered during system testing may require redesigning parts of the Course Management API from scratch.
2. QA has no influence on design decisions, so testability is often an afterthought (e.g., no way to seed test data, no staging environment with realistic data).
3. All testing is compressed into a short window at the end of the project, creating schedule pressure that leads to rushed, incomplete test coverage right before release.

### QA's role in Agile ceremonies
- **Sprint Planning**: QA helps define clear, testable Acceptance Criteria for each story before it's committed to the sprint (e.g., agreeing what "create course" must and must not allow).
- **Daily Standup**: QA reports blocking issues — e.g., "I can't test the create-course endpoint because the staging database migration hasn't run."
- **Sprint Review**: QA demonstrates tested functionality alongside developers, showing stakeholders that the feature actually works end-to-end, not just that code was written.
- **Retrospective**: QA raises process improvements — e.g., "we found 3 defects that could have been caught if unit tests covered edge cases; let's add a Definition of Done requirement for edge-case coverage."

### 4 Shift-Left practices applied to the Course Management API
1. **Reviewing requirements for testability** — Before development starts, QA asks: "What should happen if two admins submit the same course code simultaneously?" forcing that behavior to be specified upfront.
2. **Writing test cases before code (TDD/BDD)** — The team writes a Gherkin scenario for "create course" before the endpoint is implemented, so the acceptance criteria drive the implementation instead of the reverse.
3. **Static code analysis** — Running a linter/type-checker (e.g., `mypy`, `flake8`) on every commit to the API codebase catches basic errors before the code ever reaches a test environment.
4. **API contract testing before integration** — Using a schema (e.g., OpenAPI) to validate that the `POST /api/courses/` request/response shapes match what the frontend expects, before the frontend and backend teams integrate their work.

### Acceptance Criteria — Given-When-Then

**User Story**: As a college admin, I want to create a new course, so that students can enroll in it.

```gherkin
Scenario: Successfully create a new course (happy path)
  Given I am logged in as an admin
  And no course with the code "CS101" exists
  When I submit a new course with name "Data Structures" and code "CS101"
  Then the course is created successfully
  And I see "Data Structures" in the course list

Scenario: Reject duplicate course code
  Given I am logged in as an admin
  And a course with the code "CS101" already exists
  When I submit a new course with the code "CS101"
  Then I see an error message stating the course code already exists
  And no duplicate course is created

Scenario: Reject submission with missing required fields
  Given I am logged in as an admin
  When I submit a new course with the "name" field left blank
  Then I see a validation error indicating "name" is required
  And no course is created
```
