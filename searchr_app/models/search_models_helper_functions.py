from django.utils import timezone

from searchr_app.models import SearchHistory


def create_search_history_item(search, query,username):
    """
    Method creates new history item, when search is created
    :return: search_history object
    """
    print(query)
    search_history = SearchHistory(
        username=username,
        date_searched=timezone.now(),
        query_value=query,
        number_of_results=0,
        search=search,
    )
    search_history.save()
    return search_history

def add_result_to_history(search, search_result):
    search_history = SearchHistory.objects.get(search=search)
    search_history.search_results.add(search_result)
    search_history.number_of_results = search_history.search_results.all().count()
    search_history.save()
