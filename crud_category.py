from fastapi import  HTTPException
from sqlmodel import Session, select

from app.db.db_connector import  DB_SESSION

from app.models.categories_model import Category, CategoryModel, Size, SizeModel


### ============================================================================================================= ###

def get_category_from_db(session: DB_SESSION):
    category = session.exec(select(Category)).all() 
    if not category:
        HTTPException(status_code=400, detail="Not found")
    return category 

### ============================================================================================================= ###


# Function to add a category to the database
def add_category_in_db(category_form: CategoryModel, session: Session):
    category = Category(category_name=category_form.category_name)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

### ============================================================================================================= ###


# Function to update a category in the database
def update_category_in_db(id: int, category_detail: CategoryModel, session: Session):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category Not Found")
    category.category_name = category_detail.category_name
    session.commit()
    session.refresh(category)
    return category

### ============================================================================================================= ###

def get_size_from_db(session: DB_SESSION):
    size = session.exec(select(Size)).all() 
    if not size:
        HTTPException(status_code=400, detail="Not found")
    return size 

### ============================================================================================================= ###


# Function to add a size to the database
def add_size_in_db(size_form: SizeModel, session: DB_SESSION):
    new_size = Size(size=size_form.size)
    session.add(new_size)
    session.commit()
    session.refresh(new_size)
    return new_size 

### ============================================================================================================= ###



# Function to update data in the database
def update_size_in_db(id: int, size_detail: SizeModel, session: DB_SESSION):
    size = session.get(Size, id)
    if not size:
        raise HTTPException(status_code=404, detail="Not Found")
    size.size = size_detail.size
    session.commit()
    session.refresh(size)
    return size

### ============================================================================================================= ###






