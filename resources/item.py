from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel

_item_parser = reqparse.RequestParser()
_item_parser.add_argument('name',
                          type=str,
                          required=True,
                          help="This field cannot be left blank."
                          )
_item_parser.add_argument('price',
                          type=float,
                          required=True,
                          help="This field cannot be left blank."
                          )
_item_parser.add_argument('store_id',
                          type=int,
                          required=True,
                          help="Every item needs a store id."
                          )


class Item(Resource):
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = _item_parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item = ItemModel(**data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

    def post(self):
        data = _item_parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': "An item with name '{}' already exists".format(data['name'])}, 400

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return item.json(), 201
