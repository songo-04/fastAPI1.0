from pydantic import BaseModel

class ContactModel(BaseModel):
    contact_name:str
    contact_number:float

class ContactModelUpdate(BaseModel):
    contact_name:str = None
    contact_number:str = None 
