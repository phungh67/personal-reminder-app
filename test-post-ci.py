import unittest
import os
import json
from app import create_app  # Assuming you have an app factory, or import 'app' object

class TestPostAPI(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        os.environ['ADMIN_TOKEN'] = 'secret_test_token'
        os.environ['DB_PATH'] = ':memory:'  # Use in-memory DB for tests
        
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_publish_post_success(self):
        """Test publishing a post with correct credentials."""
        payload = {
            "title": "CI/CD Pipeline Test",
            "content": "# Testing\nThis is a test post."
        }
        headers = {
            "X-Admin-Token": "secret_test_token",
            "Content-Type": "application/json"
        }

        response = self.client.post('/api/post', data=json.dumps(payload), headers=headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('published', response.get_json()['status'])

    def test_publish_post_unauthorized(self):
        """Test publishing without the correct token."""
        payload = {"title": "Hacker Post", "content": "Should fail"}
        
        # Missing or wrong token
        response = self.client.post('/api/post', json=payload)
        
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()