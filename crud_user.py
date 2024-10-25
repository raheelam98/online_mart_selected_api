# user_service - crud_user.py

from fastapi import  HTTPException
from sqlmodel import Session, select
import json

from app.utils.auth import passwordIntoHash, verifyPassword
from app.db.db_connector import  DB_SESSION
from app.models.user_model import User, UserModel, UserUpdateModel, UserAuth

from app.kafka.kafka_producer import KAFKA_PRODUCER
from app.controllers.auth_user import user_login
from app.settings import NOTIFICATION_TOPIC

### ============================================================================================================= ###

def get_users_from_db(session: DB_SESSION):

    users = session.exec(select(User)).all() 
    if not users:
        HTTPException(status_code=400, detail="User not found")
    #print('get user fun  ....' )    
    return users 

### ============================================================================================================= ###

def get_user_by_id(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if user is None:
        HTTPException(status_code=400, detail="User not found")
    return user

### ============================================================================================================= ###

async def create_user_with_kafka(user_form: UserModel, session: DB_SESSION, producer: KAFKA_PRODUCER):

    users = session.exec(select(User))
    user_email: str = user_form.user_email
    user_password: str = user_form.user_password

    for user in users:
        password_exist = verifyPassword(user_password, user.user_password)
        if user.user_email == user_email and password_exist:
            raise HTTPException(
                status_code=404, detail="email and password already exist!")
        elif user.user_email == user_email:
            raise HTTPException(
                status_code=404, detail="This email already exist!")
        elif password_exist:
            raise HTTPException(
                status_code=404, detail="This password already exist!")

    user = await add_user_in_db_with_kafka(user_form, session)

    # kong_func(user.user_name, user.kid, secret_key=None)
    
    user_details = {
        "user_email": user_email,
        "user_password": user_password
    }
    ##Login the newly registered user and return the data

    token_data = user_login(user_details=UserAuth(
        **user_details), session=session)
    print("data from login", token_data)

    message = {
        "email": user_email,
        "notification_type": "user_notification"
    }

    ## TODO: Produce message to notification topic to welcome user through email
    await producer.send_and_wait(value=json.dumps(message).encode("utf-8"), topic=NOTIFICATION_TOPIC)
    return token_data


### ============================================================================================================= ###

async def create_user_with_kafka33(user_form: UserModel, session: DB_SESSION, producer: KAFKA_PRODUCER):
    users = session.exec(select(User))
    user_email: str = user_form.user_email
    user_password: str = user_form.user_password

    for user in users:
        password_exist = verifyPassword(user_password, user.user_password)
        if user.user_email == user_email and password_exist:
            raise HTTPException(
                status_code=404, detail="email and password already exist!")
        elif user.user_email == user_email:
            raise HTTPException(
                status_code=404, detail="This email already exist!")
        elif password_exist:
            raise HTTPException(
                status_code=404, detail="This password already exist!")

    # Assuming add_user_in_db_with_kafka is a coroutine function that adds the user to the database
    user = await add_user_in_db_with_kafka(user_form, session)

    user_details = {
        "user_email": user_email,
        "user_password": user_password
    }

    # Login the newly registered user and return the data
    token_data = user_login(user_details=UserAuth(
        **user_details), session=session)
    
    print("data from login", token_data)

    message = {
        "email": user_email,
        "notification_type": "user_detail"
    }

    # Produce message to notification topic to welcome user through email
    await producer.send_and_wait(value=json.dumps(message).encode("utf-8"), topic=NOTIFICATION_TOPIC)
    return token_data


### ============================================================================================================= ###

async def create_user_with_kafka22(user_form: UserModel, session: DB_SESSION, producer: KAFKA_PRODUCER):

    users = session.exec(select(User))
    user_email: str = user_form.user_email
    user_password: str = user_form.user_password
    user

    for user in users:
        password_exist = verifyPassword(user_password, user.user_password)
        if user.user_email == user_email and password_exist:
            raise HTTPException(
                status_code=404, detail="email and password already exist!")
        elif user.user_email == user_email:
            raise HTTPException(
                status_code=404, detail="This email already exist!")
        elif password_exist:
            raise HTTPException(
                status_code=404, detail="This password already exist!")

    user = await add_user_in_db_with_kafka(user_form, session)

    # kong_func(user.user_name, user.kid, secret_key=None)
    
    user_details = {
        "user_email": user_email,
        "user_password": user_password
    }

    ##Login the newly registered user and return the data

    token_data = user_login(user_details=UserAuth(
        **user_details), session=session)
    
    print("data from login", token_data)

    message = {
        "email": user_email,
        
        "notification_type": "user_detail"
    }

    ## TODO: Produce message to notification topic to welcome user through email
    await producer.send_and_wait(value=json.dumps(message).encode("utf-8"), topic=NOTIFICATION_TOPIC)
    return token_data

### ============================================================================================================= ###

async def add_user_in_db_with_kafka(user_form: UserModel, session: Session):
    try:
        hashed_password = passwordIntoHash(user_form.user_password)
        user_form.user_password = hashed_password
        if not hashed_password:
            raise HTTPException(
                status_code=500, detail="Due to some issues, password has not convert into hashed format.")
        user = User(**user_form.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user

### ============================================================================================================= ###

def add_user_in_db(user_base: UserModel, session: Session):
  
    # Convert UserModel to User instance
    #user = User(**user_base.dict())
    user = User(**user_base.model_dump())
    user.user_password = passwordIntoHash(user_base.user_password)

    #print('add user fun 1 ....', user)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    # Add the user to the session
    session.add(user)
    # Commit the session to save the user to the database
    session.commit()
    # Refresh the session to retrieve the new user data, including generated fields like user_id
    session.refresh(user)
    #print('add user fun 2 ....', user)
    return user


### ============================================================================================================= ###

def update_user_in_db(selected_id: int, user_base: UserUpdateModel, session: DB_SESSION):
    
    print('update user id fun  ....' )

    # Construct a query to select the user with the specified user_id
    user_query = select(User).where(User.user_id == selected_id)
    
    # Execute the query and get the first result
    user_statment = session.exec(user_query).first()
    
    # If no user is found with the given ID, raise a 404 HTTPException
    if not user_statment:
        raise HTTPException(status_code=404, detail="User is unavailable")
    
    # Update the fields of the user with the values from the user_base object
    user_statment.user_name = user_base.user_name
    user_statment.user_email = user_base.user_email
    user_statment.user_password = passwordIntoHash(user_base.user_password)
    user_statment.address = user_base.address
    user_statment.country = user_base.country
    user_statment.phone_number = user_base.phone_number
    
    # Add the updated user instance to the session
    session.add(user_statment)
    
    # Commit the transaction to save changes to the database
    session.commit()
    
    # Refresh the session to get the updated user instance
    session.refresh(user_statment)

    print('update user fun  ....' , user_statment)
    
    # Return the updated user instance
    return user_statment


### ============================================================================================================= ###

def delete_user_from_db(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        HTTPException(status_code=400, detail="User not found")

    session.delete(user)
    session.commit()
    return f"User ID: {user_id} has been successfully deleted. "


### ============================================================================================================= ###


