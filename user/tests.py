from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class LoginViewTest(TestCase):
    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user(username ='alex', password="abcd@1234")
        self.login_url = reverse('login')

    def test_valid_login_redirects_to_index(self):
        response = self.client.post(self.login_url,{
            'username':'alex',
            'password':'abcd@1234'
        })
        self.assertRedirects(response, reverse('index'))
    
    def test_invalid_login_shows_error(self):
        repsonse = self.client.post(self.login_url,{
            'username':'alex',
            'password':'wrongpass'
        })
        self.assertContains(repsonse, 'Invalid creadentials!', html=True)
