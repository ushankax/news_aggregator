from news_aggregator.celery import app
import json
from . import parsers
from .models import Article


@app.task()
def import_latest_news():
    """upload unique articles from sites in database"""
    vc = parsers.VCParser()
    vc_links = vc.get_urls()

    for link in vc_links:
        if Article.objects.filter(link=link):
            pass
        else:
            title_and_text = vc.get_title_and_text(link)
            title, text = title_and_text

            article = Article.objects.create(source='vc',
                                             title=title,
                                             link=link,
                                             text=text,
                                             text_preview=text[:700])
            print(article)

    habr = parsers.HabrParser()
    habr_links = habr.get_urls()

    for link in habr_links:
        if Article.objects.filter(link=link):
            pass
        else:
            title_and_text = habr.get_title_and_text(link)
            title, text = title_and_text

            article = Article.objects.create(source='habr',
                                             title=title,
                                             link=link,
                                             text=text,
                                             text_preview=text[:700])
            print(article)

    return json.dumps({"status": True})
