from typing import Optional
from sqlmodel import Field, SQLModel

### ============================================================================================================= ###

class CategoryModel(SQLModel):
    category_name: str    

class Category(CategoryModel, table=True):
    category_id: Optional[int] = Field(None, primary_key=True)

### ============================================================================================================= ###

class SizeModel(SQLModel):
    size: str  # (Large, Medium, Small)    

class Size(SizeModel, table=True):
    size_id: Optional[int] = Field(default=None, primary_key=True)


### ============================================================================================================= ###
