import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

ALGORITHM  = 'HS256'

ACCESS_TOKEN_EXPIRE = 30 

