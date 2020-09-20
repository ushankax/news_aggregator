from news_aggregator.celery import app
from .models import Article
import json


@app.task()
def test():
    Article.objects.create(source='source',
                                     title='title',
                                     link='https://vc.ru/',
                                     text='text',
                                     text_preview='preview',
                                    )

    return json.dumps({"status": True})
