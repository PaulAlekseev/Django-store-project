from .forms import SearchForm


def search_form(request):

    search_for = request.GET.get('search_form')
    return {'search_form': SearchForm(
        initial={'search_for': search_for or ''}
        )}
