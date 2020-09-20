from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, Items
from models.store import StoreModel
from models.item import ItemModel
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dendi'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if (identity == 1):
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Store, '/stores/<int:id>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
