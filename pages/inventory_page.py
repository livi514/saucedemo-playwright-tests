from playwright.sync_api import expect


class InventoryPage:
    """Page object for the saucedemo.com inventory page."""

    def __init__(self, page):
        self.page = page

        # Static elements
        self.title = page.locator("span.title")
        self.cart_icon = page.locator("a.shopping_cart_link")
        self.cart_badge = page.locator("span.shopping_cart_badge")

        # Sort dropdown (actual <select> element)
        self.sort_dropdown = page.locator("select[data-test='product-sort-container']")

        # Product containers
        self.product_items = page.locator("div.inventory_item")
        self.product_names = page.locator("div.inventory_item_name")
        self.product_prices = page.locator("div.inventory_item_price")

        # Specific product buttons
        self.backpack_add_button = page.locator(
            "[data-test='add-to-cart-sauce-labs-backpack']"
        )
        self.backpack_remove_button = page.locator(
            "[data-test='remove-sauce-labs-backpack']"
        )
        self.bike_light_add_button = page.locator(
            "[data-test='add-to-cart-sauce-labs-bike-light']"
        )
        self.bike_light_remove_button = page.locator(
            "[data-test='remove-sauce-labs-bike-light']"
        )

    # Navigation
    def navigate(self):
        """Navigate directly to the inventory page."""
        self.page.goto("/inventory.html")

    def wait_until_loaded(self):
        """Wait for the inventory page to finish loading."""
        # Wait for the page title to appear
        self.page.wait_for_selector("span.title")
        # Wait for at least one product to render
        self.page.wait_for_selector("div.inventory_item")

    # Generic product actions — available for future tests
    def add_item(self, item_name):
        """Add any item to the cart by its data-test item name."""
        self.page.locator(f"[data-test='add-to-cart-{item_name}']").click()

    def remove_item(self, item_name):
        """Remove any item from the cart by its data-test item name."""
        self.page.locator(f"[data-test='remove-{item_name}']").click()

    # Specific product actions
    def add_backpack(self):
        """Add the Sauce Labs Backpack to the cart."""
        self.backpack_add_button.click()

    def add_bike_light(self):
        """Add the Sauce Labs Bike Light to the cart."""
        self.bike_light_add_button.click()

    def remove_backpack(self):
        """Remove the Sauce Labs Backpack from the cart."""
        self.backpack_remove_button.click()

    def remove_bike_light(self):
        """Remove the Sauce Labs Bike Light from the cart."""
        self.bike_light_remove_button.click()

    # Cart helpers
    def get_cart_count(self):
        """Return the number of items in the cart, or 0 if the badge is not visible."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def open_cart(self):
        """Click the cart icon to navigate to the cart page."""
        self.cart_icon.click()

    # Sorting helpers
    def sort_by(self, option):
        """Sort products by the given option value (e.g. 'az', 'za', 'lohi', 'hilo')."""
        self.sort_dropdown.select_option(option)

    # Specific sort methods — available for future tests
    def sort_by_price_low_to_high(self):
        """Sort products by price, low to high."""
        self.sort_dropdown.select_option("lohi")

    def sort_by_price_high_to_low(self):
        """Sort products by price, high to low."""
        self.sort_dropdown.select_option("hilo")

    def sort_by_name_ascending(self):
        """Sort products alphabetically A to Z."""
        self.sort_dropdown.select_option("az")

    def sort_by_name_descending(self):
        """Sort products alphabetically Z to A."""
        self.sort_dropdown.select_option("za")

    # Product accessors
    def get_product_names(self):
        """Return a list of all product names on the page."""
        return self.product_names.all_inner_texts()

    def get_product_prices(self):
        """Return a list of all product prices on the page as strings (e.g. '$29.99')."""
        return self.product_prices.all_inner_texts()

    # Available for future tests
    def get_product_count(self):
        """Return the number of products displayed on the page."""
        return self.product_items.count()

    def get_price_of(self, product_name):
        """Return the price of a specific product by name."""
        locator = (
            self.page.locator(f"text={product_name}")
            .locator("..")
            .locator(".inventory_item_price")
        )
        return locator.inner_text()

    # State helpers — available for future tests
    def is_loaded(self):
        """Return True if the inventory page title reads 'Products'."""
        return self.title.inner_text() == "Products"

    def is_sort_dropdown_visible(self):
        """Return True if the sort dropdown is visible."""
        return self.sort_dropdown.is_visible()

    def is_cart_icon_visible(self):
        """Return True if the cart icon is visible."""
        return self.cart_icon.is_visible()

    def is_cart_badge_visible(self):
        """Return True if the cart badge is visible."""
        return self.cart_badge.is_visible()

    # Visibility assertions
    def are_product_names_visible(self):
        """Assert that all 6 product names are visible on the page."""
        for i in range(6):
            expect(self.product_names.nth(i)).to_be_visible()

    def are_product_prices_visible(self):
        """Assert that all 6 product prices are visible on the page."""
        for i in range(6):
            expect(self.product_prices.nth(i)).to_be_visible()
