from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import UserProfile

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create admin user
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
        Token.objects.create(user=regular_user)
        regular_user.userprofile.role = 'regular'
        regular_user.userprofile.save()
        self.client.force_authenticate(user=regular_user)

        response = self.client.post('/api/products/', {
            'name': 'Blocked Product',
            'description': 'Should not be allowed',
            'price': 50.00
        })
        self.assertEqual(response.status_code, 403)
