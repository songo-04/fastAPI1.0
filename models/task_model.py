from pydantic import BaseModel
import datetime
from bson import ObjectId
class TaskModel(BaseModel):
    task_name:str
    task_begin:str = None
    userId:str = None
    
    
class TaskModelUpdate(BaseModel):
    task_name:str=None
    task_begin:datetime.datetime=None