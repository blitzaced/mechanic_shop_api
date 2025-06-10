from app import create_app
from app.models import db, Customer
import unittest
from marshmallow import ValidationError
from app.utils.auth import encode_token
from werkzeug.security import generate_password_hash


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="Test", email="test@email.com", phone="123-456-7890", password="123")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "000-000-0000",
            "password": "123"
        }
        response = self.client.post('/customers/', json=customer_payload)
        self.assertRaises(ValidationError)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

        
    def test_create_invalid_cusomter(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "1234567890"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)
        
    
    def test_get_customers(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'Test')
        
    
    def test_login_customer(self):
        customer_payload = {
            "email": "test@email.com",
            "password": "123"
        }
        
        response = self.client.post('/customers/login', json=customer_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        
    
    def test_customer_update(self):
        customer_update_payoload = {
            "name": "NEW CUSTOMER",
            "email": "test@email.com",
            "phone": "123-456-7890",
            "password": "123"
        }
        
        headers = {'Authorization': "Bearer "+ self.token}
        response = self.client.put('/customers/', json=customer_update_payoload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'NEW CUSTOMER')