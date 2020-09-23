from django.test import TestCase
from core.parsers import SiteParser, VCParser, HabrParser, get_news_from_site
import re
from core.models import Article


class SiteParserTest(TestCase):
    """This TestCase is also work to HabrParser for its similarity"""

    def setUp(self):
        self.p = SiteParser('https://habr.com/ru/users/ushankax/favorites/',
                            'post__title_link',
                            'post__body post__body_full')

    def test_get_article_urls(self):
        self.assertEqual(len(list(self.p.get_article_urls())), 41)

    def test_get_title_and_text(self):
        article = list(self.p.get_article_urls())[0]
        title, text = self.p.get_title_and_text(article)
        expect = '[Разбор] Инвестиции и спекуляции:'\
                 ' в чем на самом деле разница'
        self.assertEqual(title, expect)
        self.assertEqual(text[:46],
                         'В нашем блоге мы много пишем о работе на бирже')


class VCParserTest(TestCase):

    def setUp(self):
        self.p = VCParser()
        self.no_title_article = 'https://vc.ru/flood/159719'
        self.article = 'https://vc.ru/transport/159612-avtopilot'\
                       '-tesla-sbezhal-ot-policii-v-kanade-voditel'\
                       '-usnul-i-mashina-uhodila-ot-pogoni-sama'

    def test_get_urls(self):
        self.assertGreater(len(list(self.p.get_article_urls())), 11)

    def test_get_title_and_text(self):
        title, text = self.p.get_title_and_text(self.article)
        expect = 'Автопилот Tesla сбежал от полиции в Канаде: водитель уснул'\
                 ' и машина уходила от погони сама'
        self.assertEqual(title, expect)
        self.assertEqual(text[:24], 'Владельца машины обвинил')

    def test_article_has_no_title(self):
        title, text = self.p.get_title_and_text(self.no_title_article)
        self.assertEqual(title, 'No Title')

    def test_get_news_from_vc(self):
        get_news_from_site(self.p)
        vc_articles_count = Article.objects.filter(source='vc').count()
        vc_distinct_articles_count = Article.objects.filter(source='vc') \
                                                    .distinct().count()
        self.assertGreater(vc_articles_count, 11)
        get_news_from_site(self.p)
        self.assertEqual(vc_articles_count, vc_distinct_articles_count)


class HabrParserTest(TestCase):

    def setUp(self):
        self.p = HabrParser()

    def test_url_is_correct(self):
        self.assertEqual(self.p.url, 'https://habr.com/ru/top/')

    def test_article_text_is_clear(self):
        article = 'https://habr.com/ru/company/ruvds/blog/519884/'
        title, text = self.p.get_title_and_text(article)
        self.assertIsNone(re.search('\n', text))

    def test_get_news_from_habr(self):
        get_news_from_site(self.p)
        habr_articles_count = Article.objects.filter(source='habr').count()
        habr_distinct_articles_count = Article.objects.filter(source='habr') \
                                                      .distinct().count()
        self.assertGreater(habr_articles_count, 20)
        get_news_from_site(self.p)
        self.assertEqual(habr_articles_count, habr_distinct_articles_count)
