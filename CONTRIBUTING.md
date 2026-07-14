# Contributing

Thanks for wanting to contribute! This file explains how to run the tests locally, the repository conventions (page objects, tests and fixtures), and the expectations for pull requests so contributions are fast to review and easy to maintain.

## Table of contents

- Getting started
- Running tests locally
- Repository structure and conventions
- Page Object Model (POM) guidelines
- Writing tests
- Fixtures and test data
- Style, linting and formatting
- Running tests in parallel / flakiness
- Pull request process
- Adding CI

## Getting started

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
python -m playwright install
# or install specific browsers
python -m playwright install chromium firefox webkit
```

## Running tests locally

The project configures pytest via `pyproject.toml`. The default `addopts` includes multiple browsers and parallel workers. Common commands:

- Run the whole test suite (uses `pyproject.toml` addopts):

```bash
pytest
```

- Run smoke tests only:

```bash
pytest -m smoke
```

- Run a single browser:

```bash
pytest --browser chromium
```

- Run a single test function:

```bash
pytest tests/test_login_pom.py::test_invalid_credentials -q
```

- Override the base URL (useful for staging):

```bash
pytest --base-url https://staging.example.com
```

Notes:
- `-n N` parallelism is provided by `pytest-xdist`. Parallel runs may reveal shared-state issues in tests or fixtures.
- `pytest-playwright` provides the `--browser` option used in `pyproject.toml`.

## Repository structure and conventions

- `pages/` — Page Object classes. Each file defines a single page class that exposes navigation, actions and accessors.
- `tests/` — pytest test modules. Tests should be readable and keep assertions at the behavioral level.
- `conftest.py` — fixtures shared across tests (login flows and pre-filled carts).
- `test_data.py` — simple data used by tests (users, expected messages, checkout info).
- `requirements.txt` — pinned dependencies for the project.

Naming conventions:
- Page object classes use `CamelCase` and filenames are snake_case, e.g. `pages/inventory_page.py` defines `InventoryPage`.
- Tests are `tests/test_<area>_pom.py` or similar; test functions use `snake_case` and descriptive names.

## Page Object Model (POM) guidelines

When adding or updating page objects follow these guidelines:

- Single responsibility: one class per page. Keep methods small and descriptive (e.g. `add_backpack()`, `get_cart_count()`).
- Use Playwright locators on the class `__init__` when they are reused; avoid defining locators inside many methods.
- Expose actions (verbs) and accessors (get_*, is_*).
- Keep navigation methods explicit (e.g. `navigate()` or `wait_until_loaded()`). Tests should call navigation helpers from POM when it makes the test clearer.
- Use data-test attributes where possible. When a selector must change for visual reasons, prefer attributes like `[data-test='add-to-cart-sauce-labs-backpack']` rather than brittle CSS selectors.

Example pattern:

```python
class SomePage:
    def __init__(self, page):
        self.page = page
        self.submit = page.locator("[data-test='submit']")

    def do_submit(self):
        self.submit.click()

    def get_status(self):
        return self.page.locator('.status').inner_text()
```

## Writing tests

- Tests should be focused and exercise one behavior. Arrange/Act/Assert is a helpful pattern.
- Prefer using page objects and fixtures to keep tests concise:

```python
def test_add_item_to_cart(add_backpack_to_cart):
    cart = CartPage(add_backpack_to_cart)
    assert cart.get_item_count() == 1
```

- Use Playwright's `expect()` helpers for visibility, text and state checks when possible (they include built-in waiting semantics).
- Mark slow or broad tests with markers (`@pytest.mark.smoke` is available). Explain in the test docstring if behavior is documenting a known bug or product choice.

## Fixtures and test data

- Keep fixtures small and composable. `conftest.py` currently provides:
  - `log_in_to_saucedemo` — logs in and returns a page on `/inventory.html`.
  - `add_backpack_to_cart` — uses `log_in_to_saucedemo` then adds a backpack and opens the cart.
  - `add_backpack_and_bike_light_to_cart` — adds two items and opens the cart.
- Add new fixtures in `conftest.py` as needed. If a fixture is expensive, consider using function scope and document why.

## Style, linting and formatting

- Keep code consistent and readable. We do not currently enforce linters, but please follow these conventions:
  - Use 4-space indentation for Python.
  - Use descriptive names for methods and variables.
  - Add docstrings to non-trivial helper functions.
- If you want, propose a pre-commit configuration (black/isort/flake8) in a follow-up PR.

## Running tests in parallel and flakiness

- The test configuration runs browsers in parallel (`-n 2` in `pyproject.toml`). When adding tests, avoid global mutable state that could cause tests to interfere with each other.
- If a test is flaky, try to:
  - Add explicit waits in the POM (`wait_for_selector`, or use `expect()` assertions that wait).
  - Avoid relying on absolute timing sleeps.
  - Reduce shared dependencies between tests or scope fixtures more narrowly.

## Pull request process

- Create a feature branch with a descriptive name (e.g. `feat/cart-page-remove-button` or `fix/login-error-message`).
- Keep changes small and focused.
- Include tests for new behaviors and update page objects as necessary.
- Ensure tests pass locally before opening the PR:

```bash
pytest -q
```

- In the PR description include:
  - What you changed and why.
  - Any test or environment prerequisites.
  - If the change impacts selectors or test structure, note the files to review.

## Adding CI

If you add CI (GitHub Actions), include steps to:
- Set up Python
- Install dependencies
- Run `python -m playwright install` to install browsers
- Run `pytest` (optionally in a single browser to save CI time)

A minimal example job step is:

```yaml
- name: Install Playwright browsers
  run: python -m playwright install --with-deps
- name: Run tests
  run: pytest --browser chromium -q
```

## Questions or help

If you're unsure about where to place a change or how to structure a POM, open a draft PR or an issue and tag the repository maintainers. We're happy to help iterate on design.
