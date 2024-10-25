from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Literal
from datetime import date
import uuid

from app.models.auth_admin_model import Admin
from app.models.categories_model import Category, Size

### ============================================================================================================= ###

class ProductBase(SQLModel):
    product_code: int
    is_available: bool = False      # DEFAULT 'No',  -- yes/no
    product_description: str | None
    product_add_date : date = Field(default=date.today())
  
### ============================================================================================================= ###

class ProductDetail(SQLModel):
    product_name: str
    product_type: str 
    product_price : float
    advance_payment_percetage: float = Field(default=0)
    product_code: int
    is_available: bool = False      # DEFAULT 'No',  -- yes/no
    product_description: str | None
    category_id : int = Field(foreign_key="category.category_id")
    size_id : int = Field(foreign_key="size.size_id")
    
### ============================================================================================================= ###

class ProductModel(ProductBase, ProductDetail):
    pass

### ============================================================================================================= ###

class Product(ProductModel , table=True):
    product_id: Optional[int] = Field(default=None, primary_key=True)
    kid: str = Field(default_factory=lambda: uuid.uuid4().hex)


### ============================================================================================================= ###


class ProductUpdateModel(SQLModel):
    product_name: Optional[str]
    product_type: Optional[str]
    # product_size: Optional[str]
    # product_stock: Optional[str]
    product_price: Optional[float]
    is_available: Optional[bool]
    product_description: Optional[str]
    advance_payment_percetage: Optional[str]
  

### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###

# class ProductSize(SQLModel, table=True):
    
#     product_size_id: Optional[int] = Field(None, primary_key=True)
#     size_id: int = Field(foreign_key="size.size_id")
#     price: int = Field(gt=0)  # Price associated with this size
#     product_item_id: int = Field(foreign_key="productitem.item_id")
#     # One-to-one relationship with Stock
#     stock: "Stock" = Relationship(back_populates="product_size")
#     product_item: Optional["ProductItem"] = Relationship(
#         back_populates="sizes"
#     )  # Many-to-one relationship with ProductItem

# ### ============================================================================================================= ###

# class Stock(SQLModel, table=True):
    
#     stock_id: Optional[int] = Field(
#         default=None, primary_key=True)  # Primary key for Stock
#     # Foreign key linking to ProductSize
#     product_size_id: int = Field(foreign_key="productsize.product_size_id")
#     #stock: int = 0  # Stock level
#     product_size: Optional[ProductSize] = Relationship(
#         back_populates="stock")  # One-to-one relationship with ProductSize

# ### ============================================================================================================= ###

# class ProductItem(SQLModel, table=True):
    
#     item_id: Optional[int] = Field(
#         default=None, primary_key=True)  # Primary key for ProductItem
#     # Foreign key linking to Product
#     product_id: int = Field(foreign_key="product.product_id")
#     color: str

#     # # One-to-many relationship with ProductImage
#     # product_images: List["ProductImage"] = Relationship(
#     #     back_populates="product_item")
    
#     # Many-to-one relationship with Product
#     product: Optional[Product] = Relationship(back_populates="product_items")
#     # One-to-many relationship with ProductSize
#     sizes: List[ProductSize] = Relationship(back_populates="product_item")

# ### ============================================================================================================= ###

# ### ============================================================================================================= ###

