import ast
import json
from urllib.parse import urlparse
from uuid import uuid4

import requests
from scrapyd_api import ScrapydAPI
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from searchr_app.models import Search, SearchResult
from searchr_app.views import CrawlerView, crawl

scrapyd = ScrapydAPI('http://localhost:6800')


class RunSearchView(View):

    def post(self, request, search_id):
        try:
            search = Search.objects.get(id=search_id)

            results = self.run_search_query(search.query)
            if results is None:
                return redirect('searchr_app:home')

            # set status running
            search.status = Search._RUNNING
            # set number of running searches
            search.running_results = len(results)
            search.save()

            # do sth with results
            for result in results:
                search_result = SearchResult(
                    title=result['title'],
                    url=result['link'],
                    search=search,
                )
                # todo spider to download file and count hash value
                search_result.save()
                request.POST.url = search_result.url
                response = self.start_spider(search_result.url)
                # get unique_id from new spider
                response_dict = json.loads(response.content)
                search_result.scrapy_unique_task_id = response_dict['unique_id']
                search_result.status = SearchResult._STARTED
                # search_result.html_file = crawl(request)
                # print(json.decoder.JSONDecoder().decode(search_result.html_file))
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

                if 'webPages' in search_results:
                    for result in search_results["webPages"]["value"]:
                        results.append({
                            'title': result['name'],
                            'link': result['url'],
                            'summary': result['snippet'],
                        })
                if 'images' in search_results:
                    for result in search_results["images"]["value"]:
                        results.append({
                            'title': result['name'],
                            'link': result['hostPageUrl'],
                        })
                return results

        except IOError:
            print(IOError)
            print('Query failed')
            return None

    def is_url_valid(self, url):
        validate = URLValidator()
        try:
            validate(url)
            return True
        except ValidationError:
            return False

    def start_spider(self, url):
        # url that is send from the new search result

        # url = request.POST.get('url', None)
        if not url:
            print('dupa')
            return JsonResponse({'error': 'Missing arguments: URL'})

        if not self.is_url_valid(url):
            return JsonResponse({'error': 'URL is not valid'})

        # extract domain from url
        domain = urlparse(url).netloc
        # create unique id to store in helper table in database,
        unique_id = str(uuid4())
        # configuration of settings for scrapy spider
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        print(settings)

        # Schedule new crawling task by scrapyd
        # schedule() returns task_id
        task_id = scrapyd.schedule('default',
                                   'html_file_downloader',
                                   settings=settings,
                                   url=url,
                                   domain=domain)

        return JsonResponse({
            'task_id': task_id,
            'unique_id': unique_id,
            'status': 'started',
        })
