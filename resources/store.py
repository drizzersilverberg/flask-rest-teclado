from flask_restful import Resource, reqparse
from models.store import StoreModel

BLANK_ERROR = "'{}' cannot be left blank."
NAME_ALREADY_EXISTS = "A store with name '{}' already exists"
STORE_NOT_FOUND = 'Store not found'
STORE_DELETED = 'Store deleted'
INSERT_ERROR = 'An error occurred while creating the store'


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help=BLANK_ERROR.format('name')
                        )

    def get(self, id: int):
        store = StoreModel.find_by_id(id)
        if store:
            return store.json()
        return {'message': STORE_NOT_FOUND}, 404

    def delete(self, id: int):
        store = StoreModel.find_by_id(id)
        if store:
            store.delete_from_db()
        return {'message': STORE_DELETED}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}

    def post(self):
        data = Store.parser.parse_args()

        if StoreModel.find_by_id(data['name']):
            return {'message': NAME_ALREADY_EXISTS.format(data['name'])}, 400
        store = StoreModel(data['name'])
        try:
            store.save_to_db()
        except:
            return {'message': INSERT_ERROR}, 500

        store = StoreModel.find_by_id(store.id)

        return store.json(), 201
