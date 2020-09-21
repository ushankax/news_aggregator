from django.test import TestCase, Client
from django.contrib.auth.models import User


class UserViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for n in range(3):
            user = User.objects.create_user(username='user{}'.format(n),
                                            password='password')
            user.save()

        superuser = User.objects.create_superuser(username='superuser',
                                                  password='password')
        superuser.save()

    def setUp(self):
        self.client = Client()

    def test_users_url_exists(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, 200)

    def test_unlogged_users_cannot_see_users(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.json(), [])

    def test_logged_users_see_only_themselves(self):
        self.client.login(username='user1', password='password')
        resp = self.client.get('/users/')
        user_data = resp.json()[0]
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(user_data['username'], 'user1')

    def test_superuser_sees_all_users(self):
        self.client.login(username='superuser', password='password')
        resp = self.client.get('/users/')
        self.assertEqual(len(resp.json()), 4)

    def test_unlogged_users_cant_see_detail_pages(self):
        resp = self.client.get('/users/3/')
        response = resp.json()
        self.assertEqual(response['status'], 'request was permitted')

    def test_logged_users_can_see_them_detail_pages(self):
        self.client.login(username='user1', password='password')
        resp = self.client.get('/users/5/')
        user_data = resp.json()
        self.assertEqual(len(user_data), 3)
        self.assertEqual(user_data["username"], 'user1')

    def test_logged_users_cannot_see_another_detail_pages(self):
        self.client.login(username='user1', password='password')
        resp = self.client.get('/users/6/')
        response = resp.json()
        self.assertEqual(response['status'], 'request was permitted')

    def test_superuser_can_see_all_detail_pages(self):
        self.client.login(username='superuser', password='password')
        resp = self.client.get('/users/5/')
        user_data = resp.json()
        self.assertEqual(len(user_data), 3)
