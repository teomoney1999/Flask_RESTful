from models.user import UserModel

# User for compare string 
from werkzeug.security import safe_str_cmp


def authenticate(username, password): 
    user = UserModel.find_by_username(username)
    if user is not None and safe_str_cmp(password, user.password): 
        return user
    return {"error_message": f"Username {username} or password is not correct"}


def identity(payload):
    user_id = payload["identity"] 
    return UserModel.find_by_id(user_id)