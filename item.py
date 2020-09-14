import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank."
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank."
                        )

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

        return None

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred updating the item.'}, 500

        return updated_item


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank."
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank."
                        )

    def get(self):
        return {'items': []}, 200

    def post(self):
        data = Item.parser.parse_args()

        if Item.find_by_name(data['name']):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        item = {'name': data['name'], 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return item, 201
