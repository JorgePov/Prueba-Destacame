import json, datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class LocationsTestCase(TestCase):
    fixtures = ['locations/fixtures/test.json']
    maxDiff = None

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
            "id": 3,
            "traveler": 1234,
            "travel": 1,
            "location_number": 5,
            "travel_date": "2022-08-08T02:00:00",
            "boarding_time": "01:50:00"
        }

        response = client.post(
            '/api/v1/locations', 
            {
                "traveler": 1234,
                "travel": 1,
                "location_number": 5,
                "travel_date": "2022-08-08 02:00:00.000000+00",
                "boarding_time": "01:50:00"
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('traveler', result)
        self.assertIn('travel', result)
        self.assertIn('location_number', result)
        self.assertIn('boarding_time', result)
        self.assertEqual(result, test_assert)

    def test_busy_location_number(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {'res': 'No se puede reservar, puesto ya se encuentra ocupado para este viaje'}

        response = client.post(
            '/api/v1/locations', 
            {
                "traveler": 1234,
                "travel": 1,
                "location_number": 3,
                "travel_date": "2022-08-08 02:00:00.000000+00",
                "boarding_time": "01:50:00"
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_location_number_greater_than_capacity(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {"res": "El puesto no existe, el bus tiene 10 puestos"}

        response = client.post(
            '/api/v1/locations', 
            {
                "traveler": 1234,
                "travel": 1,
                "location_number": 20,
                "travel_date": "2022-08-08 02:00:00.000000+00",
                "boarding_time": "01:50:00"
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
            "location_number": 8,
        }

        response = client.patch(
            '/api/v1/locations/1', 
            {
                "location_number": 8
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('location_number', result)

    def test_update_busy_location_number(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {'res': 'No se puede realizar el cambio, puesto ya se encuentra ocupado para este viaje'}

        response = client.patch(
            '/api/v1/locations/1', 
            {
                "location_number": 3
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(result, test_assert)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.delete('/api/v1/locations/1')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            'traveler': {
                'id_card': 1234,
                'first_name': 'juana', 
                'last_name': 'de arco', 
                'age': 25
            }, 
            'travel': {
                'id': 1, 
                'bus': {
                    'bus_plate': 'MUS32F', 
                    'capacity': 10, 
                    'is_active': True
                }, 
                'journey': {
                    'id': 1, 
                    'destination': 'Neiva', 
                    'origin': 'Paipa', 
                    'price': 20000, 
                    'is_active': True
                }, 
                'scheduled': {
                    'id': 1, 
                    'departure_time': '01:00:00', 
                    'cases_closing': '00:50:00'
                }, 
                'driver': {
                    'id': 1, 
                    'email': 'testing01@destacame.com', 
                    'first_name': 'Testing', 
                    'last_name': 'Testing', 
                    'full_name': 'Testing Testing', 
                    'is_driver': True, 
                    'is_seller': False, 
                    'is_staff': True
                }, 
                'is_active': True
            }, 
            'location_number': 3, 
            'travel_date': '2022-08-07T21:00:00', 
            'boarding_time': '01:50:00'
        }

        response = client.get('/api/v1/locations/1')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('traveler', result)
        self.assertIn('travel', result)
        self.assertIn('location_number', result)
        self.assertIn('boarding_time', result)
        self.assertEqual(result, test_assert)

    def test_get_traveler_locations(self):
        client = APIClient()
        time_static_1=str(datetime.datetime.now() + datetime.timedelta(hours=3))
        time_static_2=str(datetime.datetime.now() + datetime.timedelta(days=3))
        time_static_3=str(datetime.datetime.now() - datetime.timedelta(hours=3))
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(
            '/api/v1/locations', 
            {
                "traveler":1234, 
                "travel":1, 
                "location_number":8, 
                "travel_date": time_static_1,
                "boarding_time": "01:50:00"
            },
            format='json'
        )
        response = client.post(
            '/api/v1/locations', 
            {
                "traveler":1234, 
                "travel":1, 
                "location_number":9, 
                "travel_date": time_static_2,
                "boarding_time": "01:50:00"
            },
            format='json'
        )
        response = client.post(
            '/api/v1/locations', 
            {
                "traveler":1234, 
                "travel":1, 
                "location_number":10, 
                "travel_date": time_static_3,
                "boarding_time": "01:50:00"
            },
            format='json'
        )

        
        test_assert = [{
            'traveler': {
                'id_card': 1234,
                'first_name': 'juana', 
                'last_name': 'de arco', 
                'age': 25
            }, 
            'travel': {
                'id': 1, 
                'journey': {
                    'id': 1, 
                    'destination': 'Neiva', 
                    'origin': 'Paipa', 
                    'price': 20000, 
                    'is_active': True
                },
            }, 
            'location_number': 8, 
            'travel_date': time_static_1.replace(" ", "T"), 
            'boarding_time': '01:50:00'
        },
        {
            'traveler': {
                'id_card': 1234,
                'first_name': 'juana', 
                'last_name': 'de arco', 
                'age': 25
            }, 
            'travel': {
                'id': 1, 
                'journey': {
                    'id': 1, 
                    'destination': 'Neiva', 
                    'origin': 'Paipa', 
                    'price': 20000, 
                    'is_active': True
                },
            }, 
            'location_number': 9, 
            'travel_date': time_static_2.replace(" ", "T"), 
            'boarding_time': '01:50:00'
        }]

        client.credentials()
        response = client.get('/api/v1/locations/travelers/1234')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for locations in result:
            self.assertIn('traveler', locations)
            self.assertIn('travel', locations)
            self.assertIn('location_number', locations)
            self.assertIn('boarding_time', locations)
            break
        self.assertEqual(result, test_assert)
        
