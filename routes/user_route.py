from fastapi import APIRouter ,Depends,Response,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from models.user_model import UserModel,UserModelUpdated,UserInDB
from config.config import user_collection
from serializers.user_serialize import DecodeUsers,DecodeUser
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
from auth.isAuthenticate import isAuthenticate

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#import datetime
user_root = APIRouter(
    prefix="/user"
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Creation de token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=15)
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


#create user
@user_root.post("/register")
async def create_user(doc:UserModel):
   
    new_user = UserModel(user_name=doc.user_name,user_email=doc.user_email,user_password=get_password_hash(doc.user_password))
    new_user=dict(new_user)
    user_collection.insert_one(new_user)
    return {
        "message":"okay"
    }

@user_root.post("/login")
async def login(form_data:UserModel,response:Response):
    is_user_exist = user_collection.find_one({"user_name":form_data.user_name})
    if not is_user_exist or not verify_password(form_data.user_password,is_user_exist['user_password']):
        return {
            "message":"non register"
        }
    access_token_expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token  = create_access_token(data={"sub":is_user_exist['user_name']},expires_delta=access_token_expire)
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return {
        "message":"login successfully"
    }

@user_root.get("/me")
async def current_user(request:Request,is_auth:dict=Depends(isAuthenticate)):
    user_name = is_auth['sub']
    me = user_collection.find_one({"user_name":user_name})
    return DecodeUser(me)

@user_root.get("/")
async def get_all_user(is_auth:dict=Depends(isAuthenticate)):
    res = user_collection.find()
    decoded_users = DecodeUsers(res)
    return {
            "status":200,
            "data":decoded_users
        }

@user_root.get("/{_id}")
async def get_user_by_id(_id:str):
    res = user_collection.find_one({"_id":ObjectId(_id)})
    if(res is None):
        return {"message":"user is found"}
    decoded_user = DecodeUser(res)
    return {
        "res":200,
        "user":decoded_user
    }

@user_root.patch("/{_id}")
async def update_user(_id:str,data:UserModelUpdated):
    is_user_exist = user_collection.find_one({"_id":ObjectId(_id)})
    if(is_user_exist is None):
        return {"message":"user is found"}
    req = dict(data.model_dump(exclude_unset=True))
    user_collection.find_one_and_update({"_id":ObjectId(_id)},{"$set":req})
    return {
        "message":"user id {_id} updated"
    }

@user_root.delete("/{_id}")
async def delete_user(_id:str):
    is_user_exist = user_collection.find_one({"_id":ObjectId(_id)})
    if(is_user_exist is None):
        return {"message":"user is found"}
    user_collection.find_one_and_delete({"_id":ObjectId(_id)})
    return {
        "message":"{_id} is deleted successfully"
    }
