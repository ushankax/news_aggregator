run:
	python3 manage.py runserver

coverage:
	coverage run --source='.' manage.py test ;\
	coverage report

celery:
	celery -A news_aggregator worker --beat --scheduler django --loglevel=info

redis:
	redis-server
