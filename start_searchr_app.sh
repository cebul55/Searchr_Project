#!/usr/bin/env bash
workon searchrENV
python manage.py runserver &
#echo 'successfully started django runserver.'
cd scrapy_4_searchr_app/
scrapyd && fg
#echo 'successfully started scrapyd.'
