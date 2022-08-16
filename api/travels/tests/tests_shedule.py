import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ScheduleTestCase(TestCase):
    fixtures = ['travels/fixtures/test.json']

    def setUp(self):

        client = APIClient()

        response = client.post(
                '/api/v1/users/login', {
                'email': 'testing01@destacame.com',
                'password': 'dddd',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access']

    def test_get_Schedule(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/schedules/2')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)
        for journey in result:
            self.assertIn('id', journey)
            self.assertIn('departure_time', journey)
            self.assertIn('cases_closing', journey)
            break


