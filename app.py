from flask import Flask
from flask_restful import Resource, Api, reqparse
from manage import User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

api = Api(app)


class UserView(Resource):

    def get(self):
        pass

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("password")
        parser.add_argument("email")
        parser.add_argument("mobile")
        parser.add_argument("type")
        args = parser.parse_args()
        try:
            user = User(password=args['password'], email=args['email'], mobile=args['mobile'], user_type=args['type'])
            db.session.add(user)
            db.session.commit()
            result = {'user': user.email}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass

    def delete(self):
        pass


class CountryView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class StateView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class PlaceView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class RestaurantCategoryView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class TableCategoryView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class TableView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class RestaurantView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class MenuView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class OrderView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


api.add_resource(UserView, '/user/')
api.add_resource(CountryView, '/country/')
api.add_resource(StateView, '/state/')
api.add_resource(PlaceView, '/place/')
api.add_resource(RestaurantCategoryView, '/restaurant-categories/')
api.add_resource(TableCategoryView, '/table-categories/')
api.add_resource(TableView, '/table/')
api.add_resource(RestaurantView, '/restaurant/')
api.add_resource(MenuView, '/menu-items/')
api.add_resource(OrderView, '/book/')

if __name__ == '__main__':
    app.run(debug=True)