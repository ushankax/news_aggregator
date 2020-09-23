web: gunicorn --pythonpath news_aggregator news_aggregator.wsgi
worker: celery -A news_aggregator worker --beat --scheduler django --loglevel=info
