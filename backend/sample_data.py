#!/usr/bin/env python
"""
Sample data generator for development
Run this to populate the database with sample data
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Sample products
PRODUCTS = [
    {
        "name": "Dell XPS 15 Laptop",
        "sku": "DELL-XPS-15-001",
        "price": 1299.99,
        "stock_quantity": 5
    },
    {
        "name": "Apple MacBook Pro 16",
        "sku": "APPLE-MBP-16-001",
        "price": 2499.99,
        "stock_quantity": 3
    },
    {
        "name": "Logitech MX Master 3",
        "sku": "LOGI-MX-MASTER-3",
        "price": 99.99,
        "stock_quantity": 15
    },
    {
        "name": "USB-C Hub 7-in-1",
        "sku": "USB-HUB-7IN1-001",
        "price": 49.99,
        "stock_quantity": 20
    },
    {
        "name": "Mechanical Keyboard",
        "sku": "MECH-KB-RGB-001",
        "price": 149.99,
        "stock_quantity": 8
    }
]

# Sample customers
CUSTOMERS = [
    {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1-555-0101"
    },
    {
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone_number": "+1-555-0102"
    },
    {
        "full_name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "phone_number": "+1-555-0103"
    },
    {
        "full_name": "Alice Williams",
        "email": "alice.williams@example.com",
        "phone_number": "+1-555-0104"
    },
    {
        "full_name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "phone_number": "+1-555-0105"
    }
]


def create_products():
    """Create sample products"""
    print("\n📦 Creating sample products...")
    product_ids = []
    
    for product in PRODUCTS:
        try:
            response = requests.post(
                f"{BASE_URL}/products",
                json=product,
                timeout=5
            )
            if response.status_code == 201:
                product_data = response.json()
                product_ids.append(product_data["id"])
                print(f"  ✅ Created: {product['name']}")
            else:
                print(f"  ❌ Failed: {product['name']} - {response.text}")
        except Exception as e:
            print(f"  ❌ Error: {product['name']} - {str(e)}")
    
    return product_ids


def create_customers():
    """Create sample customers"""
    print("\n👥 Creating sample customers...")
    customer_ids = []
    
    for customer in CUSTOMERS:
        try:
            response = requests.post(
                f"{BASE_URL}/customers",
                json=customer,
                timeout=5
            )
            if response.status_code == 201:
                customer_data = response.json()
                customer_ids.append(customer_data["id"])
                print(f"  ✅ Created: {customer['full_name']}")
            else:
                print(f"  ❌ Failed: {customer['full_name']} - {response.text}")
        except Exception as e:
            print(f"  ❌ Error: {customer['full_name']} - {str(e)}")
    
    return customer_ids


def create_orders(product_ids, customer_ids):
    """Create sample orders"""
    print("\n🛒 Creating sample orders...")
    
    sample_orders = [
        {"customer_id": customer_ids[0], "items": [{"product_id": product_ids[0], "quantity": 1}]},
        {"customer_id": customer_ids[1], "items": [{"product_id": product_ids[1], "quantity": 1}]},
        {"customer_id": customer_ids[2], "items": [
            {"product_id": product_ids[2], "quantity": 2},
            {"product_id": product_ids[3], "quantity": 1}
        ]},
        {"customer_id": customer_ids[3], "items": [{"product_id": product_ids[4], "quantity": 1}]},
    ]
    
    for order in sample_orders:
        try:
            response = requests.post(
                f"{BASE_URL}/orders",
                json=order,
                timeout=5
            )
            if response.status_code == 201:
                order_data = response.json()
                customer = next((c for c in CUSTOMERS if c["full_name"]), "Unknown")
                print(f"  ✅ Created order #{order_data['id']} - Total: ${order_data['total_amount']:.2f}")
            else:
                print(f"  ❌ Failed to create order - {response.text}")
        except Exception as e:
            print(f"  ❌ Error creating order - {str(e)}")


def main():
    """Main function"""
    print("=" * 60)
    print("📊 Inventory Management System - Sample Data Generator")
    print("=" * 60)
    
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend API is not responding correctly!")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend at {BASE_URL}")
        print(f"   Error: {str(e)}")
        print("   Make sure the backend is running on port 8000")
        return
    
    print("✅ Connected to backend API")
    
    # Create sample data
    product_ids = create_products()
    customer_ids = create_customers()
    
    if product_ids and customer_ids:
        create_orders(product_ids, customer_ids)
    
    print("\n" + "=" * 60)
    print("✅ Sample data created successfully!")
    print("=" * 60)
    print("\n📊 Dashboard Stats:")
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"  • Total Products: {stats['total_products']}")
            print(f"  • Total Customers: {stats['total_customers']}")
            print(f"  • Total Orders: {stats['total_orders']}")
            print(f"  • Low Stock Products: {len(stats['low_stock_products'])}")
    except Exception as e:
        print(f"  Could not fetch dashboard stats: {str(e)}")
    
    print("\n🎉 Ready to go! Visit http://localhost:3000")


if __name__ == "__main__":
    main()
