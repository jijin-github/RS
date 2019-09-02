import enum

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from sqlalchemy.dialects.mysql import TIME

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserType(enum.Enum):
    superadmin = 'superadmin'
    admin = 'admin'
    customer = 'customer'


class User(db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    mobile = db.Column(db.Integer, nullable=True)
    authenticated = db.Column(db.Boolean, default=False)
    user_type = db.Column(
        db.Enum(UserType),
        default=UserType.customer,
        nullable=False
    )

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated


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


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey('user.email'),
                            nullable=False)
    user = db.relationship('User',
                               backref=db.backref('user_restaurants', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('restaurant_category.id'),
                         nullable=False)
    category = db.relationship('RestaurantCategory',
                               backref=db.backref('category_restaurants', lazy=True))

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'),
                           nullable=False)
    place = db.relationship('Place',
                               backref=db.backref('place_restaurants', lazy=True))
    title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=False)
    opening_time = db.Column(TIME(), nullable=False)
    closing_time = db.Column(TIME(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<Restaurant %r>' % self.title


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                              nullable=False)
    tables = db.relationship('Restaurant',
                            backref=db.backref('restaurant_tables', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('table_category.id'),
                            nullable=False)
    category = db.relationship('TableCategory',
                               backref=db.backref('table_catgory_tables', lazy=True))
    seat_count = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Table %r>' % self.id


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                              nullable=False)
    items = db.relationship('Restaurant',
                               backref=db.backref('restaurant_items', lazy=True))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float)


    def __repr__(self):
        return '<MenuItem %r>' % self.name


class OrderStatus(enum.Enum):
    open = 'open'
    close = 'close'


order_tables = db.Table('order_tables',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id')),
    db.Column('booked_id', db.Integer, db.ForeignKey('order.id'))
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                            nullable=False)
    restaurant = db.relationship('Restaurant',
                               backref=db.backref('restaurant_orders', lazy=True))
    order_tables = db.relationship('Table', secondary=order_tables, lazy='subquery',
                           backref=db.backref('table_orders', lazy=True))
    order_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    spend_hour = db.Column(db.Integer, default=2)
    paid = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)
    status = db.Column(
        db.Enum(OrderStatus),
        default=OrderStatus.open,
        nullable=False
    )


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),
        nullable=False)
    order = db.relationship('Order',
        backref=db.backref('order_items', lazy=True))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'),
                            nullable=False)
    menu = db.relationship('MenuItem',
        backref=db.backref('menu_carts', lazy=True))
    count = db.Column(db.Integer, nullable=True)

if __name__ == '__main__':
    manager.run()