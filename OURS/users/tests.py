from OURS.users import admin
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import pytest

# create an instance of the client for our use

# define test case here, this includes things like a user and data that is passed into the functions
class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

class Auth_views_tests(BaseTestCase):
    def setUp(self):
        self.c = Client()
        self.c.login(username="myusername", password="mypassword")



# class Test_tests(TestCase):

#     def test_one_one(self):
#         self.assertEqual(1+1, 2)

#     def test_one_Two(self):
#         self.assertEqual(1+1, 3)