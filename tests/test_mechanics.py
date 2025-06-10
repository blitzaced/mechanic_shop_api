import unittest
from app import create_app
from app.models import db, Mechanic
from app.utils.auth import encode_token
from werkzeug.security import generate_password_hash

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(
        name="Test",
        email="mtest@email.com",
        phone="9876543210",
        salary=50000.00
    )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()


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