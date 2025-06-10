from app import create_app
from app.models import db, Part
import unittest
from marshmallow import ValidationError


class TestPart(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.part = Part(name="Test", price=25.00)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_part(self):
        part_payload = {
            "name": "tire",
            "price": 25.00
        }
        response = self.client.post('/parts/', json=part_payload)
        self.assertRaises(ValidationError)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "tire")