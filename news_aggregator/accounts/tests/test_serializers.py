from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import Profile


class UserSerializerTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.serializer_data = {
            'username': 'new_user',
            'password': 'password',
            'subscriptions': ['habr']
        }

        self.serializer_patch_data = {
            'username': 'new_user777',
            'subscriptions': ['vc']
        }

        self.user = User.objects.create_user(username='patch_user',
                                             password='password')
        self.profile = Profile.objects.create(user=self.user,
                                              subscriptions=['habr'])
        self.user.save()
        self.profile.save()

    def test_user_profile_was_created(self):
        resp = self.client.post('/users/', self.serializer_data)
        self.assertEqual(resp.status_code, 201)

        self.client.login(username='new_user', password='password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.profile.subscriptions, ['habr'])

    def test_user_can_update_your_profile(self):
        self.client.login(username='patch_user', password='password')
        resp = self.client.patch('/users/1/',
                                 self.serializer_patch_data,
                                 content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'new_user777')
