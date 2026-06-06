from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.core.exceptions import (
    ProductNotFound,
    SKUAlreadyExists,
    NegativeStockError
)
from app.models.models import Product, OrderItem
from app.schemas.schemas import ProductCreate, ProductResponse, ProductUpdate

bp = Blueprint("products", __name__, url_prefix="/products")


def get_db():
    """Get database session"""
    return SessionLocal()


@bp.route("/", methods=["POST"])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        db = get_db()
        
        # Check if SKU already exists
        existing_product = db.query(Product).filter(Product.sku == data.get("sku")).first()
        if existing_product:
            raise SKUAlreadyExists()
        
        # Validate stock is not negative
        if data.get("stock_quantity", 0) < 0:
            raise NegativeStockError()
        
        # Create new product
        db_product = Product(**data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        result = {
            "id": db_product.id,
            "name": db_product.name,
            "sku": db_product.sku,
            "price": float(db_product.price),
            "stock_quantity": db_product.stock_quantity
        }
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/", methods=["GET"])
def get_products():
    """Get all products with pagination"""
    try:
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 10, type=int)
        
        db = get_db()
        products = db.query(Product).offset(skip).limit(limit).all()
        
        result = [
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "price": float(p.price),
                "stock_quantity": p.stock_quantity
            }
            for p in products
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        db = get_db()
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFound()
        
        result = {
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "price": float(product.price),
            "stock_quantity": product.stock_quantity
        }
        return jsonify(result), 200
    except ProductNotFound:
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a product"""
    try:
        data = request.get_json()
        db = get_db()
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFound()
        
        # If SKU is being updated, check for duplicates
        if "sku" in data and data["sku"] != product.sku:
            existing = db.query(Product).filter(Product.sku == data["sku"]).first()
            if existing:
                raise SKUAlreadyExists()
        
        # Update only provided fields
        for field, value in data.items():
            if value is not None:
                setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        result = {
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "price": float(product.price),
            "stock_quantity": product.stock_quantity
        }
        return jsonify(result), 200
    except ProductNotFound:
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product"""
    try:
        db = get_db()
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFound()
        
        db.delete(product)
        db.commit()
        
        return "", 204
    except ProductNotFound:
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
    if not product:
        raise ProductNotFound()
    
    db.delete(product)
    db.commit()
    
    return None
