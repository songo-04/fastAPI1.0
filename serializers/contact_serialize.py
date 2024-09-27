def Decode_Contact(data)-> dict:
    return {
        "_id":str(data['_id']),
        "contact_name":data['contact_name'],
        "contact_number":data['contact_number']
    }
def Decode_Contact_List(x)-> list:
    return [Decode_Contact(data) for data in x]