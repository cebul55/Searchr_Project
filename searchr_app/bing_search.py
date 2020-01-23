import json
import requests

from searchr_app.models import Search, Phrase
from searchr_project.read_key import read_bing_key


def create_search_terms(phrases):
    search_terms = ''
    for p in phrases:
        if search_terms == '':
            search_terms = search_terms + '\"' + p.value + '\" '
        else:
            search_terms = search_terms + '&& \"' + p.value + '\" '

    return search_terms


def create_bing_search_query(search, phrases, number_of_results, offset, language):
    bing_key = read_bing_key()
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    headers = {"User-Agent": user_agent,
                "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                "Connection": 'keep-alive',

               "Ocp-Apim-Subscription-Key": bing_key,
               "Pragma": "no-cache"}
    params = {"q": create_search_terms(phrases),
              "textDecorations": "True",
              "textFormat": "HTML",
              "setLang": language,
              "count": number_of_results,
              "offset": offset}
    query = {
        "search_url": search_url,
        "headers": headers,
        "params": params
    }
    return query

def update_bing_search_query(query, phrases_query):
    query['params']['q'] = phrases_query
    print(query)
    return query


def run_query(search_terms):
    # Microsoft documentation: http://bit.ly/twd-bing-api

    bing_key = read_bing_key()
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": search_terms, "textDecorations": True, "textFormat": "HTML"}

    # issue the request, given the details aboce
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results["webPages"]["value"]:
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet'],
        })

    return results


def raw_input():
    print("insert your query:")
    return input()


def main():
    search_terms = raw_input()
    results = run_query(search_terms)
    for r in results:
        print(r)


if __name__ == 'main':
    main()
