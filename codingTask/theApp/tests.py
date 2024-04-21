from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from theApp.models.users import Contact
from theApp.models.spam import Spam

User = get_user_model()

class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')

    def test_user_signup(self):
        data = {
            'name': 'Test User',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('User created successfully.', response.data['Message'])

    def test_invalid_user_signup(self):
        # Missing required fields
        data = {
            'name': 'Test User',
            'password': 'testpassword'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LoginLogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(name='Test User', phone_number='1234567890', password='testpassword')

    def test_user_login(self):
        data = {
            'phone_number': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Login successful', response.data['message'])

    def test_user_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('User logged out successfully.', response.data['Message'])

    def test_invalid_user_login(self):
        data = {
            'phone_number': '1234567890',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SpamTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.report_spam_url = reverse('report_spam')
        self.user = User.objects.create_user(name='Test User', phone_number='1234567890', password='testpassword')

    def test_report_spam(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'phone_number': '1234567890',
        }
        response = self.client.post(self.report_spam_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Number: 1234567890 is reported as spam.', response.data['message'])

    # Add more spam related test cases if needed

class SearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.search_by_name_url = reverse('search_by_name')
        self.search_by_number_url = reverse('search_by_number')
        self.user = User.objects.create_user(name='Test User', phone_number='1234567890', password='testpassword')
        self.contact = Contact.objects.create(name='Test Contact', phone_number='1234567891')
        self.spam = Spam.objects.create(phone_number='1234567891', spam_reported_count=2)

    def test_search_by_name(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test'
        }
        response = self.client.post(self.search_by_name_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Contact', response.data['Results']['search_results'][0]['name'])

    def test_search_by_number(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'phone_number': '1234567891'
        }
        response = self.client.post(self.search_by_number_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Contact', response.data['Results']['search_results'][0]['name'])
        self.assertEqual(response.data['Results']['search_results'][0]['spam_likelihood (number of times this number is reported as a spam)'], 2)

    # Add more search related test cases if needed
