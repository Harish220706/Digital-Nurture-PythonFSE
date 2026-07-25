# Hands-On 7 — Page Object Model

## Running the suite

```
cd handson_07
pip install -r ../requirements.txt
pytest tests/ -v --html=report.html --self-contained-html
```

`pytest.ini`/`conftest.py` adds the project root to the path implicitly when
run from `handson_07/`, so `from pages.simple_form_page import SimpleFormPage`
resolves correctly. If you see an import error, run pytest from inside the
`handson_07/` folder (not from a subfolder), or add `handson_07/` to
`PYTHONPATH`.

## Task 2, step 59 — Why POM matters

**Scenario**: The Submit button's ID changes from `submit` to `btn-submit`.

**In a flat (non-POM) script**: The locator `By.ID, "submit"` is likely
duplicated inline across every test file that clicks that button —
`test_simple_form.py`, `test_checkbox.py` (if it also has a submit action),
possibly a smoke test file, etc. When the ID changes, **every one of those
files** needs to be found and edited individually. If even one is missed,
that test silently starts failing (or throws a `NoSuchElementException`) and
someone has to debug it from scratch, not realizing the true cause was a
single HTML attribute change.

**With POM**: The locator exists in exactly one place — a class-level tuple
inside `simple_form_page.py` (e.g., `SUBMIT_BUTTON = (By.ID, "showInput")`).
When the underlying ID changes, you update **that one line, in that one
file**. Every test that calls `page.click_submit()` automatically picks up
the fix with zero changes to the test files themselves, because the tests
never referenced the locator directly — they only called a method name that
describes *what* the interaction does, not *how* it finds the element.

This is the core value proposition of POM: it converts an O(number of tests)
maintenance cost into an O(1) maintenance cost whenever the underlying UI
changes.
