from django.shortcuts import render
from django.db.models import get_model

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

from raspberryio.search.models import Searchable


def search(request):
    """
    Display search results. Takes an optional 'type' GET parameter
    in the form 'app-name.ModelName' to limit search results to a single model.
    """
    settings.use_editable()
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    # Determine query to make
    try:
        search_model = get_model(*request.GET.get("type", "").split(".", 1))
        if not issubclass(search_model, Searchable):
            raise TypeError
    except TypeError:
        search_model = Searchable
        search_type = "Everything"
    else:
        search_type = search_model._meta.verbose_name_plural.capitalize()
    results = search_model.objects.search(query, for_user=request.user)
    # paginate the results
    per_page = settings.SEARCH_PER_PAGE
    max_paging_links = settings.MAX_PAGING_LINKS
    paginated_results = paginate(results, page, per_page, max_paging_links)
    return render(request, 'search/search_results.html', {
        "query": query,
        "results": paginated_results,
        "search_type": search_type
    })
