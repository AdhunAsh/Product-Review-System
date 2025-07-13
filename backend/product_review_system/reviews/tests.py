from urllib import response
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

