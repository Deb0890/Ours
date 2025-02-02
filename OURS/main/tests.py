# from OURS.main.forms import NewLessonForm
from main.models import Lesson, Category, Skill, SkillLevels
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
        cls.users_info.save()
        cls.category = Category.objects.create(name='music')
        cls.category.save()
        cls.skill = Skill.objects.create(name='violin', category=cls.category)
        cls.skill.save()

        cls.example_lesson = Lesson.objects.create(
            tutor = cls.users_info,
            skill = cls.skill,
            skill_level = 'beginner',
            title = 'Learn music here!',
            description = 'lesson description',
            banner_img = 'tbc',
            days = 'Monday',
            created = 'tbc'
        )



class LessonModelTests(BaseTestCase):

    # def setUp(self):
    #     self.client = Client()
    #     self.client.login(username= 'myusername', password= 'mypassword')

    def test_lesson_items_in_db(self):
        lesson = Lesson.objects.all()
        self.assertTrue(lesson)


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

    def test_create_a_lesson_response_status(self):
        response = self.client.get(reverse('lesson-create'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_find_a_lesson_response_status(self):
        response = self.client.get(reverse('find-a-lesson'), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_update_a_lesson_response_status(self):
        response = self.client.get(reverse('update-a-lesson', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_a_lesson_response_status(self):
        response = self.client.get(reverse('delete-a-lesson', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_lesson_single_response_status(self):
        response = self.client.get(reverse('lesson-single', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_new_classroom_response_status(self):
        response = self.client.get(reverse('classroom-create', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_about_the_app_response_status(self):
        response = self.client.get(reverse('about-the-app'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_to_update_classroom_response_status(self):
        response = self.client.get(reverse('classroom-update', args=[1]), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access_to_finalise_classroom_response_status(self):
        response = self.client.get(reverse('classroom-finalise', args=[1]), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access_to_update_classroom_response_status(self):
        response = self.client.get(reverse('classroom-review', args=[1]), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access_to_confirm_classroom_response_status(self):
        response = self.client.get(reverse('classroom-confirm', args=[1]), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access_to_a_classroom_response_status(self):
        response = self.client.get(reverse('classroom-single', args=[1]), follow=True)
        self.assertEqual(response.status_code, 404)

    # def test_update_a_lesson_response_status(self):
    #     response = self.client.post(reverse('update-a-lesson', args=[1]), follow=True)
    #     self.assertTemplateUsed(response, 'pages/update-lesson.html')
    

    
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

    def test_single_lesson_page_renders(self):
        response = self.client.get(reverse('lesson-single', args=[1]), follow=True)
        #self.assertEqual(response.content)
        assert('pages/lesson-single.html' in [template.name for template in response.templates])

    def test_content_of_title_is_dashboard(self):
        response = self.client.get(reverse('dashboard'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Dashboard'

    def test_content_of_title_is_lesson_create(self):
        response = self.client.get(reverse('lesson-create'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Lesson Create'

    def test_content_of_title_is_find_a_lesson(self):
        response = self.client.get(reverse('find-a-lesson'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'Find a Lesson'
    
    def test_content_of_title_is_about_our_site(self):
        response = self.client.get(reverse('about-the-app'), follow=True)
        html = response.content
        html_in_text_format = BeautifulSoup(html, 'html.parser')
        assert html_in_text_format.title.string == 'About our site'

class PagesViewsTests(BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username= 'myusername', password= 'mypassword')

    def test_lesson_create_posts_new_lesson(self):
        
        response = self.client.post(reverse('lesson-create'), follow=True)
        self.assertTemplateUsed(response, 'pages/lesson-single.html')
        

    



class ErrorRoutes(BaseTestCase):


    # def test_custom_error_does_not_exist_renders(self):
    #     response = self.client.get('/bob', follow=True)
    #     #self.assertTemplateNotUsed('pages/dashboard.html')
    #     self.assertEqual(response, 'pages/404.html')

    # def test_custom_server_error_renders(self):
    #     response = self.client.get('/bob', follow=True)
    #     #self.assertTemplateNotUsed('pages/dashboard.html')
    #     self.assertEqual(response, 'pages/500.html')

    def test_view_url_does_not_exist(self):
        response = self.client.get('/notapage', follow=True)
        self.assertEqual(response.status_code, 404)
