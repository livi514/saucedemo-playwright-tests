# Contributing

Thanks for wanting to contribute! This file explains how to set up the project, run tests locally, how the code is organized, and what's expected from pull requests.

## Table of contents

- Getting started
- Running tests locally
- Repository structure and conventions
- Page Object Model (POM) guidelines
- Writing tests
- Fixtures and test data
- Code style and linting
- Dealing with flaky tests
- Pull request process
- CI with GitHub Actions

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

3. Install dependencies (includes linters and formatters):
```bash
pip install -r requirements.txt
```

4. Set up pre-commit hooks (optional but recommended):
```bash
pip install pre-commit
pre-commit install
```

5. Install Playwright browsers:
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
- `requirements.txt` — Pinned dependencies for reproducible installs, including linters and formatters.
- `.github/workflows/` — GitHub Actions workflow(s) for CI (linting and cross-platform testing).

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

## Code style and linting

This project uses automated linting to keep code consistent and catch potential issues.

**Linting tools:**
- **`black`** — Auto-formats code for consistency
- **`isort`** — Sorts and organizes imports
- **`flake8`** — Checks for style issues and potential bugs

**Running linters manually:**

Format code with Black:
```bash
black .
```

Sort imports with isort:
```bash
isort .
```

Check for issues with flake8:
```bash
flake8 .
```

Run all at once:
```bash
black . && isort . && flake8 .
```

**Using pre-commit hooks (automatic):**

If you installed pre-commit (see "Getting started"), linters run automatically before each commit. To run them manually on all files:
```bash
pre-commit run --all-files
```

If linters find issues, they'll either fix them automatically (Black and isort) or report them for you to fix (flake8). You can then stage and commit the changes.

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

4. **Run linters** before pushing:
```bash
black . && isort . && flake8 .
```

5. **Run tests locally** to make sure everything works:
```bash
pytest -q
```

6. **Write a clear PR description** including:
   - What you changed and why
   - Any test prerequisites or setup steps
   - Files that reviewers should focus on

7. **Push to your fork and open a PR** against the main repository

## CI with GitHub Actions

This repo uses GitHub Actions (`.github/workflows/lint_and_test.yml`) to run linting and tests automatically on every push and pull request.

The workflow has two jobs:
- **lint** — runs Black, isort, and flake8
- **test** — runs the Playwright suite across Ubuntu, Windows, and macOS (matrix strategy), and only runs if linting passes (`needs: lint`)

You don't need to replicate this locally, but if you're debugging a CI failure, running the same linters and tests locally first (see "Running tests locally" and "Code style and linting" above) will usually reproduce the issue faster than waiting on CI.

## Questions?

Not sure where to add something or how to structure a test? Open a draft PR or issue and ask for help. Happy to iterate on design and answer questions!
