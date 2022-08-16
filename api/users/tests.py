import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            email='testing01@destacame.com',
            first_name='Testing',
            last_name='Testing',
            age=30,
            id_card=1070622791,
            username='testing_login',
            is_staff=True,
        )
        user.set_password('dddd')
        user.save()

    def test_signup_user(self):
        client = APIClient()
        response = client.post(
                '/api/v1/users/login', {
                'email': 'testing01@destacame.com',
                'password': 'dddd',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        result = json.loads(response.content)
        
        self.assertIn('access', result)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])
        response = client.post(
                '/api/v1/users/signup', {
                'email': 'testing@desstacame.com',
                'password': 'rc{4@qHjR>!b`yAV',
                'first_name': 'Testing',
                'last_name': 'Testing',
                'age': 30,
                'id_card' : 1070622791,
                'is_driver': True,
                'username': 'testing01'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login_user(self):

        client = APIClient()
        response = client.post(
                '/api/v1/users/login', {
                'email': 'testing01@destacame.com',
                'password': 'dddd',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        result = json.loads(response.content)
        self.assertIn('access', result)