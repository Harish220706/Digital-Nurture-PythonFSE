# Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### 5 criteria for deciding whether to automate a test case

Applied to: *"Test that `POST /api/courses/` returns 201 with the correct course data when valid input is provided."*

1. **Repetition** — This test will run on every code change (every commit/PR), making it an excellent automation candidate since it would otherwise be run manually hundreds of times.
2. **Stability of the feature** — The "create course" endpoint's contract is not expected to change frequently once released, so the automated test won't need constant rewriting.
3. **Business criticality** — Course creation is core functionality; a regression here directly blocks the primary use case of the system, justifying automated regression coverage.
4. **Objective, deterministic outcome** — The test has a single clear pass/fail condition (status code + response body match), which automates cleanly, unlike exploratory or subjective UI judgments.
5. **ROI over time** — Given how often this endpoint will be exercised across the project's lifetime, the upfront cost of automating it is quickly repaid compared to manually testing it every release.

### Automate vs. Manual decisions

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | Repetitive, runs on every change, deterministic outcome — ideal automation candidate. |
| (b) Exploratory testing of a new search feature | **Manual** | Exploratory testing relies on human judgment and creativity to discover unexpected issues; it isn't scripted by nature. |
| (c) Performance test: 100 concurrent users calling `GET /api/courses/` | **Automate** | Cannot realistically be done manually; requires a load-testing tool (e.g., Locust, JMeter) to simulate concurrency. |
| (d) UI test for the login form | **Automate** | Stable, repetitive, high-risk (blocks all access) — a strong Selenium automation candidate. |
| (e) Verify the API documentation (Swagger) is accurate | **Manual** | Requires human judgment to compare prose/documentation intent against behavior; low repetition frequency. |
| (f) Smoke test: verify the API is reachable after deployment | **Automate** | Runs after every deployment, simple deterministic check — perfect for a fast automated smoke test in the CI/CD pipeline. |

### Automation ROI calculation

- Manual execution time: 30 minutes per run
- Automation build time (one-time cost): 4 hours = 240 minutes
- Maintenance overhead: 20% extra time per run, starting after the 10th run

**Break-even without maintenance overhead**: 240 minutes ÷ 30 minutes per manual run = **8 runs** to pay back the initial investment (ignoring automated run time, which is typically much faster than 30 minutes, so this is a conservative floor).

**Accounting for 20% maintenance overhead after run 10**: Assume each automated run effectively costs ~30 min × 0.20 = 6 minutes of amortized maintenance time after run 10 (since maintenance is occasional, not per-run, this is treated as an average overhead). Even with this overhead, the 4-hour investment is recovered well before run 10, since the break-even point (8 runs) occurs *before* the overhead even begins to apply. From run 11 onward, savings continue to accumulate at roughly 24 minutes of net savings per run (30 minutes manual − ~6 minutes amortized maintenance), so automation remains strongly worthwhile long-term.

**Conclusion**: Automating this regression test pays for itself after approximately **8 runs**, and continues generating clear savings indefinitely afterward, even with ongoing maintenance overhead factored in.

### Flaky Tests

**Definition**: A flaky test is a test that produces inconsistent results (sometimes pass, sometimes fail) when run against the same code and same environment, with no actual change in the system under test.

**Example**: A Selenium test that clicks "Submit" and immediately asserts a success message is present, without waiting for the page to finish an async network call — it passes when the network responds quickly and fails when it responds a few hundred milliseconds slower.

**3 strategies to prevent/fix flaky tests**:
1. Replace all `time.sleep()` calls with explicit `WebDriverWait` + `ExpectedConditions`, so the test waits exactly as long as needed rather than a fixed guess.
2. Ensure test data isolation — each test creates and cleans up its own data instead of relying on shared state that other tests might modify concurrently.
3. Run suspected flaky tests repeatedly in isolation (e.g., `pytest --count=20`) to confirm they fail intermittently, then fix the root timing/data issue rather than adding a retry-until-pass wrapper that just hides the symptom.

## Task 2: Compare Automation Framework Types

| Framework | Description | Advantage | Disadvantage | When to use for Course Management |
|---|---|---|---|---|
| **Linear** | Tests are recorded/written as straight-line scripts with no reuse — each script does everything from scratch (open browser, log in, perform action, verify). | Very fast to write for a one-off check. | Massive duplication; any UI change requires editing every script that touches that element. | A single one-time smoke check before a demo, never intended to be maintained. |
| **Modular** | Common actions (e.g., "login", "create course") are broken into reusable functions that tests call. | Reduces duplication; a UI change only requires updating one function. | Still requires a programmer to write and maintain the functions; not accessible to non-technical testers. | Once the team has more than a handful of tests sharing the same login/navigation steps. |
| **Data-Driven** | Test logic is separated from test data; the same script runs multiple times with different input sets (e.g., from a CSV or JSON file). | Easily covers many input combinations without duplicating test logic. | Doesn't address UI-reuse across different *types* of tests, only data variation within one test. | Testing the "create course" form with dozens of valid/invalid input combinations. |
| **Keyword-Driven** | Test steps are expressed as keywords (e.g., "ClickButton", "EnterText") in a spreadsheet or table, interpreted by an underlying engine. | Non-technical team members can write and read test cases. | Significant upfront investment to build the keyword engine; can obscure what's actually happening under the hood. | A team with manual QA testers who need to contribute test scenarios without writing Python/Java. |
| **Hybrid** | Combines Modular reusability + Data-Driven parameterization, and optionally a lightweight keyword layer on top. | Gets the benefits of all approaches: reusable, data-parameterized, and accessible. | Most complex to design and set up initially. | A growing suite serving both developers (writing modular code) and manual QA (contributing data-driven cases) — the most common real-world choice. |

### Recommendation for the described scenario
The team needs: (1) 50 login combinations, (2) reused login steps across 20 tests, (3) both technical and non-technical contributors.

**Recommendation: Hybrid framework**, combining:
- **Modular** page-object-style login function reused across all 20 test cases.
- **Data-Driven** parameterization (e.g., `pytest.mark.parametrize` reading from a CSV) to run the same login test against all 50 user/password combinations.
- Optionally, a thin **Keyword-Driven** layer (a simple table mapping human-readable steps to Modular functions) if non-technical members need to contribute new scenarios without writing Python.

This combination satisfies reuse, data coverage, and accessibility simultaneously — no single pure framework type covers all three needs alone.

### Hybrid folder structure — Course Management frontend tests

```
CourseManagementTests/
├── config/
│   └── config.yaml              # base_url, browser, timeouts
├── data/
│   ├── login_credentials.csv    # 50 user/password combinations
│   └── course_test_data.json
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── course_page.py
├── utils/
│   ├── driver_factory.py        # WebDriver setup/teardown helpers
│   └── data_reader.py           # CSV/JSON loading helpers
├── tests/
│   ├── test_login.py            # parameterized with login_credentials.csv
│   └── test_course_management.py
├── conftest.py
└── requirements.txt
```
