import unittest
from app import create_app
from app.models import db, Mechanic, Customer, Service_Ticket
from app.utils.auth import encode_token
from werkzeug.security import generate_password_hash
from datetime import date
from app.extensions import ma
from marshmallow import fields

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            self.mechanic = Mechanic(
                name="Test",
                email="mtest@email.com",
                phone="9876543210",
                salary=50000.00
            )
            db.session.add(self.mechanic)
            db.session.commit()
            db.session.refresh(self.mechanic)



    #Create Mechanic
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "000-000-0000",
            "salary": 45000.00
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")


    #Create Mechanic - Invalid    
    def test_create_invalid_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "phone": "1234567890"
        }
        
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)


    #Retrieve All Mechanics
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'Test')


    #Retrieve Specific Mechanic by ID    
    def test_get_mechanic_by_id(self):
        mechanic_id = self.mechanic.id  # use the real ID from the test DB
        response = self.client.get(f'/mechanics/{mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test')    


    #Update Mechanic
    def test_mechanic_update(self):
        mechanic_update_payload = {
            "name": "UPDATED MECHANIC",
            "email": "test@email.com",
            "phone": "123-456-7890",
            "salary": 55000.00
        }
        
        response = self.client.put('/mechanics/1', json=mechanic_update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'UPDATED MECHANIC')


    #Delete Mechanic    
    def test_delete_mechanic(self):
        with self.app.app_context():
            # Confirm the mechanic exists before deletion
            mechanic = db.session.get(Mechanic, 1)
            self.assertIsNotNone(mechanic)

        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])

        with self.app.app_context():
            # Confirm the mechanic has been deleted
            deleted_mechanic = db.session.get(Mechanic, 1)
            self.assertIsNone(deleted_mechanic)


    def test_popular_mechanics(self):
        with self.app.app_context():
            # Create a customer (required for FK in Service_Ticket)
            customer = Customer(name="Test Customer", email="cust@test.com", phone="1234567890", password="test1234")
            db.session.add(customer)
            db.session.commit()

            # Create mechanics
            mechanic1 = Mechanic(name="Alice", email="alice@test.com", phone="111", salary=50000)
            mechanic2 = Mechanic(name="Bob", email="bob@test.com", phone="222", salary=60000)
            db.session.add_all([mechanic1, mechanic2])
            db.session.commit()

            # Create service tickets for customer
            ticket1 = Service_Ticket(VIN="1HGCM82633A004352", service_date=date.today(), service_desc="Fix engine", customer_id=customer.id)
            ticket2 = Service_Ticket(VIN="1HGCM82633A004353", service_date=date.today(), service_desc="Replace tires", customer_id=customer.id)
            ticket3 = Service_Ticket(VIN="1HGCM82633A004354", service_date=date.today(), service_desc="Oil change", customer_id=customer.id)
            db.session.add_all([ticket1, ticket2, ticket3])
            db.session.commit()

            # Assign tickets to mechanics
            mechanic1.service_tickets.append(ticket1)
            mechanic1.service_tickets.append(ticket2)  # mechanic1 has 2 tickets
            mechanic2.service_tickets.append(ticket3)  # mechanic2 has 1 ticket
            db.session.commit()

        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)

        mechanics = response.json
        # mechanic1 with 2 tickets should be first
        self.assertEqual(mechanics[0]['name'], "Alice")
        self.assertEqual(len(mechanics[0]['service_tickets']), 2)
        # mechanic2 with 1 ticket should be second
        self.assertEqual(mechanics[1]['name'], "Bob")
        self.assertEqual(len(mechanics[1]['service_tickets']), 1)



    # Test the /search route with valid name parameter
    def test_search_mechanic_valid(self):
        with self.app.app_context():
            mechanic = Mechanic(name="Charlie", email="charlie@email.com", phone="333", salary=55000)
            db.session.add(mechanic)
            db.session.commit()
        
        response = self.client.get('/mechanics/search?name=Char')
        self.assertEqual(response.status_code, 200)
        mechanics = response.json
        self.assertTrue(any(m['name'] == "Charlie" for m in mechanics))


    # Test the /search route with missing name parameter
    def test_search_mechanic_missing_name(self):
        response = self.client.get('/mechanics/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing 'name' parameter", response.json.get("error", ""))
