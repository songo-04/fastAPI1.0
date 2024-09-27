
from fastapi import APIRouter
from config.config import contact_collection
from models.contact_model import ContactModel,ContactModelUpdate
from serializers.contact_serialize import Decode_Contact,Decode_Contact_List
from bson import ObjectId
contact_route = APIRouter(
    prefix="/contact"
)

@contact_route.post("/")
async def create_contact(data: ContactModel):
    data = dict(data)
    contact_collection.insert_one(data)
    return {
            "status":200,
            "res":"contact created successfully"
        }

@contact_route.get("/")
async def get_all_contact():
    res =contact_collection.find()
    if(res is None):
        return {
            "message":"list is empty"
        } 
    contact_list = Decode_Contact_List(res)
    return contact_list

@contact_route.get("/{_id}")
async def get_one_contact(_id:str):
    res = contact_collection.find_one({"_id":ObjectId(_id)})
    if(res is None):
        return {
            "message":"contact {_id} is not found"
        }
    contact = Decode_Contact(res)
    return contact

@contact_route.patch("/{_id}")
async def update_contact(_id:str,data:ContactModelUpdate):
    is_contact_exist = contact_collection.find_one({"_id":ObjectId(_id)})
    if(is_contact_exist is None):
        return {
            "message":"contact is already deleted or missing"
        }
    req = dict(data.model_dump(exclude_unset=True))
    contact_collection.find_one_and_update({"_id":ObjectId(_id)},{"$set":req})
    return {
        "message":"user id {_id} updated"
    }

@contact_route.delete("/{_id}")
async def delete_one_contact(_id:str):
    is_contact_exist = contact_collection.find_one({"_id":ObjectId(_id)})
    if(is_contact_exist is None):
        return {
            "message":'contact is not found or already deleted'
        }
    contact_collection.find_one_and_delete({"_id":ObjectId(_id)})
    return {
        "status":200,
        "message":"contact {_id} is successfully deleted"
    }