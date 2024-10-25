from fastapi import  HTTPException, Depends
from sqlmodel import Session, select
from typing import Annotated, List

from app.db.db_connector import  DB_SESSION
from app.models.product_model import Product, ProductUpdateModel, ProductDetail #  , ProductModel

from app.utils.auth_admin import admin_required

### ============================================================================================================= ###

def get_product_from_db(session: DB_SESSION):
    porduct = session.exec(select(Product)).all() 
    if not porduct:
        HTTPException(status_code=400, detail="Product not found")
    return porduct 

### ============================================================================================================= ###

def create_product_by_admin(
    form_data: ProductDetail,
    session: Session
    
):
    product = Product(**form_data.model_dump())

    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    session.add(product)
    session.commit()
    session.refresh(product)
    return product 

### ============================================================================================================= ###

# def create_product_by_admin_111(product_form: ProductDetail, session: Session, admin_verification: Annotated[dict, Depends(admin_required)]):
   
#     product = Product(**product_form.model_dump())

#     print('Product ....1')
#     if not product:
#         raise HTTPException(status_code=404, detail="Product Not Found")
    
#     print("create_product_func 1")
#     ###Check if the user is an admin
#     if not admin_verification:
#         raise HTTPException(
#             status_code=403, detail="You are not authorized to create a product!"
#         )

#     # Add the product to the session
#     session.add(product)
#     # Commit the session to save the product to the database
#     session.commit()
#     # Refresh the session to retrieve the new product data, including generated fields like product_id
#     session.refresh(product)
#     # Return the created product
#     print('Product end....', product)
#     return product



# ### ============================================================================================================= ###


def add_product_in_db(product_form: ProductDetail, session: Session):
    # Convert ProductModel to Product instance
    #product = Product(**product_form.dict())
    product = Product(**product_form.model_dump())

    print('Product ....1')
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    

    # Add the product to the session
    session.add(product)
    # Commit the session to save the product to the database
    session.commit()
    # Refresh the session to retrieve the new product data, including generated fields like product_id
    session.refresh(product)
    # Return the created product
    print('Product end....', product)
    return product

### ============================================================================================================= ###


def update_product_in_db(selected_id: int, product_form: ProductUpdateModel, session: DB_SESSION):
    # Construct a query to select the product with the specified product_id
    product_query = select(Product).where(Product.product_id == selected_id)
    
    # Execute the query and get the first result
    product_statment = session.exec(product_query).first()
    
    # If no product is found with the given ID, raise a 404 HTTPException
    if not product_statment:
        raise HTTPException(status_code=404, detail="Product is unavailable")
    
    # Update the fields of the product with the values from the product_form object
    if product_form.product_name is not None:
        product_statment.product_name = product_form.product_name
    if product_form.product_type is not None:
        product_statment.product_type = product_form.product_type
    # if product_form.product_size is not None:
    #     product_statment.product_size = product_form.product_size
    # if product_form.product_stock is not None:
    #     product_statment.product_stock = product_form.product_stock
    if product_form.product_price is not None:
        product_statment.product_price = product_form.product_price
    if product_form.is_available is not None:
        product_statment.is_available = product_form.is_available    
    if product_form.product_description is not None:
        product_statment.product_description = product_form.product_description   
    if product_form.advance_payment_percetage is not None:
        product_statment.advance_payment_percetage = product_form.advance_payment_percetage 
    
    # Add the updated product instance to the session
    session.add(product_statment)
    
    # Commit the transaction to save changes to the database
    session.commit()
    
    # Refresh the session to get the updated product instance
    session.refresh(product_statment)
    
    # Return the updated product instance
    return product_statment


# ### ============================================================================================================= ###

def delete_product_from_db(product_id: int, session: DB_SESSION):
    product = session.get(Product, product_id)
    if not product:
        HTTPException(status_code=400, detail="Product not found")

    session.delete(product)
    session.commit()
    return f"Product ID: {product_id} has been successfully deleted. "

# ### ============================================================================================================= ###
# # ### ============================================================================================================= ###


# def search_product_by_name(name: str, session: Session) -> List[Product]:
#     products = session.exec(
#         select(Product).where(Product.product_name.ilike(f"%{name}%"))
#     ).all()

#     if not products:
#         raise HTTPException(status_code=404, detail="No products found with this name.")
    
#     return products

# # ### ============================================================================================================= ###

# def search_products_by_type(product_type: str, session: DB_SESSION) -> List[Product]:
#     products = session.exec(
#         select(Product).where(Product.product_type.ilike(f"%{product_type}%"))
#     ).all()

#     if not products:
#         raise HTTPException(status_code=404, detail="No products found with this type.")
#     return products

# # ### ============================================================================================================= ###

# def get_limited_products(limit: int, session: DB_SESSION):
#     products = session.exec(select(Product).limit(limit)).all()
#     return products

# # ### ============================================================================================================= ###

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

# # ### ============================================================================================================= ###
