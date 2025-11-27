from django.test import TestCase, Client
from django.urls import reverse
import json


class UpdateStatusTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = "/api/update-status/"

    def test_update_status_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Only POST allowed"})

    def test_update_status_missing_status(self):
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Status is required"})

    def test_update_status_success(self):
        body = {"status": "completed"}
        response = self.client.post(
            self.url,
            data=json.dumps(body),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "Status updated successfully",
                "new_status": "completed"
            }
        )
