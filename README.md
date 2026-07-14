# Saucedemo Playwright Tests

A Playwright test suite for the Sauce Demo web application. Tests are written in Python using Playwright and organised using the Page Object Model (POM). The suite is configured to run locally and is set up to run across multiple browsers by default.

## Quick summary
- Language: Python (3.10+)
- Test runner: pytest + pytest-playwright
- Pattern: Page Object Model under `pages/`
- Tests: under `tests/`
- Test data / fixtures: `test_data.py` and `conftest.py`
- Pytest configuration: `pyproject.toml` (contains addopts such as browsers, parallelism and base-url)

## What’s included
- pages/
  - login_page.py — login page object (navigation, login helpers, error state).
  - inventory_page.py — product listing, sort, cart interactions.
  - cart_page.py — cart item actions and accessors.
  - checkout_page.py — checkout flow helpers and totals parsing.
  - menu_page.py — site menu and logout.
- tests/ — tests that exercise login, inventory listing/sorting, cart behavior and checkout.
- conftest.py — fixtures:
  - log_in_to_saucedemo: logs in using VALID_USER and returns a page at /inventory.html
  - add_backpack_to_cart: logs in and adds the backpack then opens the cart
  - add_backpack_and_bike_light_to_cart: logs in and adds two items then opens the cart
- test_data.py — VALID_USER, INVALID_USER, CHECKOUT_INFO, and expected error messages.
- pyproject.toml — pytest configuration (testpaths + addopts). Note: this repo does not include a `playwright.config.py`.

## Prerequisites
- Python 3.10 or later
- pip
- Internet access to install dependencies and Playwright browsers

## Installation
1. Clone the repository:
   git clone https://github.com/livi514/saucedemo-playwright-tests.git
2. Create and activate a virtual environment (recommended):
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Install Playwright browsers:
   python -m playwright install
   # or install specific browsers
   python -m playwright install chromium firefox webkit

## Running tests
The repository configures pytest via `pyproject.toml`. By default the addopts include:
--browser chromium --browser firefox --browser webkit -n 2 --base-url https://www.saucedemo.com

Basic commands:
- Run the full suite (uses pyproject.toml addopts):
  `pytest`
- Run smoke-marked tests:
  `pytest -m smoke`
- Run a single browser:
  `pytest --browser chromium`
- Run a single test:
  `pytest tests/test_login_pom.py::test_invalid_credentials`
- Override the base URL:
  `pytest --base-url https://staging.example.com`
- Run tests with verbose output:
  `pytest -vv`

Notes:
- `-n 2` (pytest-xdist) enables parallel workers — take care with tests that share mutable global state.
- `pytest-playwright` exposes the `--browser` option used here.

## How the tests are organised
- The tests use a Page Object Model: each page class exposes actions and accessors so tests remain expressive and focused on behaviour.
- Common flows (login, adding items) are exposed via fixtures in `conftest.py` to reduce duplication.
- Assertions use Playwright's `expect` helpers where applicable.

## Troubleshooting
- Tests fail due to selector changes: update the locator in the corresponding page class under `pages/`.
- Flaky tests with parallel runs: reduce `-n` workers or mark tests to avoid shared state.
- If Playwright cannot find browsers: re-run `python -m playwright install`.
