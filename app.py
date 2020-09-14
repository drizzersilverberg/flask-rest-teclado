from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dendi'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
