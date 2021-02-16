import sqlite3
from models.user import UserModel 
from flask_restful import Resource, reqparse


class UserRegister(Resource): 
    parser = reqparse.RequestParser() 
    parser.add_argument("username", 
        type=str, 
        required=True, 
        help="Username can not be blank"
    )
    parser.add_argument("password", 
        type=str, 
        required=True, 
        help="Password can not be blank"
    )
    
    def post(self): 
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data.get("username")) is not None: 
            return {"error_message": f"A user with name {data.get('username')} is already exist"}, 400

        try: 
            user = UserModel(**data)
            user.save_to_db()
        except: 
            return {"message": "User created unsuccessfully"}, 500
        
        return {"message": "User created successfully"}, 201