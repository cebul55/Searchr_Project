START /B workon newENV
START /B python manage.py runserver
echo "successfully started django runserver."
cd scrapy_4_searchr_app/
START /B scrapyd
echo "successfully started scrapyd."