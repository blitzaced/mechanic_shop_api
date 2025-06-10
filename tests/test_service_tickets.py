from app import create_app
from app.models import db, Service_Ticket
import unittest
from marshmallow import ValidationError
from datetime import date


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.service_ticket = Service_Ticket(VIN="1sad6f54asdf654sd", service_date=date(2025, 5, 6), service_desc="test notes", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.service_ticket)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_service_ticket(self):
        service_ticket_payload = {
            "VIN": "1newVIN123456",
            "service_date": "2025-05-06",
            "service_desc": "test notes",
            "customer_id": 1
        }
        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1newVIN123456")