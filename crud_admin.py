# user_service - curd_admin.py

from fastapi import  HTTPException
from sqlmodel import Session, select
from app.utils.auth import passwordIntoHash
from app.db.db_connector import  DB_SESSION

from app.models.admin_model import Admin
from app.settings import ADMIN_SECRET_KEY
from app.models.admin_model import  Admin, AdminCreateModel

### ============================================================================================================= ###

def get_admin_from_db(session: DB_SESSION):
    admins = session.exec(select(Admin)).all() 
    if not admins:
        HTTPException(status_code=400, detail="Not found")   
    return admins

### ============================================================================================================= ###


# Function to add a user to the database
def add_admin_in_db(admin_form: AdminCreateModel, session:DB_SESSION):
    
    # Convert AdminCreateModel to admin instance
    admin = Admin(**admin_form.model_dump())

    if not (admin_form.admin_secret == ADMIN_SECRET_KEY):
        raise HTTPException(status_code=404, detail="Insert Admin Secreat Key")
    
    admin_exist = session.exec(select(Admin).where(
        Admin.admin_email == admin_form.admin_email)).one_or_none()
    
    if admin_exist:
        raise HTTPException(status_code=404, detail="Admin Already Exist")

    admin.admin_name = admin_form.admin_name
    admin.admin_email = admin_form.admin_email
    admin.admin_password = passwordIntoHash(admin_form.admin_password)
    #admin.admin_password = admin_form.admin_password
    
    print(f'Admin Detail {admin}')


    # if not admin:
    #     raise HTTPException(status_code=404, detail="Admin Not Found")
    
    # Add the user to the session
    session.add(admin)
    # Commit the session to save the user to the database
    session.commit()
    # Refresh the session to retrieve the new user data, including generated fields like user_id
    session.refresh(admin)
    # Return the created user

    print("admin  ", admin)

    return admin

### ============================================================================================================= ###
