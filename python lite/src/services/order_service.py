from typing import List, Tuple, Dict
from datetime import datetime
from ..models.user import User
from ..models.item import Item
from ..utils.file_handler import FileHandler
from .inventory_service import InventoryService

class OrderService:
    CART_FILE = "data/cart.txt"
    ORDERS_FILE = "data/orders.txt"

    @classmethod
    def add_to_cart(cls, user: User, item_id: str, quantity: int) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be positive"

        item = InventoryService.get_item(item_id)
        if not item:
            return False, "Item not found"

        if item.quantity < quantity:
            return False, "Insufficient stock"

        cart_data = {
            "username": user.username,
            "item_id": item_id,
            "quantity": quantity,
            "timestamp": datetime.now().isoformat()
        }

        FileHandler.append_data(cls.CART_FILE, cart_data)
        return True, "Item added to cart"

    @classmethod
    def get_cart(cls, username: str) -> List[Dict]:
        all_cart_items = FileHandler.read_data(cls.CART_FILE)
        return [item for item in all_cart_items if item["username"] == username]

    @classmethod
    def checkout(cls, username: str) -> Tuple[bool, str]:
        cart_items = cls.get_cart(username)
        if not cart_items:
            return False, "Cart is empty"

        # Verify stock and calculate total
        total = 0
        for cart_item in cart_items:
            item = InventoryService.get_item(cart_item["item_id"])
            if not item or item.quantity < cart_item["quantity"]:
                return False, f"Insufficient stock for item {cart_item['item_id']}"
            total += item.price * cart_item["quantity"]

        # Create order
        order = {
            "username": username,
            "items": cart_items,
            "total": total,
            "status": "processing",
            "timestamp": datetime.now().isoformat()
        }

        # Update inventory
        for cart_item in cart_items:
            success, msg = InventoryService.update_item_quantity(
                cart_item["item_id"],
                -cart_item["quantity"]
            )
            if not success:
                return False, f"Failed to update inventory: {msg}"

        # Save order and clear cart
        FileHandler.append_data(cls.ORDERS_FILE, order)
        cls.clear_cart(username)
        return True, f"Order placed successfully. Total: ${total:.2f}"

    @classmethod
    def clear_cart(cls, username: str) -> None:
        cart_items = FileHandler.read_data(cls.CART_FILE)
        updated_cart = [item for item in cart_items if item["username"] != username]
        FileHandler.write_data(cls.CART_FILE, updated_cart)

    @classmethod
    def get_orders(cls, username: str = None) -> List[Dict]:
        orders = FileHandler.read_data(cls.ORDERS_FILE)
        if username:
            return [order for order in orders if order["username"] == username]
        return orders

    @classmethod
    def remove_item_from_all_carts(cls, item_id: str) -> None:
        cart_items = FileHandler.read_data(cls.CART_FILE)
        # Remove the item from all carts
        updated_cart = [item for item in cart_items if item["item_id"] != item_id]
        FileHandler.write_data(cls.CART_FILE, updated_cart) 