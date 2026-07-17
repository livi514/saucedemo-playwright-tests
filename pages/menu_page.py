class MenuPage:
    """Page object for the saucedemo.com burger menu, accessible from any page after login."""

    def __init__(self, page):
        self.page = page
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def open_menu(self):
        """Click the burger menu button to open the side menu."""
        self.menu_button.click()

    def logout(self):
        """Click the logout link to log out of the application."""
        self.logout_link.click()
