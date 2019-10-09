import json
import requests

from searchr_project.read_key import read_bing_key


def run_query(search_terms):
    # Microsoft documentation: http://bit.ly/twd-bing-api

    bing_key = read_bing_key()
    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
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
