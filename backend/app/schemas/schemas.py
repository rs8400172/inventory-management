from pydantic import BaseModel, Field, EmailStr, validator, constr, conint
from datetime import datetime
from typing import Optional, List


# ==================== PRODUCT SCHEMAS ====================

class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    sku: constr(min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)

    @validator("stock_quantity")
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

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
    full_name: constr(min_length=1, max_length=255)
    email: EmailStr
    phone_number: Optional[constr(max_length=20)] = None
    address: Optional[constr(max_length=500)] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: Optional[constr(min_length=1, max_length=255)] = None
    phone_number: Optional[constr(max_length=20)] = None
    address: Optional[constr(max_length=500)] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== ORDER ITEM SCHEMAS ====================

class OrderItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


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
    customer_id: int = Field(..., gt=0)


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
