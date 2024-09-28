from fastapi import APIRouter,Depends,Request,Response,HTTPException,status
from auth.isAuthenticate import isAuthenticate
from bson import ObjectId
from models.task_model import TaskModel,TaskModelUpdate
from datetime import datetime
from config.config import task_collection
from serializers.task_serialize import Decode_task,Decode_tasks
from utils.is_exist import is_exist
from utils.is_authorize import is_authorize
task_route = APIRouter(
    prefix='/task'
)

#create task
@task_route.post('/')
async def create_task(data: TaskModel,is_auth: dict=Depends(isAuthenticate)):
    userId=is_auth['userId']
    time_now=datetime.now()
    new_task = TaskModel(task_name=data.task_name,task_begin=str(time_now),userId=userId)
    new_task=dict(new_task)
    task_collection.insert_one(new_task)
    return {
        "status":status.HTTP_201_CREATED,
    }
    
#get all task
@task_route.get('/')
async def get_all_task(is_auth:dict=Depends(isAuthenticate)):
    userId=is_auth['userId']
    tasks = task_collection.find({"userId":userId})
    is_exist(tasks)
    tasks = Decode_tasks(tasks)
    if(len(tasks)==0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='tasks not found'
        )
    return tasks

# #get one task
@task_route.get('/{_id}')
async def get_one_task(_id:str,is_auth:dict=Depends(isAuthenticate)):
    userId = is_auth['userId']
    task = task_collection.find_one({'_id':ObjectId(_id)})
    is_exist(task)
    is_authorize(current_user_id=task['userId'],token_id=userId)
    task = Decode_task(task)
    return task

# #put one task
@task_route.patch('/{_id}')
async def update_one_task(_id:str,data:TaskModelUpdate,is_auth: dict=Depends(isAuthenticate)):
    userId=is_auth['userId']
    is_task_exist = task_collection.find_one({"_id":ObjectId(_id)})
    is_exist(is_task_exist)
    is_authorize(current_user_id=is_task_exist['userId'],token_id=userId)
    req = dict(data.model_dump(exclude_unset=True))
    task_collection.find_one_and_update({"_id":ObjectId(_id)},{"$set":req})
    return {
        "message":"task updated",
        "status":status.HTTP_202_ACCEPTED
    }
    
# #delete one task
@task_route.delete('/{_id}')
async def delete_one_task(_id: str,is_auth: dict=Depends(isAuthenticate)):
    userId = is_auth['userId']
    is_task_exist = task_collection.find_one({'_id':ObjectId(_id)})
    is_exist(is_task_exist)
    is_authorize(current_user_id=is_task_exist['userId'],token_id=userId)
    task_collection.find_one_and_delete({'_id':ObjectId(_id)})
    return {
        "message":"task deleted",
        "status":status.HTTP_202_ACCEPTED
    }