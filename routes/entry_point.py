from fastapi import APIRouter

entry_root = APIRouter()

#endPoint
@entry_root.get("/")
def apiRunning():
    res={
        "status":"ok",
        "message":"api is running"
    }
    return res