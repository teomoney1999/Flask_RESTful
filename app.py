import os 
from flask import Flask, jsonify
from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin

from resources.item import Item, ItemList
from resources.store import Store, StoreList

from datetime import timedelta

app = Flask(__name__) 

app.secret_key = "teomoney"

api = Api(app)

# SQLAlchemy Configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
# "postgres://bhbshkidakkphb:d24fb10fa3c4e44123ebcf7b24b00cb38f8cdbb0658c834c94f6ba27b9744f64@ec2-3-213-85-90.compute-1.amazonaws.com:5432/d5olmhl87fmspp"
app.config['PROPAGATE_EXCEPTIONS'] = True


# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWTManager(app)

# Whenever we create a new access token, this function gonna decided 
# should we add any extra data to that JWT as well
@jwt.user_claim_loader
def add_claims_to_jwt(identity):
    if identity == 1: 
        return {"is_admin": True}
    return {"is_admin": False}

api.add_resource(StoreList, '/stores/')
api.add_resource(ItemList, '/items/')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == "__main__":
    from db import db 
    db.init_app(app)
    app.run(debug=True)