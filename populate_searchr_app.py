import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchr_project.settings')

django.setup()

from searchr_app.models import Keyword, Phrase

# todo update populate script !!!

def populate():

    allegro_key = [
        {'keyword': 'Allegro'},
        {'keyword': 'sklep'},
    ]

    fraza_keywords = [
        {'keyword': 'Bardzo'},
        {'keyword': 'dluga'},
        {'keyword': 'fraza'},
    ]

    phrases = {
        'Allegro and sklep': {'keywords': allegro_key, 'views': 128, },
        'Bardzo dluga fraza': {'keywords': fraza_keywords, 'views': 64, },
    }

    for phrase, phrase_data in phrases.items():
        p = add_phrase(phrase, phrase_data['views'])
        for k in phrase_data['keywords']:
            add_keyword(p, k['keyword'])


def add_phrase(name, views):
    p = Phrase.objects.get_or_create(phrase_name=name)[0]
    p.views = views
    p.save()
    return p


def add_keyword(phrase, name):
    k = Keyword.objects.get_or_create(phrase=phrase, keyword=name)[0]
    k.save()
    return k


# Start execution here !
if __name__ == '__main__':
    print("Starting SearchR population script ... ")
    populate()
