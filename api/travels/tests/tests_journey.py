import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class JourneyTestCase(TestCase):
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
                'id': 4,
                'destination': 'Bogota',
                'origin': 'Girardot',
                'price': 20000,
                'is_active': True,
            }

        response = client.post(
            '/api/v1/journeys', 
            {
                'destination': 'Bogota',
                'origin': 'Girardot',
                'price': 20000
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('destination', result)
        self.assertIn('origin', result)
        self.assertIn('price', result)
        self.assertIn('is_active', result)

        self.assertEqual(result, test_assert)

    def test_journey_exist(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
                'res':"Este trayecto [Neiva - Paipa] ya existe, se encuentra asignado al siguiente id: 1"
            }

        response = client.post(
            '/api/v1/journeys', 
            {
                "destination": "Neiva",
                "origin": "Paipa",
                'price': 20000
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/journeys')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)

        for journey in result:
            self.assertIn('id', journey)
            self.assertIn('destination', journey)
            self.assertIn('origin', journey)
            self.assertIn('price', journey)
            self.assertIn('is_active', journey)
            break

    def test_get_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/journeys/1')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('destination', result)
        self.assertIn('origin', result)
        self.assertIn('price', result)
        self.assertIn('is_active', result)

    def test_update(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'id': 1,
            'price': 25000,
            'is_active': True
        }

        response = client.patch(
            '/api/v1/journeys/1', 
            {
                'price': 25000,
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('price', result)
        self.assertIn('is_active', result)

        self.assertEqual(result, test_assert)
