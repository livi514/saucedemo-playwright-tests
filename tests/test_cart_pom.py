import pytest
from playwright.sync_api import expect

from conftest import perform_login
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.menu_page import MenuPage


@pytest.mark.smoke
def test_empty_cart_state(log_in_to_saucedemo):
    """Smoke test: this test verifies that no items are displayed on the cart page, if the user navigated to it from the inventory page without adding any items to the cart"""

    # Arrange: navigate to the cart page from the inventory page (without adding any items to the cart)
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.open_cart()
    cart = CartPage(log_in_to_saucedemo)

    # Assert: there shouldn't be any items in the cart
    expect(cart.cart_items).to_have_count(0)


def test_add_item_to_cart(add_backpack_to_cart):
    """This test verifies that an item can be added to the cart and that the cart displays the correct information."""

    # Arrange: set up cart page with backpack
    cart = CartPage(add_backpack_to_cart)

    # Assert: check that the item is displayed with the correct details
    # assert that there's one item in the cart
    expect(cart.cart_items).to_have_count(1)
    # assert that the name of the first item is "Sauce Labs Backpack"
    expect(cart.item_names).to_have_text(["Sauce Labs Backpack"])
    # assert that the button on the "Sauce Labs Backpack" tile has the text "Remove"
    expect(cart.remove_backpack_button).to_have_text("Remove")


def test_remove_item_from_cart(add_backpack_to_cart):
    """This test verifies that an item can be removed from the cart and that the cart displays the correct information."""

    # Arrange: set up cart page with backpack
    cart = CartPage(add_backpack_to_cart)

    # Act: remove backpack from cart
    cart.remove_backpack()

    # Assert: check that the backpack no longer appears in the cart
    expect(cart.cart_items).to_have_count(0)


def test_removing_item_doesnt_affect_others(add_backpack_and_bike_light_to_cart):
    """This test verifies that removing one item from the cart does not affect other items in the cart."""

    # Arrange: set up cart page with backpack and bike light
    cart = CartPage(add_backpack_and_bike_light_to_cart)

    # Assert: check number of items in the cart, and item names
    expect(cart.cart_items).to_have_count(2)
    expect(cart.item_names).to_have_text(
        ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    )

    # Act: click on 'Remove' button for the backpack
    cart.remove_backpack()

    # Assert: check that the backpack no longer appears in the cart, but that the bike light still appears in the cart
    expect(cart.cart_items).to_have_count(1)
    expect(cart.item_names).to_have_text(["Sauce Labs Bike Light"])


def test_continue_shopping_button(add_backpack_to_cart):
    """This test verifies that clicking the 'Continue Shopping' button takes the user back to the inventory page."""

    # Arrange: set up cart page with backpack
    cart = CartPage(add_backpack_to_cart)

    # Act: click on the 'Continue Shopping' button
    cart.continue_shopping()

    # Assert: check that the inventory page is displayed
    inventory = InventoryPage(add_backpack_to_cart)
    expect(inventory.title).to_have_text("Products")


def test_persistence_with_continue_shopping_button(add_backpack_and_bike_light_to_cart):
    """This test verifies that clicking the 'Continue Shopping' button does not remove items from the cart."""

    # Arrange: set up cart page with backpack and bike light
    cart = CartPage(add_backpack_and_bike_light_to_cart)

    # Assert: check number of items in the cart
    expect(cart.cart_items).to_have_count(2)

    # Act: click on the 'Continue Shopping' button, then click on the cart button
    cart.continue_shopping()
    inventory = InventoryPage(add_backpack_and_bike_light_to_cart)
    inventory.open_cart()

    # Assert: check that the items are still in the cart and that the correct names are displayed
    expect(cart.cart_items).to_have_count(2)
    expect(cart.item_names).to_have_text(
        ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    )


def test_cart_persists_after_logout_and_login(add_backpack_and_bike_light_to_cart):
    """This test verifies that items in the cart persist after logging out and logging back in."""

    # Arrange: set up cart page with backpack and bike light
    cart = CartPage(add_backpack_and_bike_light_to_cart)

    # Assert: check number of items in the cart
    expect(cart.cart_items).to_have_count(2)

    # Act: log out by clicking on the menu button and then clicking 'Logout', then log back in and navigate back to the cart page
    menu = MenuPage(add_backpack_and_bike_light_to_cart)
    menu.open_menu()
    menu.logout()
    perform_login(add_backpack_and_bike_light_to_cart)
    # click on the cart button again
    inventory = InventoryPage(add_backpack_and_bike_light_to_cart)
    inventory.open_cart()

    # Assert: check that the items are still in the cart
    expect(cart.cart_items).to_have_count(2)
