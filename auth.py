# user_service - auth.py

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from app.models.user_model import User, UserAuth
from app.settings import ALGORITHM, SECRET_KEY

# ============================================================================================================================

# CryptContext class, which is used for securely hashing and verifying passwords
# bcrypt algorithm is commonly used for password hashing
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")   # instance of the CryptContext class

# ============================================================================================================================

# token is provided on base of user data and expiry_time
# dynamic function to generate either access or refresh token, only change expiry_time 
# function generates a JWT (JSON Web Token) based on user data and an expiration time.

def generateToken(user: User, expires_delta: timedelta) -> str:
    """
    Generate a token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated token.
    """

    # Calculate expiry time
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "user_name": user.user_name,
        "user_email": user.user_email,
        "exp": expire
    }
    headers = {
        "iss": user.kid,
        "kid": user.kid
    }

    # Encode token with user data and secret key
    token = jwt.encode(payload, SECRET_KEY,
                       algorithm=ALGORITHM, headers=headers)
    return token

### ============================================================================================================= ###

def passwordIntoHash(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    hash_password = pwd_context.hash(password)
    return hash_password

### ============================================================================================================= ###

def verifyPassword(plainText: str, hashedPassword: str) -> bool:
    """
    Verifies if the provided plaintext password matches the hashed password.

    Args:
        plainText (str): The plaintext password.
        hashedPassword (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # Print the plaintext and hashed passwords for debugging
    print(plainText, hashedPassword)

    # Verify if the plaintext password matches the hashed password
    isPasswordCorrect = pwd_context.verify(plainText, hash=hashedPassword)

    # Print the result of password verification for debugging
    print(isPasswordCorrect)

    return isPasswordCorrect

      
# ============================================================================================================================

# def generateToken(form_user: UserAuth , expires_delta: timedelta) -> str:

#     # Calculate expiry time     
#     expire = datetime.now(timezone.utc) + expires_delta
#     # expire = datetime.utcnow() + expires_delta
#     expire_timestimp = int(expire.timestamp())
#     user = {
#         "user_email": form_user.user_email,
#         "exp": expire_timestimp
#     }
#     encoded_jwt = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt




# def decode_access_token1(access_token: str):
#     decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
#     return decoded_jwt
##pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

