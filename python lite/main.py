from src.models.user import User, UserRole, UserStatus
from src.models.item import Item
from src.services.auth_service import AuthService
from src.services.inventory_service import InventoryService
from src.services.order_service import OrderService
import os
import json

def initialize_system():
    """Create necessary directories and files if they don't exist"""
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Initialize empty files with valid JSON
    files = [
        "data/users.txt",
        "data/inventory.txt",
        "data/cart.txt",
        "data/orders.txt"
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(options):
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    print("0. Exit")

def main_menu():
    while True:
        clear_screen()
        print("=== Computer Retail System ===")
        options = ["Login", "Register"]
        print_menu(options)
        
        choice = input("Enter your choice: ")
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def register():
    clear_screen()
    print("=== Registration ===")
    print("Note: Username must be unique and cannot contain spaces")
    print("-" * 40)
    
    while True:
        username = input("Enter username (or '0' to cancel): ").strip()
        if username == '0':
            return
        
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
            
        if ' ' in username:
            print("Username cannot contain spaces. Please try again.")
            continue
            
        if len(username) < 3:
            print("Username must be at least 3 characters long. Please try again.")
            continue
            
        password = input("Enter password: ").strip()
        if not password or len(password) < 4:
            print("Password must be at least 4 characters long. Please try again.")
            continue
        
        print("\nAvailable roles:")
        print("1. Customer")
        print("2. Admin")
        print("3. Inventory Staff")
        
        role_choice = input("Choose role (1-3): ")
        role_map = {
            "1": UserRole.CUSTOMER.value,
            "2": UserRole.ADMIN.value,
            "3": UserRole.INVENTORY.value
        }
        
        if role_choice not in role_map:
            print("Invalid role choice. Please try again.")
            input("Press Enter to continue...")
            continue
        
        success, message = AuthService.register(username, password, role_map[role_choice])
        if success:
            print("\nRegistration successful!")
            print("Note: Your account needs to be approved by an admin or manager before you can login.")
        else:
            print(f"\nRegistration failed: {message}")
        
        input("Press Enter to continue...")

def login():
    clear_screen()
    print("=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    success, message, user = AuthService.login(username, password)
    if success:
        if user.role == UserRole.CUSTOMER:
            customer_menu(user)
        elif user.role == UserRole.ADMIN:
            admin_menu(user)
        elif user.role == UserRole.INVENTORY:
            inventory_menu(user)
        elif user.role == UserRole.MANAGER:
            manager_menu(user)
    else:
        input(f"{message}\nPress Enter to continue...")

def customer_menu(user: User):
    while True:
        clear_screen()
        print(f"=== Customer Menu - {user.username} ===")
        options = ["View Items", "Add to Cart", "View Cart", "Checkout", "View Orders"]
        print_menu(options)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_items()
        elif choice == "2":
            add_to_cart(user)
        elif choice == "3":
            view_cart(user)
        elif choice == "4":
            checkout(user)
        elif choice == "5":
            view_orders(user)
        elif choice == "0":
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def admin_menu(user: User):
    while True:
        clear_screen()
        print(f"=== Admin Menu - {user.username} ===")
        options = ["Approve/Ban Users", "Generate Reports", "View All Orders"]
        print_menu(options)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            manage_users(user)
        elif choice == "2":
            generate_reports()
        elif choice == "3":
            view_all_orders()
        elif choice == "0":
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def inventory_menu(user: User):
    while True:
        clear_screen()
        print(f"=== Inventory Menu - {user.username} ===")
        options = ["Add Item", "Update Price", "Update Stock", "Delete Item", "View Items", "Generate Reports"]
        print_menu(options)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_item()
        elif choice == "2":
            update_price()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            view_items()
        elif choice == "6":
            generate_reports()
        elif choice == "0":
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def manager_menu(user: User):
    while True:
        clear_screen()
        print(f"=== Manager Menu - {user.username} ===")
        options = ["Approve/Ban Users", "Generate Reports", "View All Orders"]
        print_menu(options)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            manage_users(user)
        elif choice == "2":
            generate_reports()
        elif choice == "3":
            view_all_orders()
        elif choice == "0":
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def view_items():
    clear_screen()
    print("=== Available Items ===")
    items = InventoryService.get_all_items()
    if not items:
        input("No items available. Press Enter to continue...")
        return
    
    print("\nID | Name | Price | Quantity")
    print("-" * 40)
    for item in items:
        print(f"{item.item_id} | {item.name} | ${item.price:.2f} | {item.quantity}")
    input("\nPress Enter to continue...")

def add_to_cart(user: User):
    view_items()
    item_id = input("\nEnter item ID to add to cart: ")
    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        input("Invalid quantity. Press Enter to continue...")
        return
    
    success, message = OrderService.add_to_cart(user, item_id, quantity)
    input(f"{message}\nPress Enter to continue...")

def view_cart(user: User):
    clear_screen()
    print("=== Your Cart ===")
    cart_items = OrderService.get_cart(user.username)
    
    if not cart_items:
        input("Cart is empty. Press Enter to continue...")
        return
    
    total = 0
    print("\nItem | Quantity | Price | Subtotal")
    print("-" * 40)
    for cart_item in cart_items:
        item = InventoryService.get_item(cart_item["item_id"])
        if item:
            subtotal = item.price * cart_item["quantity"]
            total += subtotal
            print(f"{item.name} | {cart_item['quantity']} | ${item.price:.2f} | ${subtotal:.2f}")
    
    print(f"\nTotal: ${total:.2f}")
    input("\nPress Enter to continue...")

def checkout(user: User):
    success, message = OrderService.checkout(user.username)
    input(f"{message}\nPress Enter to continue...")

def view_orders(user: User):
    clear_screen()
    print("=== Your Orders ===")
    orders = OrderService.get_orders(user.username)
    
    if not orders:
        input("No orders found. Press Enter to continue...")
        return
    
    for order in orders:
        print(f"\nOrder Date: {order['timestamp']}")
        print(f"Status: {order['status']}")
        print(f"Total: ${order['total']:.2f}")
        print("Items:")
        for item in order['items']:
            print(f"- {item['item_id']}: {item['quantity']} units")
        print("-" * 40)
    
    input("\nPress Enter to continue...")

def view_all_orders():
    clear_screen()
    print("=== All Orders ===")
    orders = OrderService.get_orders()
    
    if not orders:
        input("No orders found. Press Enter to continue...")
        return
    
    for order in orders:
        print(f"\nUser: {order['username']}")
        print(f"Order Date: {order['timestamp']}")
        print(f"Status: {order['status']}")
        print(f"Total: ${order['total']:.2f}")
        print("-" * 40)
    
    input("\nPress Enter to continue...")

def manage_users(actor: User):
    while True:
        clear_screen()
        print("=== User Management ===")
        users = AuthService.get_all_users()
        
        if not users:
            input("No users found. Press Enter to continue...")
            return
        
        print("\nAvailable Users:")
        print("-" * 40)
        for idx, user in enumerate(users, 1):
            print(f"{idx}. {user['username']} | {user['role']} | {user['status']}")
        print("\n0. Back")
        
        try:
            choice = int(input("\nSelect user number (0 to go back): "))
            if choice == 0:
                break
            if choice < 1 or choice > len(users):
                raise ValueError()
            
            selected_user = users[choice - 1]
            print(f"\nSelected user: {selected_user['username']}")
            print("1. Approve")
            print("2. Ban")
            print("0. Cancel")
            
            action = input("Choose action (0-2): ")
            
            if action == "1":
                success, message = AuthService.update_user_status(
                    selected_user['username'], 
                    UserStatus.APPROVED, 
                    actor
                )
            elif action == "2":
                success, message = AuthService.update_user_status(
                    selected_user['username'], 
                    UserStatus.BANNED, 
                    actor
                )
            elif action == "0":
                continue
            else:
                message = "Invalid action"
            
            input(f"{message}\nPress Enter to continue...")
            
        except ValueError:
            input("Invalid selection. Press Enter to continue...")
            continue

def generate_reports():
    clear_screen()
    print("=== Reports ===")
    print("\n1. Sales Report")
    print("2. Inventory Report")
    report_type = input("Choose report type (1-2): ")
    
    if report_type == "1":
        orders = OrderService.get_orders()
        total_sales = sum(order['total'] for order in orders)
        print(f"\nTotal Sales: ${total_sales:.2f}")
        print(f"Total Orders: {len(orders)}")
    elif report_type == "2":
        items = InventoryService.get_all_items()
        total_items = sum(item.quantity for item in items)
        print(f"\nTotal Items in Stock: {total_items}")
        print("\nLow Stock Items (< 5 units):")
        for item in items:
            if item.quantity < 5:
                print(f"- {item.name}: {item.quantity} units")
    else:
        print("Invalid report type")
    
    input("\nPress Enter to continue...")

def add_item():
    clear_screen()
    print("=== Add New Item ===")
    item_id = input("Enter item ID: ")
    name = input("Enter item name: ")
    try:
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        input("Invalid price or quantity. Press Enter to continue...")
        return
    
    description = input("Enter description (optional): ")
    item = Item(item_id, name, price, quantity, description)
    success, message = InventoryService.add_item(item)
    input(f"{message}\nPress Enter to continue...")

def update_price():
    view_items()
    item_id = input("\nEnter item ID to update: ")
    try:
        new_price = float(input("Enter new price: "))
    except ValueError:
        input("Invalid price. Press Enter to continue...")
        return
    
    success, message = InventoryService.update_item_price(item_id, new_price)
    input(f"{message}\nPress Enter to continue...")

def update_stock():
    view_items()
    item_id = input("\nEnter item ID to update: ")
    try:
        quantity_change = int(input("Enter quantity change (positive to add, negative to remove): "))
    except ValueError:
        input("Invalid quantity. Press Enter to continue...")
        return
    
    success, message = InventoryService.update_item_quantity(item_id, quantity_change)
    input(f"{message}\nPress Enter to continue...")

def delete_item():
    clear_screen()
    print("=== Delete Item ===")
    print("Warning: Deleting an item will also remove it from all customer carts!")
    print("-" * 40)
    
    view_items()
    
    item_id = input("\nEnter item ID to delete (or '0' to cancel): ")
    if item_id == '0':
        return
        
    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ")
    if confirm.lower() != 'yes':
        input("Deletion cancelled. Press Enter to continue...")
        return
        
    success, message = InventoryService.delete_item(item_id)
    input(f"{message}\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        # Initialize system files and directories
        initialize_system()
        
        # Create default manager account if it doesn't exist
        manager = User("manager", "admin123", UserRole.MANAGER, UserStatus.APPROVED)
        AuthService.register_manager(manager)
        
        # Start the application
        main_menu()
    except Exception as e:
        print("\nAn error occurred:", str(e))
        print("\nIf this is the first time running the program, please make sure you're in the correct directory.")
        input("Press Enter to exit...") 