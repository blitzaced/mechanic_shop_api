from app import create_app, db
from app.models import db, Part
import unittest


class TestPartsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.part = Part(name="Oil Filter", price=19.99)
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_part(self):
        response = self.client.post('/parts/', json={
            "name": "Air Filter",
            "price": 15.99
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Air Filter", response.get_data(as_text=True))

    def test_create_duplicate_part(self):
        response = self.client.post('/parts/', json={
            "name": "Oil Filter",
            "price": 19.99
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Part already exists", response.get_data(as_text=True))

    def test_get_all_parts(self):
        response = self.client.get('/parts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Oil Filter", response.get_data(as_text=True))

    def test_get_specific_part(self):
        response = self.client.get(f'/parts/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Oil Filter", response.get_data(as_text=True))

    def test_get_nonexistent_part(self):
        response = self.client.get('/parts/999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Part not found", response.get_data(as_text=True))

    def test_update_part(self):
        response = self.client.put(f'/parts/{self.part_id}', json={
            "name": "Oil Filter",
            "price": 22.99
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("22.99", response.get_data(as_text=True))

    def test_update_nonexistent_part(self):
        response = self.client.put('/parts/999', json={
            "name": "Doesn't Matter",
            "price": 5.00
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Part not found", response.get_data(as_text=True))

    def test_delete_part(self):
        response = self.client.delete(f'/parts/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", response.get_data(as_text=True))

    def test_delete_nonexistent_part(self):
        response = self.client.delete('/parts/999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Part not found", response.get_data(as_text=True))