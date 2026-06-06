from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Optional, List


# ==================== PRODUCT SCHEMAS ====================

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    price: float
    stock_quantity: int = Field(default=0, ge=0)

    @validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @validator("stock_quantity")
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = None
    stock_quantity: Optional[int] = Field(None, ge=0)

    @validator("price")
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @validator("stock_quantity")
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== CUSTOMER SCHEMAS ====================

class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== ORDER ITEM SCHEMAS ====================

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    @validator("product_id", "quantity")
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

    class Config:
        from_attributes = True


# ==================== ORDER SCHEMAS ====================

class OrderBase(BaseModel):
    customer_id: int

    @validator("customer_id")
    def validate_customer_id(cls, v):
        if v <= 0:
            raise ValueError("Customer ID must be greater than 0")
        return v


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_items=1)

    @validator("items")
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must contain at least one item")
        return v


class OrderResponse(OrderBase):
    id: int
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# ==================== DASHBOARD SCHEMAS ====================

class LowStockProduct(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock_quantity: int

    class Config:
        from_attributes = True


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
