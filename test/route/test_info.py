from app import create_app
import unittest
from unittest import TestCase
from flask import Flask, json
from config import APP_TITLE, JWT_SECRET_KEY
from flask_jwt_extended import JWTManager

app = create_app()
jwt = JWTManager(app)


class TestWelcome(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_welcome(self):
        """
        Tests the route screen message
        """
        rv = self.app.get('/api/')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": '/api/inference to get structured patient data'}, rv.get_json())


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
        self.app = app.test_client()

    def tearDown(self):
        pass  # Add any teardown logic if needed

    def test_valid_login(self):
        mock_user_data = {
            'username': 'john',
            'password': 'password123'
        }
        response = self.app.post('/api/login', data=json.dumps(mock_user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_invalid_login(self):
        mock_user_data = {
            'username': 'invalid_username',
            'password': 'invalid_password'
        }
        response = self.app.post('/api/login', data=json.dumps(mock_user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Invalid username or password')

if __name__ == '__main__':
    unittest.main()
