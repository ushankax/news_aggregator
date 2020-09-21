from django.test import TestCase
from core.models import Article


class ArticleModelTestCase(TestCase):

    def setUp(self):
        self.article = Article.objects.create(source='habr',
                                              title='Непобедимый',
                                              text='text',
                                              link='https://habr.com/ru/post/519886/'
                                             )

    def test_str_is_correct(self):
        self.assertEqual(str(self.article), "'Непобедимый' from habr")

