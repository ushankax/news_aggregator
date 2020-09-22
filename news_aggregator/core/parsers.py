import requests
from bs4 import BeautifulSoup
import re
import logging
from .models import Article


logger = logging.getLogger(__name__)


class SiteParser:
    """base class for parsing news from sites like habr, vc"""

    def __init__(self, url, title_class, body_class):
        self.url = url
        self.title_class = title_class
        self.body_class = body_class

    def get_article_urls(self) -> list:
        """return full list of links from all pages"""
        flag = True

        try:
            r = requests.get(self.url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)

        while flag:
            soup = BeautifulSoup(r.text, 'lxml')

            for link in soup.find_all('a', class_=self.title_class):
                yield link.get('href')

            next_page = None

            for a in soup.find_all('a', id='next_page'):
                next_page = a['href']

            if next_page:
                try:
                    r = requests.get("{}{}".format(self.url[:16], next_page))
                    r.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    logger.error(err)

                next_page = None
            else:
                flag = False

    def get_title_and_text(self, article) -> tuple:
        """return title and text from the article"""
        try:
            r = requests.get(article)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)

        soup = BeautifulSoup(r.text, 'lxml')

        h1 = soup.h1.get_text()
        title = h1.strip()

        raw_text = soup.find('div', class_=self.body_class).get_text()
        text = re.sub('\n', '', raw_text)
        text = re.sub('\r', '', text)
        return title, text


class HabrParser(SiteParser):
    """class based on SiteParser adapted for parsing from habr.com"""

    def __init__(self):
        self.url = 'https://habr.com/ru/top/'
        self.title_class = 'post__title_link'
        self.body_class = 'post__body post__body_full'
        self.source = 'habr'


class VCParser(SiteParser):
    """class based on SiteParser adapted for parsing from vc.ru"""

    def __init__(self):
        self.url = 'https://vc.ru/'
        self.title_class = 'content-feed__link'
        self.body_class = 'content content--full'
        self.source = 'vc'

    def get_title_and_text(self, article) -> tuple:
        """vc articles sometimes haven't titles and can have redaction mark"""
        try:
            r = requests.get(article)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)

        soup = BeautifulSoup(r.text, 'lxml')

        if soup.h1:
            h1 = soup.h1
            title_raw = h1.get_text()
            title = re.sub('\n\n\nМатериал редакции', '', title_raw)
        else:
            title = "No Title"

        text = ''

        for div in soup.find_all('div', class_=self.body_class):
            for p in div('p'):
                text += p.get_text()

        return title.strip(), text


def get_news_from_site(site):
    """template which load news to postgres from single site"""
    article_links = site.get_article_urls()

    for link in article_links:
        if Article.objects.filter(link=link):
            pass
        else:
            title_and_text = site.get_title_and_text(link)
            title, text = title_and_text

            article = Article.objects.create(source=site.source,
                                             title=title,
                                             link=link,
                                             text=text)
