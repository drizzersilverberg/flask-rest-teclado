from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank."
                        )

    def get(self, id):
        store = StoreModel.find_by_id(id)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def delete(self, id):
        store = StoreModel.find_by_id(id)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}

    def post(self):
        data = Store.parser.parse_args()

        if StoreModel.find_by_id(data['name']):
            return {'message': "A store with name '{}' already exists".format(data['name'])}, 400
        store = StoreModel(data['name'])
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store'}, 500

        store = StoreModel.find_by_id(store.id)

        return store.json(), 201
