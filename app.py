import datetime
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse
from models import User, Country, State, Place, RestaurantCategory, TableCategory, Table, Restaurant, MenuItem, Order
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

api = Api(app)


class UserView(Resource):

    def get(self):
        output = []
        users = User.query.all()
        for user in users:
            result = {}
            result['email'] = user.email
            result['mobile'] = user.mobile
            result['user_type'] = user.user_type.value
            output.append(result)
        return output

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
        output = []
        countries = Country.query.all()
        for country in countries:
            result = {}
            result['id'] = country.id
            result['code'] = country.code
            result['name'] = country.name
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("code")
        parser.add_argument("name")
        args = parser.parse_args()
        try:
            country = Country(code=args['code'], name=args['name'])
            db.session.add(country)
            db.session.commit()
            result = {'country': country.name}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class StateView(Resource):

    def get(self):
        output = []
        states = State.query.all()
        for state in states:
            result = {}
            result['id'] = state.id
            result['country_id'] = state.country_id
            result['name'] = state.name
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("country_id")
        parser.add_argument("name")
        args = parser.parse_args()
        try:
            state = State(country_id=args['country_id'], name=args['name'])
            db.session.add(state)
            db.session.commit()
            result = {'state': state.name}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class PlaceView(Resource):

    def get(self):
        output = []
        places = Place.query.all()
        for place in places:
            result = {}
            result['id'] = place.id
            result['state_id'] = place.state_id
            result['name'] = place.name
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("state_id")
        parser.add_argument("name")
        args = parser.parse_args()
        try:
            place = Place(state_id=args['state_id'], name=args['name'])
            db.session.add(place)
            db.session.commit()
            result = {'place': place.name}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class RestaurantCategoryView(Resource):

    def get(self):
        output = []
        categories = RestaurantCategory.query.all()
        for category in categories:
            result = {}
            result['id'] = category.id
            result['name'] = category.name
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()
        try:
            category = RestaurantCategory(name=args['name'])
            db.session.add(category)
            db.session.commit()
            result = {'Restaurant Category': category.name}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class TableCategoryView(Resource):

    def get(self):
        output = []
        categories = TableCategory.query.all()
        for category in categories:
            result = {}
            result['id'] = category.id
            result['title'] = category.title
            result['price'] = category.price
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("price")
        args = parser.parse_args()
        try:
            category = TableCategory(title=args['title'], price=args['price'])
            db.session.add(category)
            db.session.commit()
            result = {'Table Category': category.title}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class RestaurantView(Resource):

    def get(self):
        output = []
        restaurants = Restaurant.query.all()
        for restaurant in restaurants:
            # print(restaurant.restaurant_items)
            result = {}
            result['id'] = restaurant.id
            result['user_email'] = restaurant.user_email
            result['place_id'] = restaurant.place_id
            result['title'] = restaurant.title
            result['description'] = restaurant.description
            result['mobile'] = restaurant.mobile
            result['email'] = restaurant.email
            result['opening_time'] = restaurant.opening_time.strftime("%H:%M")
            result['closing_time'] = restaurant.closing_time.strftime("%H:%M")
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("user_email")
        parser.add_argument("restaurant_category_id")
        parser.add_argument("place_id")
        parser.add_argument("title")
        parser.add_argument("description")
        parser.add_argument("mobile")
        parser.add_argument("email")
        parser.add_argument("opening_time")
        parser.add_argument("closing_time")
        args = parser.parse_args()
        user_exist = User.query.filter_by(email=args['user_email'])
        if not user_exist:
            user = User(password='default', email=args['user_email'], user_type='admin')
            db.session.add(user)
            db.session.commit()
        try:
            opening_time = datetime.datetime.strptime(args['opening_time'], '%H:%M').time()
            closing_time = datetime.datetime.strptime(args['closing_time'], '%H:%M').time()
            restaurant = Restaurant(user_email=args['user_email'], category_id=args['restaurant_category_id'],
                                    place_id=args['place_id'], title=args['title'],
                                    description=args['description'], mobile=args['mobile'],
                                    email=args['email'], opening_time=opening_time,
                                    closing_time=closing_time)
            db.session.add(restaurant)
            db.session.commit()
            result = {'Restaurant Title': restaurant.title}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class TableView(Resource):

    def get(self):
        output = []
        tables = Table.query.all()
        for table in tables:
            result = {}
            result['id'] = table.id
            result['table_category_id'] = table.category_id
            result['restaurant_id'] = table.restaurant_id
            result['seat_count'] = table.seat_count
            result['count'] = table.count
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("table_category_id")
        parser.add_argument("restaurant_id")
        parser.add_argument("seat_count")
        parser.add_argument("count")
        args = parser.parse_args()
        try:
            table = Table(category_id=args['table_category_id'], restaurant_id=args['restaurant_id'],
                                        seat_count=args['seat_count'], count=args['count'])
            db.session.add(table)
            db.session.commit()
            result = {'Table': table.id}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class MenuView(Resource):

    def get(self):
        output = []
        items = MenuItem.query.all()
        for item in items:
            result = {}
            result['restaurant_id'] = item.restaurant_id
            result['name'] = item.name
            result['description'] = item.description
            result['price'] = item.price
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("restaurant_id")
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("price")
        args = parser.parse_args()
        try:
            item = MenuItem(restaurant_id=args['restaurant_id'], name=args['name'], description=args['description'],
                                price=args['price'])
            db.session.add(item)
            db.session.commit()
            result = {'Item Name': item.name}
        except:
            status_code = 404
            result = {'message': 'There is some error'}
        return result, status_code

    def put(self):
        pass


class OrderView(Resource):

    def get(self):
        output = []
        orders = Order.query.all()
        for order in orders:
            result = {}
            result['id'] = order.id
            result['user_email'] = order.user_email
            result['mobile'] = order.mobile
            result['restaurant_id'] = order.restaurant_id
            result['order_time'] = order.order_time.strftime("%m/%d/%Y, %H:%M:%S")
            result['spend_hour'] = order.spend_hour
            result['paid'] = order.paid
            result['active'] = order.active
            result['status'] = order.status.value
            result['tables'] = [table.id for table in order.order_tables]
            output.append(result)
        return output

    def post(self):
        status_code = 200
        parser = reqparse.RequestParser()
        parser.add_argument("user_email")
        parser.add_argument("mobile")
        parser.add_argument("restaurant_id")
        parser.add_argument("spend_hour")
        parser.add_argument('table', action='append')
        parser.add_argument('selected_items', action='split')
        args = parser.parse_args()
        user_exist = User.query.filter_by(email=args['user_email'], user_type='customer').all()
        if not user_exist:
            user = User(password='default', email=args['user_email'], user_type='customer')
            db.session.add(user)
            db.session.commit()
        # try:
        order_obj = Order(user_email=args['user_email'], mobile=args['mobile'], restaurant_id=args['restaurant_id'],
                          spend_hour=args['spend_hour'], active=True)
        db.session.add(order_obj)
        db.session.commit()
        for table_id in args.table:
            table_obj = Table.query.get(int(table_id))
            table_obj.table_orders.append(order_obj)
        db.session.commit()


        result = {'Item Name': order_obj.id}
        # except:
        #     status_code = 404
        #     result = {'message': 'There is some error'}
        return result, status_code

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