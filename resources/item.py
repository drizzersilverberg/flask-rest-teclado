from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = 'An error occured inserting the item.'
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

_item_parser = reqparse.RequestParser()
_item_parser.add_argument('name',
                          type=str,
                          required=True,
                          help=BLANK_ERROR.format('name')
                          )
_item_parser.add_argument('price',
                          type=float,
                          required=True,
                          help=BLANK_ERROR.format('price')
                          )
_item_parser.add_argument('store_id',
                          type=int,
                          required=True,
                          help=BLANK_ERROR.format('store_id')
                          )


class Item(Resource):
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404

    @jwt_required
    def delete(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': ITEM_DELETED}

    def put(self, name: str):
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
        return {
            'items': [item.json() for item in ItemModel.find_all()]
        }, 200

    def post(self):
        data = _item_parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': NAME_ALREADY_EXISTS.format(data['name'])}, 400

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return item.json(), 201
