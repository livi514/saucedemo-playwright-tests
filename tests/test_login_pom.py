import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data import ERROR_MESSAGES

# ---- Baseline checks (raw page, no POM) ------


@pytest.mark.smoke
def test_visibility_of_error(page):
    """Smoke test: the login page should load in a clean state with no error message visible."""

    # Arrange: open the login page
    page.goto("/")

    # Assert: error message must not appear before any user interaction
    error = page.locator("[data-test='error']")
    expect(error).not_to_be_visible()


@pytest.mark.smoke
def test_visibility_of_login_button(page):
    """Smoke test: the login button should be visible on the login page when it first loads."""

    # Arrange: open the login page
    page.goto("/")

    # Assert: login button should be visible before user interaction
    expect(page.locator("#login-button")).to_be_visible()


@pytest.mark.smoke
def test_login_button_enabled(page):
    """Smoke test: the login button should be enabled on the login page when it first loads."""

    # Arrange: open the login page
    page.goto("/")

    # Assert: login button should be enabled when the page first loads / before user interaction
    expect(page.locator("#login-button")).to_be_enabled()


@pytest.mark.smoke
def test_page_title(page):
    """Smoke test: the title 'Swag Labs' should be visible when the login page first loads"""

    # Arrange: open the login page
    page.goto("/")

    # Assert: the page should have the title 'Swag Labs' when it first loads
    expect(page).to_have_title("Swag Labs")


@pytest.mark.smoke
def test_username_placeholder_text(page):
    """Smoke test: the username input field should have the placeholder text 'Username' before user interaction"""

    # Arrange: open the login page
    page.goto("/")

    # Assert: the username input field has the correct placeholder text when the login page first loads
    username_input = page.locator("#user-name")
    expect(username_input).to_have_attribute("placeholder", "Username")


@pytest.mark.smoke
def test_password_placeholder_text(page):
    """Smoke test: the password input field should have the placeholder text 'Password' before user interaction"""

    # Arrange: open the login page
    page.goto("/")

    # Assert: the password input field has the correct placeholder text when the login page first loads
    password_input = page.locator("#password")
    expect(password_input).to_have_attribute("placeholder", "Password")


@pytest.mark.smoke
def test_login_button_text(page):
    """Smoke test: the login button should have the text 'Login' when the login page first loads"""

    # Arrange: open the login page
    page.goto("/")

    # Assert: the login button has the correct placeholder text
    button = page.locator("#login-button")
    expect(button).to_contain_text("Login")


@pytest.mark.smoke
def test_response_code(page):
    """Smoke test: the response code should be 200 OK when the login page first loads"""

    # Arrange: open the login page
    response = page.goto("/")

    # Assert: the page returns the expected response code
    assert response.status == 200


# ---- Successful login (fixture + POM) ------


def test_url_after_login(log_in_to_saucedemo):
    """This test checks that the URL is correct after a successful login using the log_in_to_saucedemo fixture, which uses the LoginPage POM to perform the login action."""

    # Assert: the URL is correct after a successful login
    expect(log_in_to_saucedemo).to_have_url("/inventory.html")


# ---- Failed login (POM) ------


def test_invalid_credentials(page):
    """This test checks that the error message is displayed when invalid credentials are used to log in using the LoginPage POM."""

    # Arrange: open the login page
    login = LoginPage(page)
    login.navigate()

    # Act: enter invalid credentials
    login.login_with_invalid_credentials()

    # Assert: the error message is displayed
    expect(login.error_message).to_contain_text(ERROR_MESSAGES["invalid_credentials"])


def test_empty_username_text(page):
    """This test checks that the error message is displayed when the username field is left empty during login using the LoginPage POM."""

    # Arrange: open the login page
    login = LoginPage(page)
    login.navigate()

    # Act: login with empty username
    login.login_with_empty_username()

    # Assert: the error message is displayed
    expect(login.error_message).to_contain_text(ERROR_MESSAGES["missing_username"])


def test_empty_password_text(page):
    """This test checks that the error message is displayed when the password field is left empty during login using the LoginPage POM."""

    # Arrange: open the login page
    login = LoginPage(page)
    login.navigate()

    # Act: login with empty password
    login.login_with_empty_password()

    # Assert: the error message is displayed
    expect(login.error_message).to_contain_text(ERROR_MESSAGES["missing_password"])
