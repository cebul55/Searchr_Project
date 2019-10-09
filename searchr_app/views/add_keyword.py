from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import render
from searchr_app.forms import KeywordForm
from searchr_app.views import home


@login_required
def add_keyword(request):
    form = KeywordForm()

    # a HTTP POST?
    if request.method == 'POST':
        form = KeywordForm(request.POST)

        # Have we been provided with a valid form ?
        if form.is_valid():
            # Save new category to the DB
            keyword = form.save(commit=True)
            return home(request)
            # else:
            #     form.add_error('keyword', "Keyword Name value must be uniqe! Capitalization is not verified.")
            #     # print(form.errors)

        else:
            print(form.errors)

    return render(request, 'searchr_app/add_keyword.html', {'form': form})

