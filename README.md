# Simple-python-retail-system
it is about a python retail system  ; Four roles are assign : customer , manager , admin and Inventory staff  

                       
                                                                                
Author 

EMPG8999

Jinxing

                                                                                
                                                                                


# Computer Retail System

A simple command-line based computer retail system with role-based access control.

## Default Manager Credentials
- Username: manager
- Password: admin123

## Project Structure
```
computer_retail/
├── data/               # Data storage directory
│   ├── users.txt      # User information
│   ├── inventory.txt  # Inventory items
│   ├── cart.txt      # Shopping cart data
│   └── orders.txt    # Order history
├── src/               # Source code
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   └── utils/        # Utility functions
└── main.py           # Entry point
```

## Features
1. User Management
   - Registration (Customer, Admin, Inventory Staff)
   - Login
   - Status approval system

2. Role-based Access
   - Customer: Browse items, manage cart, place orders, track orders
   - Admin: Approve users, ban users, generate reports
   - Inventory Staff: Manage inventory, update prices, generate reports
   - Manager: All admin privileges plus ability to manage admins

## How to Run
1. Make sure you have Python 3.x installed
2. Navigate to the project directory
3. Run `python main.py` 
