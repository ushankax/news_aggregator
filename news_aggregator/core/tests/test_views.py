from django.test import TestCase, Client
from core.views import ArticleViewSet
from django.contrib.auth.models import User
from accounts.models import Profile
from core.models import Article
from core.parsers import HabrParser


class ArticleViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create users with different subscriptions; create test articles"""

        habr_user = User.objects.create_user(username='habr_user',
                                             password='password')
        Profile.objects.create(user=habr_user, subscriptions=['habr'])

        vc_user = User.objects.create_user(username='vc_user',
                                           password='password')
        Profile.objects.create(user=vc_user, subscriptions=['vc'])

        mega_user = User.objects.create_user(username='mega_user',
                                             password='password')
        Profile.objects.create(user=mega_user,
                               subscriptions=['vc', 'habr'])

        test_habr_article = 'https://habr.com/ru/post/519886/'
        habr_parser = HabrParser()
        title, text = habr_parser.get_title_and_text(test_habr_article)

        for _ in range(3):
            Article.objects.create(source='habr', title=title, text=text)

        for _ in range(2):
            Article.objects.create(source='vc',
                                   title='vctitle',
                                   text='vctext')

    def setUp(self):
        self.client = Client()

    def test_view_url_exists(self):
        self.client.login(username='habr_user', password='password')
        resp = self.client.get('/articles/')
        self.assertEqual(resp.status_code, 200)

    def test_articles_doesnt_work_for_guests(self):
        resp = self.client.get('/articles/')
        self.assertEqual(resp.status_code, 403)

    def test_user_gets_correct_news_by_subscription(self):
        self.client.login(username='habr_user', password='password')
        resp = self.client.get('/articles/')

        self.assertEqual(resp.resolver_match.func.__name__,
                         ArticleViewSet.as_view({'get': 'list'}).__name__)
        self.assertEqual(len(resp.json()['results']), 3)

    def test_listing_text_is_preview(self):
        """check that 'text' field in listing less than 700 characters"""
        self.client.login(username='habr_user', password='password')
        resp = self.client.get('/articles/')

        test_article = resp.json()['results'][0]
        self.assertLess(len(test_article['text']), 702)

    def test_detail_text_is_full(self):
        """check that 'text' field in detail view is full"""
        self.client.login(username='habr_user', password='password')
        resp = self.client.get('/articles/2/')
        test_article = resp.json()['text']
        self.assertGreater(len(test_article), 700)
