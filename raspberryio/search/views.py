from django.shortcuts import render
from django.db.models import get_model

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

from raspberryio.search.models import Searchable, searchable_models


def search(request):
    """
    Display search results. Takes an optional 'type' GET parameter
    in the form 'app-name.ModelName' to limit search results to a single model.
    """
    settings.use_editable()
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    # Determine query to make
    use_everything = False
    try:
        raw_type_query = request.GET.get("type", "")
        type_query = raw_type_query.split(".", 1)
        if not raw_type_query in settings.SEARCH_MODEL_CHOICES:
            raise TypeError
        search_model = get_model(*type_query)
    except TypeError:
        use_everything = True
    else:
        search_type = search_model._meta.verbose_name_plural.capitalize()
        # Swap the model out for its Searchable proxy model for making queries
        for proxy_model in searchable_models:
            if search_model in proxy_model.__bases__:
                search_model = proxy_model
                use_everything = False
                break
    # type was given, but a Searchable proxy model could not be found. Search
    # on all types.
    if use_everything:
        search_model = Searchable
        search_type = "Everything"
    results = search_model.objects.search(query, for_user=request.user)
    results = [
        result for result in results
        if getattr(result, 'is_published', lambda: True)()
    ]
    # paginate the results
    per_page = settings.SEARCH_PER_PAGE
    max_paging_links = settings.MAX_PAGING_LINKS
    paginated_results = paginate(results, page, per_page, max_paging_links)
    return render(request, 'search/search_results.html', {
        "query": query,
        "results": paginated_results,
        "search_type": search_type
    })
