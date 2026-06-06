from flask import Flask, jsonify
from flask_cors import CORS

from app.core.config import settings
from app.core.database import engine, Base
from app.routes import products, customers, orders, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Configure CORS
CORS(
    app,
    origins=settings.ALLOWED_ORIGINS,
    allow_headers=["Content-Type", "Authorization", "*"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    supports_credentials=True,
    max_age=3600
)

# Register blueprints
app.register_blueprint(products.bp)
app.register_blueprint(customers.bp)
app.register_blueprint(orders.bp)
app.register_blueprint(dashboard.bp)


@app.route("/", methods=["GET"])
def read_root():
    """Root endpoint"""
    return jsonify({
        "message": "Welcome to Inventory Management System",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json"
    })


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    })
