from io import StringIO
from django import template
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from bs4 import BeautifulSoup
from users.models import Profile
#from users.views import sign_up, get_profile, update_profile

# define test case here, this includes things like a user and data that is passed into the functions
class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        cls.user = {
            "username":"unclebob",
            "email":"bob@example.com",
            "first_name":"Bob",
            "last_name":"Smith",
            "password1":"cFtr5lB7",
            "password2":"cFtr5lB7"
        }

        cls.user_bad_email = {
            "username":"danj",
            "email":"myemail@crazymail.com",
            "first_name":"Dan",
            "last_name":"Cooper",
            "password1":"mypassword",
            "password2":"mypassword"
        }

        cls.user_bad_username = {
            "username":"myusername",
            "email":"crazymail@crazymail.com",
            "first_name":"James",
            "last_name":"Derrick",
            "password1":"mypassword",
            "password2":"mypassword"
        }        

        cls.user_bad_passwords = {
            "username":"deb0890",
            "email":"newemail@crazymail.com",
            "first_name":"deb",
            "last_name":"Francis",
            "password1":"mypassword45",
            "password2":"mypassword"
        }    

        cls.user_info = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
        # cls.user_info_two = User.objects.create_user('thisusername', 'thisemail@crazymail.com', 'thispassword')
        cls.user_info.save()
        cls.user_info.profile.user_id = User.objects.get(id=1)
        cls.user_info.profile.bio = 'This is a test bio'
        cls.user_info.save()


class AuthUrlTests(BaseTestCase):

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
    
    def test_content_of_title_is_login(self):
        response = self.client.get(reverse('log_in'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Log In'

    #signup page should redirect on submitting
    def test_signup_user_and_login_at_once(self):
        response = self.client.post(reverse('sign_up'), self.user, follow=True)
        self.assertTemplateUsed(response,'pages/dashboard.html')

    def test_the_right_template_is_rendered(self):       
        response = self.client.post(reverse('sign_up'), self.user, follow=True)
        # create a list of templates and check the one we want to use is in that list
        assert('auth/signup.html' not in [template.name for template in response.templates])

    def test_base_template_present(self):
        response = self.client.get(reverse('sign_up'), follow=True)
        #templates = [template for template in response.templates]
        assert('auth/base.html' in [template.name for template in response.templates])

        
    #correct page renders
    def test_signup_page_renders(self):
        response = self.client.get(reverse('sign_up'), follow=True)
        self.assertTemplateUsed(response, 'auth/signup.html')
    
    def test_login_page_renders(self):
        response = self.client.get(reverse('log_in'), follow=True)
        self.assertTemplateUsed(response, 'auth/login.html')


class ProtectedRoutesTests(BaseTestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username= 'myusername', password= 'mypassword')

    def test_can_view_dashboard_when_logged_in(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        assert('pages/dashboard.html' in [template.name for template in response.templates])
   
    def test_dashboard_extends_base_template(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        assert('pages/base.html' in [template.name for template in response.templates])
    
    def test_user_can_access_profile_to_update(self):
        response = self.client.get(reverse('update_profile'), follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        self.assertTemplateUsed(response, 'auth/profile.html')


    def test_content_of_title_is_profile(self):
        response = self.client.get(reverse('update_profile'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Profile'

    def test_user_can_view_profile(self):
        response = self.client.get(reverse('single_profile', args=[1]), follow=True)
        self.assertTemplateUsed(response, 'auth/single-profile.html')

    def test_user_can_logout(self):
        response = self.client.get(reverse('log_out'), follow=True)
        print([template.name for template in response.templates])
        self.assertTemplateUsed(response, 'pages/homepage.html')


class ErrorRoutes(BaseTestCase):

    def test_view_url_does_not_exist(self):
        response = self.client.get('/users', follow=True)
        self.assertEqual(response.status_code, 404)

    # def test_custom_error_page_does_not_exist_renders(self):
    #     response = self.client.get('/notapage', follow=True)
    #     self.assertTemplateUsed(response, 'pages/404.html')

    def test_custom_error_unauthorized_access(self):
        response = self.client.get('/notapage', follow=True)
        #self.assertTemplateNotUsed('pages/dashboard.html')
        self.assertEqual(response.status_code, 404)

class TestUserModels(BaseTestCase):   

    # def setUp(self):
    #     self.client = Client()
    #     self.client.login(username= 'myusername', password= 'mypassword')

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_user_profile_contains_bio(self):
        user_bio = self.user_info.profile.bio
        self.assertTrue(user_bio)
    
    #if we create a user we should have 2 users in database
    def test_user_is_added_to_db(self):
        User.objects.create_user('myusername1', 'myemail1@crazymail.com', 'mypassword')
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_username_is_not_valid(self):
        response = self.client.post(reverse('sign_up'), self.user_bad_username, follow=True)
        self.assertTemplateUsed(response,'auth/signup.html')

    def test_email_is_not_valid(self):
        response = self.client.post(reverse('sign_up'), self.user_bad_email, follow=True)
        self.assertTemplateUsed(response,'auth/signup.html')  
    
    def test_password_is_not_valid(self):
        response = self.client.post(reverse('sign_up'), self.user_bad_passwords, follow=True)
        self.assertTemplateUsed(response,'auth/signup.html')

    



#if login info is missing, user isn't created


#if there are duplicate emails and usernames or weak password, check user isn't signed up