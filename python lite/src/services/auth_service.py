from typing import Optional, Tuple, List, Dict
from ..models.user import User, UserRole, UserStatus
from ..utils.file_handler import FileHandler

class AuthService:
    USER_FILE = "data/users.txt"

    @classmethod
    def register(cls, username: str, password: str, role: str) -> Tuple[bool, str]:
        # Basic validation
        if not username or not password:
            return False, "Username and password cannot be empty"
            
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
            
        if ' ' in username:
            return False, "Username cannot contain spaces"
            
        if len(password) < 4:
            return False, "Password must be at least 4 characters long"

        users = FileHandler.read_data(cls.USER_FILE)
        
        # Check if username already exists (case-insensitive)
        if any(user["username"].lower() == username.lower() for user in users):
            return False, "Username already exists. Please choose a different username"

        # Validate role
        try:
            user_role = UserRole(role)
        except ValueError:
            return False, "Invalid role"

        # Manager role is not allowed for registration
        if user_role == UserRole.MANAGER:
            return False, "Cannot register as Manager"

        # Create new user
        user = User(username, password, user_role)
        FileHandler.append_data(cls.USER_FILE, user.to_dict())
        return True, "Registration successful. Waiting for approval."

    @classmethod
    def register_manager(cls, manager: User) -> None:
        users = FileHandler.read_data(cls.USER_FILE)
        if not any(user["username"] == manager.username for user in users):
            FileHandler.append_data(cls.USER_FILE, manager.to_dict())

    @classmethod
    def login(cls, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        users = FileHandler.read_data(cls.USER_FILE)
        
        for user_data in users:
            if user_data["username"] == username:
                user = User.from_dict(user_data)
                if user.password == password:
                    # Manager can always login regardless of status
                    if user.role == UserRole.MANAGER:
                        return True, "Login successful", user
                    
                    if user.status == UserStatus.BANNED:
                        return False, "Your account has been banned", None
                    if user.status == UserStatus.PENDING:
                        return False, "Your account is pending approval", None
                    return True, "Login successful", user
                return False, "Invalid password", None
                
        return False, "User not found", None

    @classmethod
    def get_all_users(cls) -> List[Dict]:
        users = FileHandler.read_data(cls.USER_FILE)
        # Filter out manager from the list for display
        return [user for user in users if user["role"] != UserRole.MANAGER.value]

    @classmethod
    def update_user_status(cls, username: str, new_status: UserStatus, actor: User) -> Tuple[bool, str]:
        if not isinstance(new_status, UserStatus):
            return False, "Invalid status"

        def update_condition(user):
            return user["username"] == username

        users = FileHandler.read_data(cls.USER_FILE)
        target_user = next((User.from_dict(u) for u in users if u["username"] == username), None)
        
        if not target_user:
            return False, "User not found"

        # Prevent modifying manager account
        if target_user.role == UserRole.MANAGER:
            return False, "Cannot modify Manager account"

        # Check permissions
        if actor.role == UserRole.ADMIN:
            if target_user.role in [UserRole.MANAGER, UserRole.ADMIN]:
                return False, "Admins cannot modify Manager or other Admin accounts"
        
        success = FileHandler.update_data(
            cls.USER_FILE,
            update_condition,
            {"status": new_status.value}
        )
        
        return success, "Status updated successfully" if success else "Failed to update status" 