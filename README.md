# SEARCH PROJECT

## Project implemented for purposes of writing Engineer's Thesis on Warsaw University of Technology

author: B.Cybulski 

## 1. Basic environment configuration:
Can be found in file requirements.txt(or requirements_windows.txt for Windows users). It is recommended to work on virtualenvironment.

## 2. Technology Stack
- Programming language: Python
- Framework: Django and Scrapy
- IDE: PyCharm
- Database: PostgreSQL
- Search engine: Bing Search
- Online code repository: GitHub
- Framework CSS: Bootstrap
- For displaying HTML code: [Google prettyprint](https://github.com/google/code-prettify)
- Apache-Tika
- BeautifulSoup library

## 3. Set up project on local machine
- Install all necessary libraries
- Configure virtual environment
- set up postgreSQL database using script in file **create_database.sql**
- generate secret_key for Django by running:
```python
from django,core.management.utils import get_random_secret_key
get_random_secret_key()
```
and save it in file **/searchr_project/conf/secret.key**
- set up Bing Search API on [Azure](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/web-sdk-python-quickstart) and save secret key in file **/searchr_project/conf/bing.key**
- save password for admin psql user in file **/searchr_project/conf/searchrDB.key**
- next step is to migrate database structure. Run following commands in project root folder (where *manage.py* file is stored):
```python
python manage.py migrate
python manage.py makiemigraitons
```
- Create super user
```python
python manage.py createsuperuser
```
## 4. Run project
In order to run project on localhost, you have to start django server as well as scrapy server. Run following command to start django server:
```
python manage.py runserver
```
To start scrapy server go to *scrapy_4_searchr_app* folder and execute command:
```
scrapyd
```
That will start django server on localhost:8000 and scrapy server on localhost:6800

## 4.1 Enter application
Go to url: [http://localhost:8000/](http://localhost:8000/)