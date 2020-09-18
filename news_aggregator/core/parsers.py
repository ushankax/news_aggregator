import requests
from bs4 import BeautifulSoup


class SiteParser:

    def __init__(self, url, title_class):
        self.url = url
        self.title_class = title_class
        self.link_list = []

    def get_urls(self) -> list:
        """Return full list of links from all pages"""
        flag = True
        r = requests.get(self.url)

        while flag:
            soup = BeautifulSoup(r.text, 'lxml')

            for link in soup.find_all('a', class_=self.title_class):
                self.link_list.append(link.get('href'))

            next_page = None

            for a in soup.find_all('a', id='next_page'):
                next_page = a['href']

            if next_page:
                r = requests.get("{}{}".format(self.url[:16], next_page))
                next_page = None
            else:
                flag = False

        return self.link_list

    def get_title_and_text(self, article) -> tuple:
        """Return title and text from the article"""
        r = requests.get(article)
        soup = BeautifulSoup(r.text, 'lxml')
        return (soup.h1.get_text(),
                soup.find('div', class_="post__body post__body_full").get_text())

