from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.models import Product, Customer, Order
from app.schemas.schemas import DashboardResponse, LowStockProduct

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

LOW_STOCK_THRESHOLD = 10


def get_db():
    """Get database session"""
    return SessionLocal()


@bp.route("/", methods=["GET"])
def get_dashboard():
    """Get dashboard statistics"""
    try:
        db = get_db()
        
        # Total products
        total_products = db.query(func.count(Product.id)).scalar() or 0
        
        # Total customers
        total_customers = db.query(func.count(Customer.id)).scalar() or 0
        
        # Total orders
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        
        # Low stock products (stock <= threshold)
        low_stock_products = db.query(Product).filter(
            Product.stock_quantity <= LOW_STOCK_THRESHOLD
        ).all()
        
        low_stock_list = [
            {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "price": float(product.price),
                "stock_quantity": product.stock_quantity
            }
            for product in low_stock_products
        ]
        
        result = {
            "total_products": total_products,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "low_stock_products": low_stock_list,
            "low_stock_threshold": LOW_STOCK_THRESHOLD
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
