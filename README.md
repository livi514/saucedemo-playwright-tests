# saucedemo-playwright-tests

A Playwright test suite for the Sauce Demo web application. This repository contains automated end-to-end tests written in Python using Playwright and configured for local execution.

## Project Overview

- Tests cover the Sauce Demo app workflows such as login, product browsing, cart management, and checkout.
- Built for fast, reliable browser automation with Playwright Python.

## Prerequisites

- Python 3.10 or later
- pip
- Internet access to install dependencies

## Installation

1. Clone the repository.
2. Open a terminal in the project folder.
3. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Install Playwright browsers if needed:

```bash
python -m playwright install
```

## Running Tests

- Run the full test suite:

```bash
pytest
```

- Run a specific test file:

```bash
pytest tests/test_example.py
```

## Project Structure

- `tests/` - test files for Sauce Demo scenarios
- `requirements.txt` - Python dependencies
- `playwright.config.py` or project-specific Playwright config

## Notes

- Adjust test selectors or configuration if Sauce Demo page structure changes.
- Use `python -m pytest` if the repository requires a module invocation.
