import base64
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json
from wehaveweneed.web.models import Category, Post, UserProfile

# This technique for testing a resource protected via HTTP Auth is described
# here: http://thomas.pelletier.im/2009/12/test-your-django-piston-api-with-auth/
class BaseHttpAuthenticatedClient(TestCase):
    def setUp(self):
        self.client = Client()
        # Assumes you've already created a user / pass of, "admin" / "admin".
        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }

class ApiTest(BaseHttpAuthenticatedClient):
    def setUp(self):
        super(ApiTest, self).setUp()
        category = Category(slug="food", name="Food")
        category.save()
        need = Post(title="Test Need",
                    location="Haiti",
                    category=category,
                    content="Water",
                    type="need")
        need.save()
        have = Post(title="Test Have",
                    location="Haiti",
                    category=category,
                    content="Ham Sandwich",
                    type="have")
        have.save()
        new_user = User.objects.create_user("admin", "admin@example.com", "admin")
        new_user_profile = UserProfile(user=new_user, organization="FooBar, Inc.")
        new_user_profile.save()

    def test_read_a_need_should_succeed(self):
        response = self.client.get("/api/needs.json")
        self.assertEqual(response.status_code, 200)
        api_response = json.loads(response.content)
        self.assertEqual(api_response[0].get("title"), "Test Need")

    def test_read_a_have_should_succeed(self):
        response = self.client.get("/api/haves.json")
        self.assertEqual(response.status_code, 200)
        api_response = json.loads(response.content)
        self.assertEqual(api_response[0].get("title"), "Test Have")

    def test_read_a_post_should_succeed(self):
        response = self.client.get("/api/post/1.json")
        self.assertEqual(response.status_code, 200)
        api_response = json.loads(response.content)
        self.assertEqual(api_response.get("title"), "Test Need")
        self.assertEqual(api_response.get("content"), "Water")
        self.assertEqual(api_response.get("location"), "Haiti")

    def test_read_categories_should_succeed(self):
        response = self.client.get("/api/categories.json")
        self.assertEqual(response.status_code, 200)
        api_response = json.loads(response.content)
        self.assertEqual(api_response[0].get("name"), "Food")
        self.assertEqual(api_response[0].get("slug"), "food")

    def test_a_test_user_should_already_exist(self):
        user = User.objects.get(username="admin")
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, "admin@example.com")

    def test_authenticated_post_should_succeed(self):
        # When creating a new post via the API you must use the value of "slug"
        # for the "category" parameter.
        new_post = {"title": "Test Post",
                    "location": "Haiti",
                    "category": "food",
                    "content": "water",
                    "priority": "mid",
                    "type": "need"}
        self.client.login(username="admin", password="admin")
        new_post_response = self.client.post("/api/post/", data=new_post, follow=True, **self.extra)
        self.assertEqual(new_post_response.status_code, 201)
        # The new Post ID is returned as the content of the API call.
        test_response = self.client.get("/api/post/%s.json" % new_post_response.content)
        api_response = json.loads(test_response.content)
        self.assertEqual(api_response.get("title"), "Test Post")
        self.assertEqual(api_response.get("content"), "water")
        self.assertEqual(api_response.get("location"), "Haiti")

    def test_authenticated_post_with_bad_values_should_be_rejected(self):
        # This post leaves off the "priority" field which is a required field.
        new_post = {"title": "Test Post",
                    "location": "Haiti",
                    "category": "food",
                    "content": "water",
                    "type": "need"}
        self.client.login(username="admin", password="admin")
        new_post_response = self.client.post("/api/post/", data=new_post, follow=True, **self.extra)
        self.assertEqual(new_post_response.status_code, 400)
