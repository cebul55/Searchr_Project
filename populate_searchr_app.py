import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchr_project.settings')

django.setup()

from searchr_app.models import Keyword, SearchResult

# todo update populate script !!!

def populate():

    allegro_results = [
        {'title': 'Allegro', 'url': 'https://google.com', 'views': 9},
        {'title': 'Allegro - portal aukcyjny', 'url': 'https://google.com', 'views': 18},
    ]

    python_results = [
        {'title': 'Python', 'url': 'https://google.com', 'views': 32},
        {'title': 'Python tutorial', 'url': 'https://google.com', 'views': 128},
    ]

    keywords = {
        'Allegroo': {'results': allegro_results},
        'Pythonn': {'results': python_results},
    }

    for keyword, keyword_data in keywords.items():
        k = add_keyword(keyword)
        for s in keyword_data['results']:
            add_search_result(k, s['title'], s['url'], s['views'])


def add_keyword(name):
    k = Keyword.objects.get_or_create(keyword=name)[0]
    k.save()
    return k


def add_search_result(keyword, title, url, views):
    search_result = SearchResult.objects.get_or_create(keyword=keyword, search_result_title=title)[0]
    search_result.url = url
    search_result.views = views
    search_result.save()
    return search_result


# Start execution here !
if __name__ == '__main__':
    print("Starting SearchR population script ... ")
    populate()
