from fastapi import Request,HTTPException, status
from dotenv import load_dotenv
import os
import jwt
load_dotenv()

async def isAuthenticate(request:Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token missing",
            )
        
        user_info = jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
        user_name = user_info.get("sub")
        if user_name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid token'
            )
        print(user_info)
        return user_info
    except jwt.PyJWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid token'
            )