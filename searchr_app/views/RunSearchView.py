import ast

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from searchr_app.models import Search, SearchResult


class RunSearchView(View):

    def get(self, request, search_id):
        try:
            search = Search.objects.get(id=search_id)
            results = self.run_search_query(search.query)
            if results == None:
                return redirect('searchr_app:home')

            # do sth with results
            for result in results:
                search_result = SearchResult(
                    title=result['title'],
                    url=result['link'],
                    search=search,
                )
                # todo spider to download file and count hash value
                search_result.save()
            return redirect('searchr_app:show_search', request.user.username, search.project.slug, search.slug)
        except Search.DoesNotExist:
            return redirect('searchr_app:home')

    def run_search_query(self, query):
        try:
            # issue the request, given the details aboce
            dict = {}
            dict = ast.literal_eval(query)
            response = requests.get(dict['search_url'], headers=dict['headers'], params=dict['params'])

            response.raise_for_status()

            if response.status_code == 200:
                search_results = response.json()
                print(response.json())
                results = []
                for result in search_results["webPages"]["value"]:
                    results.append({
                        'title': result['name'],
                        'link': result['url'],
                        'summary': result['snippet'],
                    })
                return results

        except IOError:
            print(IOError)
            print('Query failed')
            return None
