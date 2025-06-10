from app import create_app, db
from app.models import db, Service_Ticket, Mechanic, Part
import unittest
from datetime import date
import json



class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # or however you configure testing
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

            # Create initial test data
            self.mechanic1 = Mechanic(name="Test Mech 1", email="test@email.com", phone="789-456-1230", salary=50000.00)
            self.mechanic2 = Mechanic(name="Test Mech 2", email="test@test.com", phone="123-456-7890", salary=55000.00)
            self.part1 = Part(name="Brake Pad", price=50)
            self.part2 = Part(name="Oil Filter", price=15)
            db.session.add_all([self.mechanic1, self.mechanic2, self.part1, self.part2])
            db.session.commit()

            self.ticket = Service_Ticket(VIN="1234VIN", service_date=date(2025, 6, 10), service_desc="Initial service", customer_id=1)
            db.session.add(self.ticket)
            db.session.commit()
            
            self.ticket_id = self.ticket.id
            self.mechanic1_id = self.mechanic1.id
            self.mechanic2_id = self.mechanic2.id
            self.part1_id = self.part1.id
            self.part2_id = self.part2.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_service_ticket(self):
        payload = {
            "VIN": "5678VIN",
            "service_date": "2025-06-11",
            "service_desc": "New service",
            "customer_id": 1
        }
        response = self.client.post('/service_tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['VIN'], "5678VIN")

    def test_get_all_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_specific_service_ticket(self):
        response = self.client.get(f'/service_tickets/{self.ticket.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.ticket.id)

    def test_get_service_ticket_not_found(self):
        response = self.client.get('/service_tickets/999999')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_add_mechanic_to_ticket(self):
        response = self.client.put(f'/service_tickets/{self.ticket.id}/add-mechanic/{self.mechanic1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("successfully added", data["message"])

    def test_add_same_mechanic_again(self):
        # Add first time
        self.client.put(f'/service_tickets/{self.ticket.id}/add-mechanic/{self.mechanic1.id}')
        # Add second time should error
        response = self.client.put(f'/service_tickets/{self.ticket.id}/add-mechanic/{self.mechanic1.id}')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("already assigned", data["error"])

    def test_remove_mechanic_from_ticket(self):
        # Add mechanic first
        self.client.put(f'/service_tickets/{self.ticket.id}/add-mechanic/{self.mechanic2.id}')
        # Now remove
        response = self.client.put(f'/service_tickets/{self.ticket.id}/remove-mechanic/{self.mechanic2.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Successfully removed", data["message"])

    def test_remove_mechanic_not_assigned(self):
        response = self.client.put(f'/service_tickets/{self.ticket.id}/remove-mechanic/{self.mechanic2.id}')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("was not assigned", data["error"])

    def test_add_part_to_ticket(self):
        response = self.client.put(f'/service_tickets/{self.ticket.id}/add-part/{self.part1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("added to ticket", data["message"])

    def test_add_part_to_ticket_already_added(self):
        self.client.put(f'/service_tickets/{self.ticket.id}/add-part/{self.part1.id}')
        response = self.client.put(f'/service_tickets/{self.ticket.id}/add-part/{self.part1.id}')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("already been added", data["message"])

    def test_add_part_ticket_not_found(self):
        response = self.client.put('/service_tickets/999999/add-part/1')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Service ticket not found", data["error"])

    def test_add_part_not_found(self):
        response = self.client.put(f'/service_tickets/{self.ticket.id}/add-part/999999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Part not found", data["error"])


if __name__ == '__main__':
    unittest.main()