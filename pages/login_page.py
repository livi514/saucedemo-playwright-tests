from test_data import INVALID_USER, VALID_USER


class LoginPage:
    """Page object for the saucedemo.com login page."""

    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    # Navigation
    def navigate(self):
        """Navigate to the login page."""
        self.page.goto("/")

    # Field-level actions
    def fill_username(self, username):
        """Fill in the username field."""
        self.username_input.fill(username)

    def fill_password(self, password):
        """Fill in the password field."""
        self.password_input.fill(password)

    def click_login(self):
        """Click the login button."""
        self.login_button.click()

    # Combined action
    def login(self, username, password):
        """Fill in credentials and click the login button."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    # Common login scenarios
    def login_with_invalid_credentials(self):
        """Attempt login with invalid username and password."""
        self.login(INVALID_USER["username"], INVALID_USER["password"])

    def login_with_empty_username(self):
        """Attempt login with an empty username field."""
        self.login("", VALID_USER["password"])

    def login_with_empty_password(self):
        """Attempt login with an empty password field."""
        self.login(VALID_USER["username"], "")

    # Accessors
    def get_error_message(self):
        """Return the text of the error message."""
        return self.error_message.inner_text()

    def get_username_placeholder(self):
        """Return the placeholder text of the username input field."""
        return self.username_input.get_attribute("placeholder")

    def get_password_placeholder(self):
        """Return the placeholder text of the password input field."""
        return self.password_input.get_attribute("placeholder")

    # State helpers — available for future tests
    def is_error_visible(self):
        """Return True if the error message is visible."""
        return self.error_message.is_visible()

    def is_login_button_enabled(self):
        """Return True if the login button is enabled."""
        return self.login_button.is_enabled()

    def is_login_button_visible(self):
        """Return True if the login button is visible."""
        return self.login_button.is_visible()

    def is_on_inventory_page(self):
        """Return True if the current URL indicates the inventory page."""
        return self.page.url.endswith("/inventory.html")
