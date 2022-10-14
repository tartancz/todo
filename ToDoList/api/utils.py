from django.core.paginator import InvalidPage, Paginator
from rest_framework.reverse import reverse
from rest_framework.utils.urls import replace_query_param
from rest_framework.response import Response


def get_paginated_nested_serializer(
    request,
    serializer_class,
    query_set,
    page_size=10,
    page_kwarg="page",
    size_kwarg="page_size",
):
    if request.query_params.get(size_kwarg):
        page_size = request.query_params.get(size_kwarg)
        try:
            page_size = int(page_size)
        except (TypeError, ValueError):
            return {"detail": f"Size {page_size} is not integer"}

    paginator = Paginator(query_set, page_size)
    page = request.query_params.get(page_kwarg) or 1

    try:
        page = paginator.validate_number(page)
    except InvalidPage as e:
        if page == "last":
            page = paginator.num_pages
        else:
            return {"detail": f"{e}"}


    queryset_paginated = paginator.page(page)
    comments = serializer_class(
        instance=queryset_paginated, many=True, context={"request": request}
    ).data
    next = ""
    url = request.build_absolute_uri()
    if queryset_paginated.has_next():
        next = replace_query_param(url, page_kwarg, queryset_paginated.next_page_number())
    previous = ""
    if queryset_paginated.has_previous():
        previous = replace_query_param(url, page_kwarg, queryset_paginated.previous_page_number())
    context = {
        "count": query_set.count(),
        "next": next,
        "previous": previous,
        "results": comments,
    }
    return context
