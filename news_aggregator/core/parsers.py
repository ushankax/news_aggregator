import requests
from bs4 import BeautifulSoup


class SiteParser:
    """Class-template for parsing news from sites like habr, vc"""

    def __init__(self, url, title_class, body_class):
        self.url = url
        self.title_class = title_class
        self.body_class = body_class

    def get_urls(self) -> list:
        """Return full list of links from all pages"""
        flag = True
        r = requests.get(self.url)
        link_list = []

        while flag:
            soup = BeautifulSoup(r.text, 'lxml')

            for link in soup.find_all('a', class_=self.title_class):
                link_list.append(link.get('href'))

            next_page = None

            for a in soup.find_all('a', id='next_page'):
                next_page = a['href']

            if next_page:
                r = requests.get("{}{}".format(self.url[:16], next_page))
                next_page = None
            else:
                flag = False

        return link_list

    def get_title_and_text(self, article) -> tuple:
        """Return title and text from the article"""
        r = requests.get(article)
        soup = BeautifulSoup(r.text, 'lxml')

        h1 = soup.h1.get_text()
        title = h1.strip()
        text = soup.find('div', class_=self.body_class).get_text()

        return title, text


class HabrParser(SiteParser):
    """Class based on SiteParser adapted for parsing from habr.com"""

    def __init__(self):
        self.url = 'https://habr.com/ru/top/'
        self.title_class = 'post__title_link'
        self.body_class = 'post__body post__body_full'


class VCParser(SiteParser):
    """Class based on SitiParser adapted for parsing from vc.ru"""

    def __init__(self):
        self.url = 'https://vc.ru/'
        self.title_class = 'content-feed__link'
        self.body_class = 'content content--full'

    def get_title_and_text(self, article) -> tuple:
        r = requests.get(article)
        soup = BeautifulSoup(r.text, 'lxml')

        h1 = soup.h1
        h1.a.extract()
        title = h1.get_text()

        text = ''

        for div in soup.find_all('div', class_=self.body_class):
            for p in div('p'):
                text += "\n{}".format(p.get_text())

        return title.strip(), text

