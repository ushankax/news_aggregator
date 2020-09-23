[![Build Status](https://travis-ci.org/ushankax/news_aggregator.svg?branch=master)](https://travis-ci.org/ushankax/news_aggregator)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)

# Новостной агрегатор

Тестовое задание для CASHOFF.


## Инструменты:

1. Django
2. Django REST Framework
3. Celery (+ django_celery_beat)
4. База данных: PostgreSQL
5. Travis CI (автоматическое тестирование)


## Вспомогательные библиотеки:

1. bs4
2. requests


## Как протестировать:

Приложение загружено на Heroku. Ссылка: https://aqueous-plains-72054.herokuapp.com/


## Инструкция:

1. Статьи могут просматривать только зарегистрированные пользователи;
2. Создать учетную запись можно по [ссылке](https://aqueous-plains-72054.herokuapp.com/users/). Для этого нужно отправить запрос с данными "username", "password" и "subscriptions" (доступны "habr" и "vc")
3. Данные учетной записи можно редактировать (например, при желании отредактировать список подписок). Для этого перейдите на страницу своей учетной записи и отправьте patch-запрос с измененными данными
3. После создания учетной записи вы можете [войти](https://aqueous-plains-72054.herokuapp.com/api-auth/login/) и просмотреть список статей по подписке [по ссылке](https://aqueous-plains-72054.herokuapp.com/articles/)
4. Новости загружаются каждые 24 часа, сначала отображаются новые
