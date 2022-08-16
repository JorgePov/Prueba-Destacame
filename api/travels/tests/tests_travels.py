import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TravelsTestCase(TestCase):
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
            "bus": "MUD32F",
            "journey": 1,
            "scheduled": 3,
            "driver":2,
            'is_active': True
        }

        response = client.post(
            '/api/v1/travels', 
            {
                "bus": "MUD32F",
                "journey": 1,
                "scheduled": 3,
                "driver": 2
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('bus', result)
        self.assertIn('journey', result)
        self.assertIn('scheduled', result)
        self.assertIn('driver', result)
        self.assertIn('is_active', result)

    def test_busy_driver_on_schedule(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'res': 'El conductor ya se encuentra ocupado en ese horario'
        }

        response = client.post(
            '/api/v1/travels', 
            {
                "bus": "MUD32F",
                "journey": 1,
                "scheduled": 3,
                "driver": 1
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blocked_journey_on_schedule(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'res': 'Ya existe un viaje para este destino en este horario'
        }

        response = client.post(
            '/api/v1/travels', 
            {
                "bus": "MUD32F",
                "journey": 1,
                "scheduled": 1,
                "driver": 2
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_busy_bus_on_schedule(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'res': 'El Bus ya se encuentra ocupado en ese horario'
        }

        response = client.post(
            '/api/v1/travels', 
            {
                "bus": "MUS32F",
                "journey": 1,
                "scheduled": 2,
                "driver": 2
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            "id": 1,
            "bus": "MUD32F",
            "journey": 1,
            "scheduled": 3,
            "driver": 1,
            'is_active': True
        }

        response = client.patch(
            '/api/v1/travels/1', 
            {
                "bus": "MUD32F",
                "scheduled": 3,
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('bus', result)
        self.assertIn('journey', result)
        self.assertIn('scheduled', result)
        self.assertIn('driver', result)
        self.assertIn('is_active', result)

        self.assertEqual(result, test_assert)

    def test_update_busy_driver_on_schedule(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {'res': 'El conductor ya se encuentra ocupado en ese horario'}

        response = client.patch(
            '/api/v1/travels/2', 
            {
                "driver": 1,
                "scheduled": 3,
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_blocked_journey_on_schedule(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {"res": "Ya existe un viaje para este destino en este horario"}

        response = client.patch(
            '/api/v1/travels/2', 
            {
                "journey": 1,
                "scheduled": 1,
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_busy_bus_on_schedule(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {'res': 'El Bus ya se encuentra ocupado en ese horario'}

        response = client.patch(
            '/api/v1/travels/2', 
            {
                "bus": "MUS32F",
                "scheduled": 3,
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/travels')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)

        for travels in result:
            self.assertIn('id', travels)
            self.assertIn('bus', travels)
            self.assertIn('journey', travels)
            self.assertIn('driver', travels)
            self.assertIn('is_active', travels)
            break

    def test_get_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            "id": 1,
            "bus": {
                "bus_plate": "MUS32F",
                "capacity": 10,
                "is_active": True
            },
            "journey": {
                "id": 1,
                "destination": "Neiva",
                "origin": "Paipa",
                "price": 20000,
                "is_active": True
            },
            "scheduled": {
                "id": 1,
                "departure_time": "01:00:00",
                "cases_closing": "00:50:00"
            },
            "driver": {
                "id": 1,
                "email": "testing01@destacame.com",
                "first_name": "Testing",
                "last_name": "Testing",
                "full_name": "Testing Testing",
                "is_driver": True,
                "is_seller": False,
                "is_staff": True
            },
            "is_active": True
            }

        response = client.get('/api/v1/travels/1')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('bus', result)
        self.assertIn('journey', result)
        self.assertIn('driver', result)
        self.assertIn('is_active', result)
        self.assertEqual(result, test_assert)

    def test_get_by_driver(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/driver/travels/1')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 3)

        for travels in result:
            self.assertIn('id', travels)
            self.assertIn('bus', travels)
            self.assertIn('journey', travels)
            self.assertIn('driver', travels)
            self.assertIn('is_active', travels)
            break

