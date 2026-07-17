class CheckoutPage:
    """Page object for the saucedemo.com checkout flow (Your Information → Overview → Complete)."""

    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")

        # Step 1: Your Information
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")

        # Step 2: Overview
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_total_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")
        self.finish_button = page.locator("[data-test='finish']")

    # Actions
    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill in the checkout information form and click Continue."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        """Click the Finish button to complete the order."""
        self.finish_button.click()

    # Accessors
    def get_title_text(self) -> str:
        """Return the text of the current page title."""
        return self.title.inner_text()

    def get_cart_item_count(self) -> int:
        """Return the number of items displayed on the checkout overview page."""
        return self.cart_items.count()

    def get_item_names(self):
        """Return a list of item names displayed on the checkout overview page."""
        return self.item_names.all_inner_texts()

    def get_totals(self):
        """
        Parse and return the item total, tax, and order total as floats.
        Returns a tuple: (item_total, tax, total)
        """
        item_total_text = self.item_total_label.text_content()
        tax_text = self.tax_label.text_content()
        total_text = self.total_label.text_content()

        item_total_value = float(item_total_text.split("$")[1])
        tax_value = float(tax_text.split("$")[1])
        total_value = float(total_text.split("$")[1])

        return item_total_value, tax_value, total_value
