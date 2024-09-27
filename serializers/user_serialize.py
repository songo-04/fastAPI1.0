def DecodeUser(data)->dict:
    return {
        "user_name":data['user_name'],
        "user_email":data['user_email'],
        "user_password":data['user_password'],
        "_id":str(data['_id'])
    }

def DecodeUsers(x)->list:
    return [DecodeUser(data) for data in x]