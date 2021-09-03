from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# create an instance of the client for our use

class Users_tests(TestCase):

    #client = Client()

    def test_one_one(self):
            self.assertEqual(1+1, 2)