from fastapi import FastAPI , HTTPException, Depends
from typing import Annotated, List
from sqlalchemy import or_

from fastapi.security import OAuth2PasswordRequestForm
from datetime import  timedelta, datetime, timezone
from sqlmodel import select

from app.db.db_connector import create_db_and_tables,DB_SESSION
from app.utils.auth_admin import create_access_token, decode_access_token, oauth2_scheme

from app.models.auth_admin_model import Admin

from app.models.product_model import Product , ProductUpdateModel, ProductDetail
from app.controllers.crud_product import create_product_by_admin, get_product_from_db , add_product_in_db, update_product_in_db, delete_product_from_db
from app.controllers.operations import  search_product_by_name, get_limited_products, search_products_by_type, search_products_by_category, search_specific_size_products

from app.models.categories_model import Category, CategoryModel, Size, SizeModel
from app.controllers.crud_category import ( add_category_in_db, get_category_from_db, update_category_in_db
                                           , add_size_in_db, get_size_from_db, update_size_in_db )


### ============================================================================== ###

app = FastAPI(lifespan = create_db_and_tables)

# @app.get('/')
# def get_route():
#     return "product service"

### ============================================================================== ###

# @app.get('/api/product', response_model=list[Product])
# def get_product(session:DB_SESSION):
#       product_list = get_product_from_db(session)
#       if not product_list:
#         raise HTTPException(status_code=404, detail="Product Not Found in DB")
#       else:
#         return product_list  
    

### ============================================================================== ###

@app.post("/token/v1")
def login_v1(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], session: DB_SESSION):

    username = form_data.username
    password = form_data.password

    statement = select(Admin).where(
        (Admin.admin_name == username) and (Admin.admin_password == password)
    )
    
    user_in_db = session.exec(statement).one_or_none()
    
    print(f'user_in_db ... {user_in_db}')

    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(subject=user_in_db.admin_name, expires_delta=access_token_expires)
    
    print(f'access_token ... {access_token}')

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds()
    }

### ============================================================================== ###
### ============================================================================== ###

@app.post("/api/create_product_by_admin", response_model=Admin)
def add_product_by_admin(
    form_data: ProductDetail, 
    token: Annotated[str, Depends(oauth2_scheme)], 
    session: DB_SESSION
):
    # Decode the token (if needed)
    #decoded_token = decode_jwt(token)

    # Add the product using the function defined earlier
    product = create_product_by_admin(form_data, session)

    return product

### ============================================================================== ###

@app.get("/api/get_all_products_of_official_admin")
def get_all_product_with_dependency_injection(token:Annotated[str, Depends(oauth2_scheme)] , session: DB_SESSION):  
    print(f'dependency_injection token ... {token} ') 
    product_list = get_product_from_db(session)

    if not product_list:
        raise HTTPException(status_code=404, detail="User Not Found in DB")
    else:
        return product_list

### ============================================================================== ###

@app.get("/api/all_product/", response_model=List[Product])
def get_all_products(session: DB_SESSION):
    # Query the database to get all users
    statement = select(Product)
    product_in_db = session.exec(statement).all()

    # Return the list of users without passwords
    return product_in_db


### ============================================================================== ###

# # working on it 
# @app.get("/authorized_special_product")
# def get_special_item(token:Annotated[str, Depends(oauth2_scheme)]):
#     print(f'get_special_item... ')  
#     return {"speical": "product", "token": token}

### ============================================================================== ###

@app.post("/api/add_product_by_user", response_model=Product)
def add_product(new_product: ProductDetail, session: DB_SESSION ):
    # Call the function to add the data to the database
    created_product = add_product_in_db(new_product, session)
    if not created_product:
        raise HTTPException(status_code=404, detail="Can't Add Product")
    return created_product

### ============================================================================== ###

@app.put('/api/update_product/{id}', response_model=Product)
def update_product(id: int, product_detail: ProductUpdateModel, session: DB_SESSION):
    # Call the function to update the data to the database
    updated_product = update_product_in_db(id, product_detail, session)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Can't Find Product")
    return updated_product

### ============================================================================== ###

@app.delete("/api/delete_product", response_model=Product)
def delete_product(message: Annotated[str, Depends(delete_product_from_db)]):
    return message

### ============================================================================== ###

@app.get("/api/get_limited_products/", response_model=list[Product])
def get_limited_products(products: Annotated[list[Product], Depends(get_limited_products)]):
    if not products:
        raise HTTPException(
            status_code=404, detail="Try again, products has not fetched.")
    return products

### ============================================================================== ###

@app.get("/api/search_product_by_name/{product_name}", response_model=List[Product])
def search_product(name: str, session: DB_SESSION):
    return search_product_by_name(name, session)

### ============================================================================== ###

@app.get("/api/search_special_type_porducts/{product_type}", response_model=List[Product])
def search_product_type(product_type: str, session: DB_SESSION ):
    return search_products_by_type(product_type, session)

### ============================================================================== ###

@app.get('/api/get_all_categories', response_model=list[Category])
def get_category(session:DB_SESSION):
      category_list = get_category_from_db(session)
      if not category_list:
        raise HTTPException(status_code=404, detail="Not Found")
      else:
        return category_list   
      
### ============================================================================== ###
  
@app.post('/api/add_category', response_model=Category)
def create_category(category_form: CategoryModel, session: DB_SESSION):
    created_category = add_category_in_db(category_form, session)
    if not create_category:
        raise HTTPException(status_code=404, detail="Not Found")
    return created_category      

### ============================================================================== ###

@app.put('/api/update_category/{id}', response_model=Category)
def update_category(id: int, category_detail: CategoryModel, session: DB_SESSION):
    updated_category = update_category_in_db(id, category_detail, session)
    if not update_category:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_category

### ============================================================================== ###

@app.get("/api/search_specific_category_products/", response_model=List[Product])
def search_products_by_category(products: Annotated[List[Product], Depends(search_products_by_category)]):
    if not products:
        raise HTTPException(
            status_code=500, detail="Some things went wrong, while creating product.")
    return products

### ============================================================================== ###

@app.get('/api/size', response_model=list[Size])
def get_size(session:DB_SESSION):
      size_list = get_size_from_db(session)
      if not size_list:
        raise HTTPException(status_code=404, detail="Not Found")
      else:
        return size_list   
      
### ============================================================================== ###
  
@app.post('/api/add_size', response_model=Size)
def create_size(size_form: SizeModel, session: DB_SESSION):
    created_size = add_size_in_db(size_form, session)
    if not created_size:
        raise HTTPException(status_code=404, detail="Not Found")
    return created_size

### ============================================================================== ###

@app.put('/api/update_size/{id}', response_model=Size)
def update_size(id: int, size_detail: SizeModel, session:  DB_SESSION):
    updated_size = update_size_in_db(id, size_detail, session)
    if not updated_size:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_size

### ============================================================================== ###


@app.get("/api/get_specific_size_products/", response_model=List[Product])
def search_specific_size_products(product_items: Annotated[List[Product], Depends(search_specific_size_products)]):
    if not product_items:
        raise HTTPException(
            status_code=500, detail="Products of this size are not available")
    return product_items

### ============================================================================== ###              
