import sqlite3
from models.user import UserModel 
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


_user_parser = reqparse.RequestParser() 
_user_parser.add_argument("username", 
        type=str, 
        required=True, 
        help="Username can not be blank"
    )
_user_parser.add_argument("password", 
        type=str, 
        required=True, 
        help="Password can not be blank"
    )
class UserRegister(Resource): 
    def post(self): 
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data.get("username")) is not None: 
            return {"error_message": f"A user with name {data.get('username')} is already exist"}, 400

        try: 
            user = UserModel(**data)
            user.save_to_db()
        except: 
            return {"message": "User created unsuccessfully"}, 500
        
        return {"message": "User created successfully"}, 201

class User(Resource): 
    @classmethod
    def get(cls, user_id): 
        user = UserModel.find_by_id(user_id)
        if not user: 
            return {"message": "User not found"}, 404
        return user.json()
        

    @classmethod
    def delete(cls, user_id): 
        user = UserModel.find_by_id(user_id)
        if not user: 
            return {"message": "User not found"}, 404
        
        try: 
            user.delete_from_db()
        except: 
            return {"message": "Can not delete user"}, 500
            
        return {"message": "Delete successfully"}, 404
    

class UserLogin(Resource):
    @classmethod
    def post(cls): 
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database 
        user = UserModel.find_by_username(data.get("username"))

        # This is what the authenticate() used to do
        if user and safe_str_cmp(user.password, data.get("password")):
            # identity= is what identity function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        
        return {"message": "Invalid credentials"}, 401
