from typing import List, Tuple, Optional
from ..models.item import Item
from ..utils.file_handler import FileHandler

class InventoryService:
    INVENTORY_FILE = "data/inventory.txt"

    @classmethod
    def add_item(cls, item: Item) -> Tuple[bool, str]:
        items = FileHandler.read_data(cls.INVENTORY_FILE)
        
        # Check if item ID already exists
        if any(i["item_id"] == item.item_id for i in items):
            return False, "Item ID already exists"

        FileHandler.append_data(cls.INVENTORY_FILE, item.to_dict())
        return True, "Item added successfully"

    @classmethod
    def delete_item(cls, item_id: str) -> Tuple[bool, str]:
        items = FileHandler.read_data(cls.INVENTORY_FILE)
        
        # Check if item exists
        if not any(i["item_id"] == item_id for i in items):
            return False, "Item not found"

        # Remove item from inventory
        updated_items = [item for item in items if item["item_id"] != item_id]
        FileHandler.write_data(cls.INVENTORY_FILE, updated_items)

        # Import here to avoid circular import
        from .order_service import OrderService
        # Remove item from all customer carts
        OrderService.remove_item_from_all_carts(item_id)
        
        return True, "Item deleted successfully and removed from all carts"

    @classmethod
    def update_item_price(cls, item_id: str, new_price: float) -> Tuple[bool, str]:
        if new_price < 0:
            return False, "Price cannot be negative"

        def update_condition(item):
            return item["item_id"] == item_id

        success = FileHandler.update_data(
            cls.INVENTORY_FILE,
            update_condition,
            {"price": new_price}
        )
        return success, "Price updated successfully" if success else "Item not found"

    @classmethod
    def update_item_quantity(cls, item_id: str, quantity_change: int) -> Tuple[bool, str]:
        items = FileHandler.read_data(cls.INVENTORY_FILE)
        item = next((i for i in items if i["item_id"] == item_id), None)
        
        if not item:
            return False, "Item not found"

        new_quantity = item["quantity"] + quantity_change
        if new_quantity < 0:
            return False, "Insufficient quantity"

        def update_condition(item):
            return item["item_id"] == item_id

        success = FileHandler.update_data(
            cls.INVENTORY_FILE,
            update_condition,
            {"quantity": new_quantity}
        )
        return success, "Quantity updated successfully" if success else "Failed to update quantity"

    @classmethod
    def get_all_items(cls) -> List[Item]:
        items = FileHandler.read_data(cls.INVENTORY_FILE)
        return [Item.from_dict(item) for item in items]

    @classmethod
    def get_item(cls, item_id: str) -> Optional[Item]:
        items = FileHandler.read_data(cls.INVENTORY_FILE)
        item_data = next((i for i in items if i["item_id"] == item_id), None)
        return Item.from_dict(item_data) if item_data else None 