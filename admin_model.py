# # user_service - admin_model.py

import uuid
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

### ============================================================================================================= ###

class AdminBase(SQLModel):
    admin_email: EmailStr
    admin_password: str
  
### ============================================================================================================= ###

class AdminLoginForm(AdminBase):
    admin_secret: str | None

### ============================================================================================================= ###

class AdminCreateModel(AdminLoginForm):
    admin_name: str
   
### ============================================================================================================= ###


class Admin(AdminBase, table=True):
    admin_id: int | None = Field(default=None, primary_key=True)  # Use default=None
    admin_name: str
    admin_kid: str = Field(default_factory=lambda: uuid.uuid4().hex)    

### ============================================================================================================= ###

# class Token(SQLModel):
#     access_token: str
#     token_type: str
  

# class Admin(AdminBase, table=True):
#     admin_id: int | None = Field(int, primary_key=True) # This is incorrect
#     admin_name: str
#     admin_kid: str = Field(default=lambda: uuid.uuid4().hex)

