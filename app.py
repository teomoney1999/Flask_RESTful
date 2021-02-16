from flask import Flask, jsonify
from flask_restful import Api

from flask_jwt import JWT
from security import identity, authenticate

from resources.user import UserRegister

from resources.item import Item, ItemList
from resources.store import Store, StoreList

from datetime import timedelta

from db import db

app = Flask(__name__) 
# app.config['JWT_AUTH_HEADER_PREFIX'] = 'teomoney'
app.secret_key = "teomoney"

api = Api(app)

@app.before_first_request
def create_table():
    db.create_all() 

# Authentication endpoint
app.config["JWT_AUTH_URL_RULE"] = "/login"
# Token expiration time 
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
# Authentication key name 
app.config["JWT_AUTH_USERNAME_KEY"] = "username"

jwt = JWT(app, authenticate, identity)      # auth_endpoint: /auth

# SQLAlchemy Configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

@jwt.jwt_error_handler
def customized_error_handler(error): 
    return jsonify({
        "message": error.description, 
        "code": error.status_code
    }), error.status_code


@jwt.auth_response_handler
def customized_response_handler(access_token, identity): 
    return jsonify({
        "access_token": access_token.decode("utf-8"), 
        "user_id": identity.id
    })

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(StoreList, '/stores/')
api.add_resource(ItemList, '/items/')
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)