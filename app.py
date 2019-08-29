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
        # # admin = User(password='iiiiyyyy', email='admin@example.com', mobile=99988888, user_type='admin')
        # # db.session.add(admin)
        # # db.session.commit()
        # print(User.query.all())
        return "User Not Found", 404

    def post(self):
        print("Yesss")
        pass

    def put(self):
        pass

    def delete(self):
        pass

api.add_resource(UserView, '/user/')

if __name__ == '__main__':
    app.run(debug=True)