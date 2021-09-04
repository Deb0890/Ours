from io import StringIO
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from bs4 import BeautifulSoup

# define test case here, this includes things like a user and data that is passed into the functions
class AuthUrlTests(TestCase):

    #client = Client() seems to not be needed

    def test_signup_page_response_status(self):
        response = self.client.get(reverse('sign_up'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page_response_status(self):
        response = self.client.get(reverse('log_in'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page_response_status(self):
        response = self.client.get(reverse('log_out'), follow=True)
        self.assertEqual(response.status_code, 200)

    
    def test_content_of_title_is_signup(self):
        response = self.client.get(reverse('sign_up'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Sign Up'


#signup page should redirect on submitting
    # def test_signup_page_post_response(self):
    #     self.user= {
    #         "username":"username",
    #         "email":"bob@example.com",
    #         "first_name":"Bob",
    #         "last_name":"Smith",
    #         "password1":"mypassword",
    #         "password2":"mypassword"
    #     }

    #     response = self.client.post(reverse('sign_up') )
    #     self.assertEqual(response.status_code, 302)

#also possibly create test that shouldn't sign up user with an existing username, 409?

#correct page renders
    def test_signup_page_renders(self):
        response = self.client.get(reverse('sign_up'), follow=True)
        self.assertTemplateUsed(response, 'auth/signup.html')
    
    def test_login_page_renders(self):
        response = self.client.get(reverse('log_in'), follow=True)
        self.assertTemplateUsed(response, 'auth/login.html')
    
    def test_logout_page_renders(self):
        response = self.client.get(reverse('log_out'), follow=True)
        self.assertTemplateUsed(response, 'auth/logout.html')


# class AuthViewTests(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.bar = 



    

    


# class Test_tests(TestCase):

#     def test_one_one(self):
#         self.assertEqual(1+1, 2)

#     def test_one_Two(self):
#         self.assertEqual(1+1, 3)
