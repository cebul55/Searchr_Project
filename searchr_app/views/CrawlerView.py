from urllib.parse import urlparse
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI

from searchr_app.models import CrawlItem

scrapyd = ScrapydAPI('https://localhost:6800')


def is_url_valid(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


class CrawlerView(View):

    @csrf_exempt
    @method_decorator(login_required)
    def post(self, request):
        # url that is send from the new search result
        url = request.POST.get('url', None)

        if not url:
            return JsonResponse({'error': 'Missing arguments: URL'})

        if not is_url_valid(url):
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

        # Schedule new crawling task by scrapyd
        # schedule() returns task_id
        task_id = scrapyd.schedule('default',
                                   'link_extractor_crawler',
                                   settings=settings,
                                   url=url,
                                   domain=domain)

        return JsonResponse({
            'task_id': task_id,
            'unique_id': unique_id,
            'status': 'started',
        })

    @csrf_exempt
    @method_decorator(login_required)
    def get(self, request):
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Task_id or unique_id argument is missing.'})

        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                item = CrawlItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dictionary['data']})
            except CrawlItem.DoesNotExist:
                return JsonResponse({'error': 'CrawlItem with secified unique_id' + unique_id + ', does not exist.'})
        else:
            return JsonResponse({'status': status})