# tests.py in users app
from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        response = self.client.post('/api/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass1234',
            'role': 'regular'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_login_returns_token(self):
        User.objects.create_user(username='loginuser', password='pass123')
        response = self.client.post('/api/login/', {
            'username': 'loginuser',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.admin_user.userprofile.role = 'admin'
        self.admin_user.userprofile.save()

    def test_admin_can_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post('/api/products/', {
            'name': 'Test Product',
            'description': 'Great product',
            'price': 99.99
        })
        self.assertEqual(response.status_code, 201)

    def test_regular_user_cannot_create_product(self):
        regular_user = User.objects.create_user(username='user', password='userpass')
        token = Token.objects.create(user=regular_user)
        regular_user.userprofile.role = 'regular'
        regular_user.userprofile.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post('/api/products/', {
            'name': 'Blocked Product',
            'description': 'Should not be allowed',
            'price': 50.00
        })
        self.assertEqual(response.status_code, 403)


# tests.py in reviews app
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from products.models import Product

class ReviewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='Reviewed Item', description='desc', price=10)

        self.user = User.objects.create_user(username='reviewer', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.user.userprofile.role = 'regular'
        self.user.userprofile.save()

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'/api/products/{self.product.id}/reviews/', {
            'rating': 4,
            'feedback': 'Pretty good!'
        })
        self.assertEqual(response.status_code, 201)

    def test_duplicate_review_prevented(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(f'/api/products/{self.product.id}/reviews/', {
            'rating': 5,
            'feedback': 'Nice!'
        })
        second_review = self.client.post(f'/api/products/{self.product.id}/reviews/', {
            'rating': 3,
            'feedback': 'Changed my mind'
        })
        self.assertEqual(second_review.status_code, 400)
        
