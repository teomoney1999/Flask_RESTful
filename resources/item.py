from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument("price",
        type=float, 
        required=True, 
        help="This field can not be left blank"
    )
    parser.add_argument("store_id",
        type=int, 
        required=True, 
        help="Every item need a store_id"
    )

    @jwt_required()
    def get(self, name):
        print("===Name get", name)
        result = ItemModel.find_by_name(name)
        if result: 
            return {"result": [result.json()]}, 200
        return {"message": f"An item with name {name} does not exist"}, 404

    @jwt_required()
    def post(self, name): 
        # if next(filter(lambda i: i == i.get("name"), items), None) is not None:
        #     return {"error_message": f"An item with name '{name}' is already exist"}, 400
        if ItemModel.find_by_name(name): 
            return {"error_message": f"An item with name '{name}' is already exist"}, 404
 
        data = Item.parser.parse_args()
        posted_item = ItemModel(name, **data)

        try: 
            posted_item.save_to_db()
        except: 
            return {"error_message": "Can not insert data into database. Try again later!"}, 500

        return posted_item.json(), 201

    @jwt_required()
    def delete(self, name): 
        item = ItemModel.find_by_name(name)
        if item: 
            item.delete_from_db()
            return {"message": "deleted successfully"}

        return {"error_message": f"An item name {name} does not exist"}
    
    @jwt_required()
    def put(self, name): 
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item: 
            try: 
                item.price = data.get("price")
            except: 
                return {"error_message": "Can not update data into database. Try again later!"}, 500
        else: 
            try:
                item = ItemModel(name, **data)   
            except: 
                return {"error_message": "Can not insert data into database. Try again later!"}, 500
        
        item.save_to_db()

        return {"result": item.json()}, 200


class ItemList(Resource): 
    @jwt_required()
    def get(self): 
        # return { "result": list(item.json() for item in ItemModel.query.filter().all()) }, 200
        return { "result": list(map( lambda item: item.json(), ItemModel.query.all() )) }, 200