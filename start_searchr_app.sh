#!/usr/bin/env bash
workon searchENV
python manage.py runserver &
cd scrapy_4_searchr_app/
scrapyd && fg
