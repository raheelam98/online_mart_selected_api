import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class Admin(SQLModel, table=True):
    admin_id: int | None = Field(int, primary_key=True)
    admin_name: str
    admin_email: str
    admin_password: str
    admin_kid: str = Field(default=lambda: uuid.uuid4().hex)

### ============================================================================================================= ###

class AdminBase(SQLModel):
    admin_email: EmailStr
    admin_password: str
    admin_name: str
  
### ============================================================================================================= ###

class AdminLoginForm(AdminBase):
    admin_secret: str | None



### ============================================================================================================= ###

# class AdminCreateModel(AdminLoginForm):
#     admin_name: str
   
## ============================================================================================================= ###


# class Admin(AdminBase, table=True):
#     admin_id: int | None = Field(default=None, primary_key=True)  # Use default=None
#     admin_name: str
#     admin_kid: str = Field(default_factory=lambda: uuid.uuid4().hex)    


## ============================================================================================================= ###


