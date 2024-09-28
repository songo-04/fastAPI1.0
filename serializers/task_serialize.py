def Decode_task(data)->dict:
    return{
        "task_name":data['task_name'],
        "task_begin":data['task_begin'],
        "_id":str(data['_id'])
    }
    
def Decode_tasks(x)-> list:
    return [Decode_task(data) for data in x]