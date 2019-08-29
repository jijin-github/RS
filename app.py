from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy.dialects.mysql import TIME


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Country %r>' % self.name


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'),
                            nullable=False)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<State %r>' % self.name


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'),
                           nullable=False)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Place %r>' % self.name


class RestaurantCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<RestaurantCategory %r>' % self.name


class TableCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Category %r>' % self.title


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('TableCategory.id'),
                            nullable=False)
    category = db.relationship('tablecategory',
                               backref=db.backref('restaurant', lazy=True))
    seat_count = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Table %r>' % self.title


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Menu %r>' % self.name


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('restaurantcategory.id'),
                         nullable=False)
    category = db.relationship('RestaurantCategory',
                               backref=db.backref('restaurant', lazy=True))

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'),
                           nullable=False)
    place = db.relationship('Place',
                               backref=db.backref('restaurant', lazy=True))
    title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    opening_time = db.Column(TIME(), nullable=False)
    closing_time = db.Column(TIME(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<Restaurant %r>' % self.title


tables = db.Table('tags',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id'), primary_key=True),
    db.Column('booked_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                            nullable=False)
    restaurant = db.relationship('Restaurant',
                               backref=db.backref('restaurant', lazy=True))
    tables = db.relationship('Table', secondary=tables, lazy='subquery',
                           backref=db.backref('orders', lazy=True))
    order_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    spend_hour = db.Column(db.Integer, default=2)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),
        nullable=False)
    order = db.relationship('Order',
        backref=db.backref('orders', lazy=True))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'),
                            nullable=False)
    menu = db.relationship('Menu',
        backref=db.backref('items', lazy=True))
    count = db.Column(db.Integer, nullable=True)                            




# db.create_all()
# db.session.add(User(username="Flask", email="example@example.com"))
# db.session.add(User(username="Flask2", email="example2@example.com"))
# db.session.commit()
#
# users = User.query.all()
# print(users)