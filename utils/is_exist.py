from fastapi import HTTPException,status


def is_exist(data):
    if(data is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=format('${data} not found')
        )