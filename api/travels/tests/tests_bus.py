import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class BusTestCase(TestCase):
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

    def test_create(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'bus_plate': 'MUR32F',
            'capacity': 10,
            'is_active': True
        }

        response = client.post(
            '/api/v1/buses', 
            {
                'bus_plate': 'MUR32F',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('bus_plate', result)
        self.assertIn('capacity', result)
        self.assertIn('is_active', result)

        self.assertEqual(result, test_assert)

    def test_update(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'bus_plate': 'MUS32F',
            'capacity': 20,
            'is_active': True
        }

        response = client.patch(
            '/api/v1/buses/MUS32F', 
            {
                'capacity': '20',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bus_plate', result)
        self.assertIn('capacity', result)
        self.assertIn('is_active', result)

        self.assertEqual(result, test_assert)

    def test_get(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/buses')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)

        for bus in result:
            self.assertIn('bus_plate', bus)
            self.assertIn('capacity', bus)
            self.assertIn('is_active', bus)
            break

    def test_get_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/buses/MUS32F')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bus_plate', result)
        self.assertIn('capacity', result)
        self.assertIn('is_active', result)


