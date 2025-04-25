from enum import Enum
from typing import List, Dict

class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    INVENTORY = "inventory"
    MANAGER = "manager"

class UserStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    BANNED = "banned"

class User:
    def __init__(self, username: str, password: str, role: UserRole, status: UserStatus = UserStatus.PENDING):
        self.username = username
        self.password = password
        self.role = role
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role.value,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(
            username=data["username"],
            password=data["password"],
            role=UserRole(data["role"]),
            status=UserStatus(data["status"])
        ) 