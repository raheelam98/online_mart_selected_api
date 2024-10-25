from fastapi import  HTTPException, Depends
from sqlmodel import Session, select
from typing import Annotated, List

from app.db.db_connector import  DB_SESSION
from app.models.product_model import Product  #, ProductUpdateModel, ProductDetail #  , ProductModel
from app.models.categories_model import Size

# ### ============================================================================================================= ###

def search_product_by_name(name: str, session: Session) -> List[Product]:
    products = session.exec(
        select(Product).where(Product.product_name.ilike(f"%{name}%"))
    ).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found with this name.")
    
    return products

# ### ============================================================================================================= ###

def search_products_by_type(product_type: str, session: DB_SESSION) -> List[Product]:
    products = session.exec(
        select(Product).where(Product.product_type.ilike(f"%{product_type}%"))
    ).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found with this type.")
    return products

# ### ============================================================================================================= ###

def get_limited_products(limit: int, session: DB_SESSION):
    products = session.exec(select(Product).limit(limit)).all()
    return products

# ### ============================================================================================================= ###

def search_products_by_category(category_id: int, session: DB_SESSION):
    if category_id:
        products = session.exec(select(Product).where(
            Product.category_id == category_id)).all()
        if products:
            return products
        raise HTTPException(
            status_code=404, detail=f"Product not found from this category id: {category_id}")
    raise HTTPException(
        status_code=404, detail="you have not entered the category id")



### ============================================================================== ###

def search_specific_size_products(size_id: int, session: DB_SESSION):
    # Query for each Product with the given size_id
    results = session.exec(
        select(Product)
        .join(Size)
        .where(Size.size_id == size_id)
        .distinct()
    ).all()

    return results


# ### ============================================================================================================= ###




# ### ============================================================================================================= ###


# def search_products_by_category(category_id: int, session: DB_SESSION):
#     if category_id:
#         products = session.exec(select(Product).where(
#             Product.category_id == category_id)).all()
#         if products:
#             return products
#         raise HTTPException(
#             status_code=404, detail=f"Product not found from this category id: {category_id}")
#     raise HTTPException(
#         status_code=404, detail="you have not entered the category id")

# ### ============================================================================================================= ###
