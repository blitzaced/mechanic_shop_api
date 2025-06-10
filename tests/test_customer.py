from app import create_app
from app.models import db, Customer, Service_Ticket
from datetime import date
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

    
    #Create Customer
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

    
    #Create Customer - Invalid    
    def test_create_invalid_cusomter(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "1234567890"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)
        
    
    #Retrieve All Customers
    def test_get_customers(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'Test')
    
    
    #Retrieve Specific Customer by ID    
    def test_get_customer_by_id(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test')       
        
    
    #Customer Login
    def test_login_customer(self):
        customer_payload = {
            "email": "test@email.com",
            "password": "123"
        }
        
        response = self.client.post('/customers/login', json=customer_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        
    
    #Update Customer
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
    
    
    #Delete Customer(auth req)    
    def test_delete_customer(self):
        with self.app.app_context():
            # Confirm the customer exists before deletion
            customer = db.session.get(Customer, 1)
            self.assertIsNotNone(customer)

        # Perform DELETE with token auth
        response = self.client.delete(
            '/customers/',
            headers={'Authorization': f'Bearer {self.token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])

        with self.app.app_context():
            # Confirm the customer has been deleted
            deleted_customer = db.session.get(Customer, 1)
            self.assertIsNone(deleted_customer)
    
    
    #Get My Tickets (auth req)        
    def test_get_my_tickets(self):
        with self.app.app_context():
            # Create a service ticket linked to the test customer (ID 1)
            ticket = Service_Ticket(
                VIN="1HGCM82633A004352",
                customer_id=1,
                service_date=date.today(),
                service_desc="Oil change and tire rotation"
            )
            db.session.add(ticket)
            db.session.commit()

        # Make authenticated GET request
        response = self.client.get(
            '/customers/my-tickets',
            headers={'Authorization': f'Bearer {self.token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['service_desc'], "Oil change and tire rotation")