# Contributing

Thanks for wanting to contribute! This file explains how to set up the project, run tests locally, how the code is organized, and what's expected from pull requests.

## Table of contents

- Getting started
- Running tests locally
- Repository structure and conventions
- Page Object Model (POM) guidelines
- Writing tests
- Fixtures and test data
- Code style and formatting
- Dealing with flaky tests
- Pull request process
- Setting up CI with GitHub Actions

## Getting started

1. Fork the repository and clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/saucedemo-playwright-tests.git
cd saucedemo-playwright-tests
```

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
```

## Running tests locally

This project uses pytest configured in `pyproject.toml`. By default, tests run across multiple browsers and with parallel workers.

**Common commands:**

- Run all tests:
```bash
pytest
```

- Run only smoke tests (quick tests):
```bash
pytest -m smoke
```

- Run tests in a single browser:
```bash
pytest --browser chromium
```

- Run a specific test:
```bash
pytest tests/test_login_pom.py::test_invalid_credentials -q
```

- Override the base URL (useful for testing staging environments):
```bash
pytest --base-url https://staging.example.com
```

**Notes:**
- Tests run in parallel using `pytest-xdist` (configured in `pyproject.toml`). If you see flaky behavior, try running with `-n 0` to disable parallel execution.
- `pytest-playwright` provides the `--browser` option and handles browser automation.

## Repository structure and conventions

- `pages/` — Page Object classes. Each file defines a single page class.
- `tests/` — Test modules. Each file tests a specific area of the application.
- `conftest.py` — Pytest fixtures shared across tests (login flows, pre-filled carts).
- `test_data.py` — Test data like user credentials and expected messages.
- `requirements.txt` — Pinned dependencies for reproducible installs.

**Naming conventions:**
- Page object classes: `CamelCase` (e.g., `InventoryPage`, `CartPage`)
- Page object files: `snake_case` (e.g., `inventory_page.py`, `cart_page.py`)
- Test files: `test_<feature>_pom.py` (e.g., `test_login_pom.py`)
- Test functions: `snake_case` with descriptive names (e.g., `test_user_can_add_item_to_cart`)

## Page Object Model (POM) guidelines

The Page Object Model keeps selectors and page interactions in one place. When the UI changes, you only update the Page Object, not every test.

**Key principles:**
- **Single responsibility:** One class per page
- **Reusable locators:** Define locators in `__init__` if they're used multiple times
- **Clear methods:** Use action verbs (`add_item()`, `click_checkout()`) and accessors (`get_price()`, `is_loaded()`)
- **Prefer data-test attributes:** Use `[data-test='...']` selectors instead of brittle CSS classes
- **Explicit navigation:** Include methods like `navigate()` or `wait_until_loaded()`

**Example:**

```python
class CartPage:
    def __init__(self, page):
        self.page = page
        self.checkout_button = page.locator("[data-test='checkout']")
        self.item_count = page.locator(".cart-count")

    def click_checkout(self):
        self.checkout_button.click()

    def get_item_count(self):
        return self.item_count.inner_text()

    def is_checkout_enabled(self):
        return self.checkout_button.is_enabled()
```

## Writing tests

Tests should be focused and check one behavior at a time. Use the Arrange/Act/Assert pattern:

```python
def test_add_item_to_cart(log_in_to_saucedemo):
    # Arrange
    inventory = InventoryPage(log_in_to_saucedemo)
    
    # Act
    inventory.add_backpack_to_cart()
    
    # Assert
    assert inventory.get_cart_count() == "1"
```

**Guidelines:**
- Keep tests concise by using Page Objects and fixtures
- Use Playwright's `expect()` assertions for visibility and state checks (they include automatic waits):
```python
from playwright.async_api import expect

expect(page.locator(".item")).to_be_visible()
expect(page.locator("h1")).to_contain_text("Products")
```
- Mark slow or broad tests with `@pytest.mark.smoke`
- If testing a known bug or edge case, document it in the test docstring

## Fixtures and test data

Fixtures are reusable test setup helpers. They're defined in `conftest.py`:

- `log_in_to_saucedemo` — Logs in and returns a page object at `/inventory.html`
- `add_backpack_to_cart` — Logs in, adds a backpack, and opens the cart
- `add_backpack_and_bike_light_to_cart` — Logs in and adds two items to the cart

**Adding new fixtures:**
- Add them to `conftest.py`
- Keep fixtures small and composable
- Use appropriate scope (usually `function` for independence)
- Add a docstring explaining what the fixture does

```python
@pytest.fixture
def log_in_to_saucedemo(page):
    """Log in with valid credentials and return the page."""
    page.goto("https://www.saucedemo.com")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    page.wait_for_load_state("networkidle")
    return page
```

## Code style and formatting

- Use 4-space indentation for Python
- Use descriptive names for variables and methods
- Add docstrings to non-trivial functions
- Keep lines reasonably short and readable

Currently no linters are enforced, but consider these tools for future PRs:
- `black` — Code formatter
- `isort` — Import sorter
- `flake8` — Linter

## Dealing with flaky tests

Flaky tests fail randomly. To prevent this:

- **Add explicit waits:** Use `page.wait_for_selector()` or Playwright's `expect()` assertions
- **Avoid `time.sleep()`:** Let Playwright handle timing automatically
- **Isolate tests:** Each test should be independent; avoid shared state between tests
- **Check fixture scope:** Use `scope='function'` (the default) to ensure tests don't interfere with each other
- **Reduce dependencies:** Minimize what each fixture does; break large setups into smaller pieces

Example of a flaky test:
```python
# Bad: assumes timing
inventory.add_item()
time.sleep(2)
assert inventory.get_cart_count() == "1"

# Good: waits for the element
inventory.add_item()
expect(inventory.cart_badge).to_be_visible()
assert inventory.get_cart_count() == "1"
```

## Pull request process

1. **Create a feature branch** with a descriptive name:
```bash
git checkout -b feat/add-logout-button-test
git checkout -b fix/inventory-page-selector
```

2. **Keep changes focused and small** — One feature or fix per PR

3. **Write tests for new features** and update Page Objects as necessary

4. **Run tests locally** before pushing:
```bash
pytest -q
```

5. **Write a clear PR description** including:
   - What you changed and why
   - Any test prerequisites or setup steps
   - Files that reviewers should focus on

6. **Push to your fork and open a PR** against the main repository

## Setting up CI with GitHub Actions

A minimal GitHub Actions workflow to run tests in CI:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Install Playwright browsers
        run: python -m playwright install --with-deps
      - name: Run tests
        run: pytest --browser chromium -q
```

This workflow:
- Sets up Python
- Installs dependencies
- Installs Playwright browsers
- Runs pytest with a single browser (faster in CI)

## Questions?

Not sure where to add something or how to structure a test? Open a draft PR or issue and ask for help. Happy to iterate on design and answer questions!
