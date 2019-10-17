from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import KeywordForm


class AddKeywordView(View):
    form = KeywordForm()

    @method_decorator(login_required)
    def get(self, request):

        return render(request, 'searchr_app/add_keyword.html', {'form': self.form})

    @method_decorator(login_required)
    def post(self, request):
        self.form = KeywordForm(request.POST)

        # Have we been provided with a valid form ?
        if self.form.is_valid():
            # Save new Keyword to the DB
            keyword = self.form.save(commit=True)
            return redirect('searchr_app:home')

        else:
            print(self.form.errors)

        return render(request, 'searchr_app/add_keyword.html', {'form': self.form})

