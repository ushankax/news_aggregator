web: gunicorn --pythonpath news_aggregator news_aggregator.wsgi
worker: cd news_aggregator && celery -A news_aggregator worker --beat --scheduler django --loglevel=info
