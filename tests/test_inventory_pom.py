import re

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage

# Inventory page baseline checks
# These baseline tests check the state of the inventory page before any user interaction
# (i.e. the user has just logged in and been taken to the inventory page)


@pytest.mark.smoke
def test_pom_inventory_page_title(log_in_to_saucedemo):
    """Smoke test: the inventory page should have the title 'Products' before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the page should have the title 'Products'
    expect(inventory.title).to_have_text("Products")


@pytest.mark.smoke
def test_pom_cart_icon_visible(log_in_to_saucedemo):
    """Smoke test: the cart icon should be visible on the inventory page, before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the cart icon should be visible
    expect(inventory.cart_icon).to_be_visible()


@pytest.mark.smoke
def test_pom_number_of_products(log_in_to_saucedemo):
    """Smoke test: there should be 6 products displayed on the page, before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: there should be 6 'Product names' displayed
    expect(inventory.product_names).to_have_count(6)


@pytest.mark.smoke
def test_pom_sort_dropdown_visible(log_in_to_saucedemo):
    """Smoke test: the drop-down menu for sort options should be visible, before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the drop-down menu should be visible
    expect(inventory.sort_dropdown).to_be_visible()


@pytest.mark.smoke
def test_pom_sort_dropdown_options(log_in_to_saucedemo):
    """Smoke test: the drop down options should be visible and have the text 'Name (A to Z)Name (Z to A)Price (low to high)Price (high to low)'"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the drop-down menu should have the expected text
    expect(inventory.sort_dropdown).to_have_text(
        "Name (A to Z)Name (Z to A)Price (low to high)Price (high to low)"
    )


@pytest.mark.smoke
def test_pom_sort_dropdown_default_value(log_in_to_saucedemo):
    """Smoke test: the default option in the drop-down menu should be 'az'"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the drop-down menu should have the default option 'az'
    expect(inventory.sort_dropdown).to_have_value("az")


@pytest.mark.smoke
def test_pom_cart_badge_not_visible(log_in_to_saucedemo):
    """Smoke test: the cart badge should not be visible before the user has added items to the cart"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the cart badge is not visible
    expect(inventory.cart_badge).not_to_be_visible()


@pytest.mark.smoke
def test_pom_product_names_visible(log_in_to_saucedemo):
    """Smoke test: the product names should be visible before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the product names are visible
    inventory.are_product_names_visible()


@pytest.mark.smoke
def test_pom_product_prices_visible(log_in_to_saucedemo):
    """Smoke test: the product prices should be visible before any user interaction"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Assert: the product prices are visible
    inventory.are_product_prices_visible()


# Adding and removing items from cart


def test_pom_add_and_remove_item_from_cart(log_in_to_saucedemo):
    """Test adding and removing items from the cart, and that the inventory cart badge and button text update accordingly"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Act: add backpack to cart
    inventory.add_backpack()

    # Assert: cart badge shows 1 item, and button shows text "Remove"
    expect(inventory.cart_badge).to_have_text("1")
    expect(inventory.backpack_remove_button).to_have_text("Remove")

    # Act: remove backpack from cart
    inventory.remove_backpack()

    # Assert: cart badge no longer visible, and button text is updated to "Add to cart"
    expect(inventory.cart_badge).not_to_be_visible()
    expect(inventory.backpack_add_button).to_have_text("Add to cart")


def test_pom_add_two_items_to_cart(log_in_to_saucedemo):
    """Test adding two items to the cart, and that the inventory cart badge and button texts update accordingly"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Act: add backpack and bike light to cart
    inventory.add_backpack()
    inventory.add_bike_light()

    # Assert: cart badge shows "2" and buttons for both items show text "Remove"
    expect(inventory.cart_badge).to_have_text("2")
    expect(inventory.backpack_remove_button).to_have_text("Remove")
    expect(inventory.bike_light_remove_button).to_have_text("Remove")


# Sorting tests


@pytest.mark.parametrize(
    "sort_value, expected_order",
    [
        ("az", "ascending"),
        ("za", "descending"),
    ],
)
def test_pom_sort_by_name(log_in_to_saucedemo, sort_value, expected_order):
    """Parameterised test to check that items appear in the expected order when sorted in alphabetical or reverse alphabetical order"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Capture the expected order before changing the sort option.
    expected_names = inventory.get_product_names()
    expected_names.sort(reverse=expected_order == "descending")

    # Act: select sort option
    inventory.sort_by(sort_value)

    # Assert: names are in the expected order
    expect(inventory.product_names).to_have_text(expected_names)


@pytest.mark.parametrize(
    "sort_value, expected_order", [("lohi", "ascending"), ("hilo", "descending")]
)
def test_pom_sort_by_price(log_in_to_saucedemo, sort_value, expected_order):
    """Parameterised test to check that items appear in the expected order when sorted in ascending or descending price order"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Capture the expected order before changing the sort option.
    expected_prices = inventory.get_product_prices()
    expected_prices.sort(
        key=lambda price: float(price.replace("$", "")),
        reverse=expected_order == "descending",
    )

    # Act: select sort option
    inventory.sort_by(sort_value)

    # Assert: prices are in the expected order
    expect(inventory.product_prices).to_have_text(expected_prices)


# Navigation to cart page


def test_pom_url_after_clicking_cart(log_in_to_saucedemo):
    """Test to check that the cart button navigates to the cart page"""

    # Arrange: open the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()

    # Act: click cart button
    inventory.open_cart()

    # Assert: URL is as expected
    expect(log_in_to_saucedemo).to_have_url(re.compile("cart"))
