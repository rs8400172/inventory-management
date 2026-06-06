from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.core.exceptions import (
    OrderNotFound,
    CustomerNotFound,
    InsufficientStock,
    InvalidOrderData
)
from app.models.models import Order, OrderItem, Product, Customer
from app.schemas.schemas import (
    OrderCreate,
    OrderResponse,
    OrderDetailResponse,
    OrderItemCreate
)

bp = Blueprint("orders", __name__, url_prefix="/orders")


def get_db():
    """Get database session"""
    return SessionLocal()


@bp.route("/", methods=["POST"])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        db = get_db()
        
        # Validate customer exists
        customer = db.query(Customer).filter(Customer.id == data.get("customer_id")).first()
        if not customer:
            raise CustomerNotFound()
        
        # Validate and check stock for all items
        total_amount = 0.0
        order_items = []
        
        items = data.get("items", [])
        for item_data in items:
            product = db.query(Product).filter(Product.id == item_data.get("product_id")).first()
            if not product:
                raise InvalidOrderData(f"Product with ID {item_data.get('product_id')} not found")
            
            # Check stock availability
            if product.stock_quantity < item_data.get("quantity", 0):
                raise InsufficientStock(
                    product_name=product.name,
                    requested=item_data.get("quantity", 0),
                    available=product.stock_quantity
                )
            
            # Calculate item total
            item_total = product.price * item_data.get("quantity", 0)
            total_amount += item_total
            
            order_items.append({
                "product": product,
                "quantity": item_data.get("quantity", 0),
                "unit_price": product.price
            })
        
        # Create order
        db_order = Order(
            customer_id=data.get("customer_id"),
            total_amount=total_amount
        )
        db.add(db_order)
        db.flush()  # Flush to get order ID without committing
        
        # Create order items and reduce stock
        for item_info in order_items:
            product = item_info["product"]
            quantity = item_info["quantity"]
            
            # Create order item
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=item_info["unit_price"]
            )
            db.add(order_item)
            
            # Reduce stock
            product.stock_quantity -= quantity
        
        db.commit()
        db.refresh(db_order)
        
        result = {
            "id": db_order.id,
            "customer_id": db_order.customer_id,
            "total_amount": float(db_order.total_amount),
            "created_at": db_order.created_at.isoformat()
        }
        return jsonify(result), 201
    except CustomerNotFound:
        return jsonify({"error": "Customer not found"}), 404
    except (InsufficientStock, InvalidOrderData) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/", methods=["GET"])
def get_orders():
    """Get all orders with pagination"""
    try:
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 10, type=int)
        
        db = get_db()
        orders = db.query(Order).offset(skip).limit(limit).all()
        
        result = [
            {
                "id": o.id,
                "customer_id": o.customer_id,
                "total_amount": float(o.total_amount),
                "created_at": o.created_at.isoformat()
            }
            for o in orders
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Get a specific order with details"""
    try:
        db = get_db()
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFound()
        
        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price)
            }
            for item in order.order_items
        ]
        
        result = {
            "id": order.id,
            "customer_id": order.customer_id,
            "total_amount": float(order.total_amount),
            "created_at": order.created_at.isoformat(),
            "items": items
        }
        return jsonify(result), 200
    except OrderNotFound:
        return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete an order (and restore stock)"""
    try:
        db = get_db()
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFound()
        
        # Restore stock for all items in the order
        for item in order.order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock_quantity += item.quantity
        
        db.delete(order)
        db.commit()
        
        return "", 204
    except OrderNotFound:
        return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
