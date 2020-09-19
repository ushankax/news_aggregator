from django.test import TestCase
from core.parsers import SiteParser, VCParser


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
        self.assertEqual(text[:47], '\nВ нашем блоге мы много пишем о работе на бирже')


class VCParserTest(TestCase):

    def setUp(self):
        self.p = VCParser()
        self.article = 'https://vc.ru/transport/159612-avtopilot-tesla-sbezhal-ot-policii-v-kanade-voditel-usnul-i-mashina-uhodila-ot-pogoni-sama'

    def test_get_urls(self):
        self.assertEqual(len(self.p.get_urls()), 12)

    def test_get_title_and_text(self):
        title, text = self.p.get_title_and_text(self.article)
        self.assertEqual(title, 'Автопилот Tesla сбежал от полиции в Канаде: водитель уснул и машина уходила от погони сама')
        self.assertEqual(text[:25], '\nВладельца машины обвинил')

