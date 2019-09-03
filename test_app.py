#!flask/bin/python
import os
import unittest

from settings import app, db
from models import User

class TestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
        self.app_context = app.app_context()
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        u = User(password="11111", email='john@example.com', mobile=999999, user_type='admin')
        assert u.email == 'john@example.com'

    def test_user_page(self):
        response = self.client.get(path='/user/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()