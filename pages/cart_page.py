class CartPage:
    """Page object for the saucedemo.com cart page."""

    def __init__(self, page):
        self.page = page

        # Cart item containers
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")

        # Remove buttons for specific products
        self.remove_backpack_button = page.locator(
            "[data-test='remove-sauce-labs-backpack']"
        )
        self.remove_bike_light_button = page.locator(
            "[data-test='remove-sauce-labs-bike-light']"
        )

        # Navigation buttons
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")
        self.checkout_button = page.locator("[data-test='checkout']")

    # Actions
    def remove_backpack(self):
        """Remove the Sauce Labs Backpack from the cart."""
        self.remove_backpack_button.click()

    def remove_bike_light(self):
        """Remove the Sauce Labs Bike Light from the cart."""
        self.remove_bike_light_button.click()

    def continue_shopping(self):
        """Click the 'Continue Shopping' button to return to the inventory page."""
        self.continue_shopping_button.click()

    def checkout(self):
        """Click the 'Checkout' button to proceed to checkout."""
        self.checkout_button.click()

    # Accessors
    def get_item_count(self):
        """Return the number of items currently in the cart."""
        return self.cart_items.count()

    def get_item_names(self):
        """Return a list of item names currently displayed in the cart."""
        return self.item_names.all_inner_texts()

    def get_item_prices(self):
        """Return a list of item prices currently displayed in the cart."""
        return self.item_prices.all_inner_texts()

    def get_title_text(self):
        """Return the text of the page title."""
        return self.page.locator(".title").inner_text()
