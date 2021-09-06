from io import StringIO
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from bs4 import BeautifulSoup
# Create your tests here.

#views tests

class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        cls.user = {
            "username":"username",
            "email":"bob@example.com",
            "first_name":"Bob",
            "last_name":"Smith",
            "password1":"cFtr5lB7",
            "password2":"cFtr5lB7"
        }

        cls.users_info = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

class PagesUrlTests(BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username= 'myusername', password= 'mypassword')
    #client = Client() seems to not be needed

    def test_homepage_response_status(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_response_status(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_lesson_create_response_status(self):
        response = self.client.get(reverse('lesson-create'), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_lesson_single_response_status(self):
        response = self.client.get(reverse('lesson-single'), follow=True)
        print(response)
        self.assertEqual(response.status_code, 200)
    
    def test_find_a_lesson_response_status(self):
        response = self.client.get(reverse('find-a-lesson'), follow=True)
        self.assertEqual(response.status_code, 200)

    
    
#     def test_content_of_title_is_signup(self):
#         response = self.client.get(reverse('sign_up'), follow=True)
#         html = response.content
#         html_in_text_format = BeautifulSoup(html, 'html.parser')
#         assert html_in_text_format.title.string == 'Sign Up'
    
#     def test_content_of_title_is_login(self):
#         response = self.client.get(reverse('log_in'), follow=True)
#         html = response.content
#         html_in_text_format = BeautifulSoup(html, 'html.parser')
#         assert html_in_text_format.title.string == 'Log In'

#     #signup page should redirect on submitting
#     def test_signup_page_post_response(self):
#         response = self.client.post(reverse('sign_up'), self.user, follow=True)
#         self.assertTemplateUsed(response,'pages/dashboard.html')

#     #also possibly create test that shouldn't sign up user with an existing username, 409?

#     def test_the_right_template_is_rendered(self):       
#         response = self.client.post(reverse('sign_up'), self.user, follow=True)
#         # create a list of templates and check the one we want to use is in that list
#         assert('auth/signup.html' not in [template.name for template in response.templates])

#     def test_base_template_present(self):
#         response = self.client.get(reverse('sign_up'), follow=True)
#         #templates = [template for template in response.templates]
#         assert('auth/base.html' in [template.name for template in response.templates])

        
    #correct page renders
    def test_homepage_renders(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertTemplateUsed(response, 'pages/homepage.html')
    
    def test_dashboard_renders(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
    
    def test_lesson_create_page_renders(self):
        response = self.client.get(reverse('lesson-create'), follow=True)
        self.assertTemplateUsed(response, 'pages/lesson-create.html')

    def test_find_a_lesson_page_renders(self):
        response = self.client.get(reverse('find-a-lesson'), follow=True)
        self.assertTemplateUsed(response, 'pages/find-a-lesson.html')

# class ProtectedRoutesTests(BaseTestCase):

#     def setUp(self):
#         self.client = Client()
#         self.client.login(username= 'myusername', password= 'mypassword')

#     def test_can_view_dashboard_when_logged_in(self):
#         response = self.client.get(reverse('dashboard'), follow=True)
#         #self.assertTemplateNotUsed('pages/dashboard.html')
#         assert('pages/dashboard.html' in [template.name for template in response.templates])
   
#     def test_dashboard_extends_base_template(self):
#         response = self.client.get(reverse('dashboard'), follow=True)
#         #self.assertTemplateNotUsed('pages/dashboard.html')
#         assert('pages/base.html' in [template.name for template in response.templates])

class ErrorRoutes(BaseTestCase):


    def test_custom_error_does_not_exist_renders(self):
        response = self.client.get('/bob', follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        self.assertEqual(response, 'pages/404.html')

    def test_custom_server_error_renders(self):
        response = self.client.get('/bob', follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        self.assertEqual(response, 'pages/500.html')

    def test_view_url_does_not_exist(self):
        response = self.client.get('/home', follow=True)
        self.assertEqual(response.status_code, 404)


# class Test_tests(TestCase):

#     def test_one_one(self):
#         self.assertEqual(1+1, 2)

#     def test_one_Two(self):
#         self.assertEqual(1+1, 3)