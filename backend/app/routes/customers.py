from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.exceptions import CustomerNotFound, EmailAlreadyExists
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerResponse, CustomerUpdate

bp = Blueprint("customers", __name__, url_prefix="/customers")


def get_db():
    """Get database session"""
    return SessionLocal()


@bp.route("/", methods=["POST"])
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        db = get_db()
        
        # Check if email already exists
        existing_customer = db.query(Customer).filter(Customer.email == data.get("email")).first()
        if existing_customer:
            raise EmailAlreadyExists()
        
        # Create new customer
        db_customer = Customer(**data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        
        result = {
            "id": db_customer.id,
            "full_name": db_customer.full_name,
            "email": db_customer.email,
            "phone_number": db_customer.phone_number,
            "address": db_customer.address
        }
        return jsonify(result), 201
    except EmailAlreadyExists:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/", methods=["GET"])
def get_customers():
    """Get all customers with pagination"""
    try:
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 10, type=int)
        
        db = get_db()
        customers = db.query(Customer).offset(skip).limit(limit).all()
        
        result = [
            {
                "id": c.id,
                "full_name": c.full_name,
                "email": c.email,
                "phone_number": c.phone_number,
                "address": c.address
            }
            for c in customers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get a specific customer by ID"""
    try:
        db = get_db()
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise CustomerNotFound()
        
        result = {
            "id": customer.id,
            "full_name": customer.full_name,
            "email": customer.email,
            "phone_number": customer.phone_number,
            "address": customer.address
        }
        return jsonify(result), 200
    except CustomerNotFound:
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update a customer"""
    try:
        data = request.get_json()
        db = get_db()
        
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise CustomerNotFound()
        
        # Update only provided fields
        for field, value in data.items():
            if value is not None:
                setattr(customer, field, value)
        
        db.commit()
        db.refresh(customer)
        
        result = {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        }
        return jsonify(result), 200
    except CustomerNotFound:
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        db = get_db()
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise CustomerNotFound()
        
        db.delete(customer)
        db.commit()
        
        return "", 204
    except CustomerNotFound:
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
