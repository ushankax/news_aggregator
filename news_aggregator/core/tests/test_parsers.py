from django.test import TestCase
from core.parsers import SiteParser, VCParser, HabrParser
import re


class SiteParserTest(TestCase):
    """This TestCase is also work to HabrParser for its similarity"""

    def setUp(self):
         self.p = SiteParser('https://habr.com/ru/users/ushankax/favorites/',
                             'post__title_link',
                             'post__body post__body_full')

    def test_get_urls(self):
        self.assertEqual(len(self.p.get_urls()), 41)

    def test_get_title_and_text(self):
        article = self.p.get_urls()[0]
        title, text = self.p.get_title_and_text(article)
        self.assertEqual(title, '[Разбор] Инвестиции и спекуляции: в чем на самом деле разница')
        self.assertEqual(text[:46], 'В нашем блоге мы много пишем о работе на бирже')


class VCParserTest(TestCase):

    def setUp(self):
        self.p = VCParser()
        self.no_title_article = 'https://vc.ru/flood/159719'
        self.article = 'https://vc.ru/transport/159612-avtopilot-tesla-sbezhal-ot-policii-v-kanade-voditel-usnul-i-mashina-uhodila-ot-pogoni-sama'

    def test_get_urls(self):
        self.assertEqual(len(self.p.get_urls()), 12)

    def test_get_title_and_text(self):
        title, text = self.p.get_title_and_text(self.article)
        self.assertEqual(title, 'Автопилот Tesla сбежал от полиции в Канаде: водитель уснул и машина уходила от погони сама')
        self.assertEqual(text[:24], 'Владельца машины обвинил')

    def test_article_has_no_title(self):
        title, text = self.p.get_title_and_text(self.no_title_article)
        self.assertEqual(title, 'No Title')


class HabrParserTest(TestCase):

    def setUp(self):
        self.p = HabrParser()

    def test_url_is_correct(self):
        self.assertEqual(self.p.url, 'https://habr.com/ru/top/')

    def test_article_text_is_clear(self):
        article = 'https://habr.com/ru/company/ruvds/blog/519884/'
        title, text = self.p.get_title_and_text(article)
        self.assertIsNone(re.search('\n', text))

