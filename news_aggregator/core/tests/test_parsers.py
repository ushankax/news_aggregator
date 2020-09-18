from django.test import TestCase
from core.parsers import SiteParser


class HabrParserTest(TestCase):

    def setUp(self):
         self.p = SiteParser('https://habr.com/ru/users/ushankax/favorites/', 'post__title_link')

    def test_get_urls(self):
        self.assertEqual(len(self.p.get_urls()), 41)

    def test_get_title_and_text(self):
        article = self.p.get_urls()[0]
        title, text = self.p.get_title_and_text(article)
        self.assertEqual(title, '\n[Разбор] Инвестиции и спекуляции: в чем на самом деле разница\n')
        self.assertEqual(text[:47], '\nВ нашем блоге мы много пишем о работе на бирже')


