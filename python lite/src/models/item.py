from typing import Dict

class Item:
    def __init__(self, item_id: str, name: str, price: float, quantity: int, description: str = ""):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

    def to_dict(self) -> Dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Item':
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            description=data.get("description", "")
        ) 