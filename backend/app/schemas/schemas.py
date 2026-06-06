from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List


# ==================== PRODUCT SCHEMAS ====================

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    stock_quantity: int = 0

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or len(v) < 1 or len(v) > 255:
            raise ValueError("Name must be between 1 and 255 characters")
        return v

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v):
        if not v or len(v) < 1 or len(v) > 100:
            raise ValueError("SKU must be between 1 and 100 characters")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("stock_quantity")
    @classmethod
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== CUSTOMER SCHEMAS ====================

class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if not v or len(v) < 1 or len(v) > 255:
            raise ValueError("Full name must be between 1 and 255 characters")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is not None and len(v) > 20:
            raise ValueError("Phone number must be at most 20 characters")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError("Address must be at most 500 characters")
        return v


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== ORDER ITEM SCHEMAS ====================

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    @field_validator("product_id", "quantity")
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Value must be greater than 0")
        return v


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


# ==================== ORDER SCHEMAS ====================

class OrderBase(BaseModel):
    customer_id: int

    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, v):
        if v <= 0:
            raise ValueError("Customer ID must be greater than 0")
        return v


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must contain at least one item")
        return v


class OrderResponse(OrderBase):
    id: int
    total_amount: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


# ==================== DASHBOARD SCHEMAS ====================

class LowStockProduct(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: List[LowStockProduct]
    low_stock_threshold: int = 10


# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
