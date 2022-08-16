import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TravelersTestCase(TestCase):
    fixtures = ['locations/fixtures/test.json']

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
            "id_card":108072,
            "first_name":"make",
            "last_name":"mike",
            "age":20
        }

        response = client.post(
            '/api/v1/travelers', 
            {
                "id_card":108072,
                "first_name":"make",
                "last_name":"mike",
                "age":20
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id_card', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)
        self.assertIn('age', result)
        self.assertEqual(result, test_assert)

    def test_update(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_assert = {
            "id_card": 1234,
            "first_name": "juana",
            "last_name": "de arco",
            "age": 20
        }

        response = client.patch(
            '/api/v1/travelers/1234', 
            {
                "age": 20
            },
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id_card', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)
        self.assertIn('age', result)
        self.assertEqual(result, test_assert)

    def test_get_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/v1/travelers/1234')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id_card', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)
        self.assertIn('age', result)


