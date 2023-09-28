from fastapi import APIRouter, Request, Response, status, Depends, HTTPException, Query
from app.models.user import User
from app.serializers.user import UserSerializer
from app.schemas.user import userEntity, usersEntity
from app.db.base import DataBase
from .utils import hash_password, verify_password
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

db_url = os.environ.get('DB_URL')
db_name = os.environ.get('DB_NAME')
table_name = os.environ.get('TABLE_NAME')

user = APIRouter()
db = DataBase(db_url=db_url)


@user.get("/users/")
async def get_users():
    
    """api covers below features
    1. user search (single/multiple)
    2. featch all users
    """
    
    filter = {}
    # func primarly written to get all users or specific user based on filter
    # if filter is None:
    return usersEntity(db.query(db_name=db_name, table_name=table_name, bulk=True))


    # # 2nd condition (if user choose filter)
    # db.query(db_name=db_name, table_name=table_name, bulk=True, filter=filter)
    
    
@user.post("/register")
async def register_user(user_data: User):
    "api covers user registeration based on required details"
    
    user_dict = UserSerializer.from_request(user_data)
    
    user = db.query(db_name=db_name, table_name=table_name, filter={"_id"})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
        
    # # Compare password and passwordConfirm
    # if payload.password != payload.passwordConfirm:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    # #  Hash the password
    # payload.password = hash_password(payload.password)
    

    db.upload(db_name=db_name, table_name=table_name, data=dict(user))
    
    return {"status": "success"}

@user.get("/login")
async def login(user: User):
    "api covers user login part using jwt"
    
    db.query(db_name=db_name, table_name=table_name, filter={})
    
    