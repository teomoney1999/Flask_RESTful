from db import db 
from models.store import StoreModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", 
        required=True,
        help="Store is required name"
    )

    @jwt_required
    def get(self, name): 
        store = StoreModel.find_by_name(name)
        if store: 
            return store.json(), 200
        return {"error_message": f"A store name {name} is not found"}, 404

    @jwt_required
    def post(self, name): 
        if StoreModel.find_by_name(name): 
            return {"error_message": f"The store name {name} is already exist"}, 404
        
        store = StoreModel(name)
        try: 
            store.save_to_db() 
        except: 
            return {"error_message": f"The store name {name} can not be created"}, 500
        
        return store.json(), 201

    @jwt_required
    def delete(self, name): 
        store = StoreModel.find_by_name(name)
        if store:
            try: 
                store.delete_from_db()
                return {"message": f"Deleted {name} successfully"}, 200
            except: 
                return {"error_message": f"The store name {name} can not be deleted"}, 500

        return {"error_message": f"A store name {name} is not exist"}, 404

    # def put(self, name): 
    #     store = StoreModel.find_by_name(name)
    #     if store:
    #         # update a exist store 
    #         store.save
    #     else: 
    #         # create a new store
    #         pass
    #     pass

class StoreList(Resource): 
    @jwt_required
    def get(self): 
        return { "result": list(store.json() for store in StoreModel.query.all()) }, 200