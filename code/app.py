from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from pkg_resources import require
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "mont-hin-gha-and-pizza" 
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            type = float,
            required = True,
            help = "This Field cannot be blank or other type than float."
    )
    # data = parser.parse_args()

    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x : x ['name'] == name, items), None )
        return { "item" : item }, 200 if item else 404
        # for item in items:
        #     if (item['name'] == name):
        #         return item
        # return { 'items you are finding ' : None }, 404

    # @jwt_required()
    def post(self, name):

        item = next(filter(lambda x : x ['name'] == name, items), None )
        if item:
            return { "message" : "An item with this name already exists."}, 400

        data = Item.parser.parse_args()

        # data = request.get_json()
        print(data)
        item = { 'name' : name, 'price' : data['price'] }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return { 'message' : 'item deleted'}

    def put(self,name):

        data = Item.parser.parse_args()

        item = next(filter(lambda x : x ['name'] == name, items), None )
        if item is None:
            item = { "name" : name, "price" : data['price']}
            items.append(item)
            # return { "message" : 'item not found'}
        else:
            item.update(data)
        return item

class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return { 'items' : items }

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
#http://127.0.0:5000/

if __name__ == "__main__":
    app.run(debug=True, port = 5000)