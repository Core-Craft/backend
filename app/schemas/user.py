def userEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":str(item["name"]),
        "email":str(item["email"])
    }
    
    
def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]