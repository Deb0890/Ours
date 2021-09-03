from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import pytest

# create an instance of the client for our use

# class BaseTestCase(TestCase):
    
#     @classmethod
#     def setUpTestData(cls):

#         # cls.bar = Owned_status.objects.create(
#         #     status="owned"
#         # )
#         # cls.bar.save()

#         # cls.foo = Review.objects.create(
#         #     album="Donda",
#         #     artist="Kanye West",
#         #     owned=cls.bar,
#         #     score=6,
#         #     best_of_the_week=False,
#         #     review="This album was okay.")

#         cls.user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')




class Users_tests(TestCase):

    #client = Client()
    
    def test_one_one(self):
            self.assertEqual(1+1, 2)
    
    def test_one_Two(self):
            self.assertEqual(1+1, 3)