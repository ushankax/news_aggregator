from celery import shared_task
import json
from . import parsers
import logging


logger = logging.getLogger(__name__)


@shared_task
def get_daily_news():
    """upload unique articles from sites to database"""
    vc = parsers.VCParser()
    habr = parsers.HabrParser()

    parsers.get_news_from_site(vc)
    parsers.get_news_from_site(habr)

    logger.info('success news loaded')
    return json.dumps({"status": True})
