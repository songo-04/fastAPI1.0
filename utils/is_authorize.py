from fastapi import HTTPException,status

def is_authorize(current_user_id: str,token_id: str):
    if(current_user_id != token_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail='access denied!!'
        )