import pytest
import json
from api.utils import get_paginated_nested_serializer
from api.serializers import CommentSerializer
from todo.models import ToDo
from django.core.paginator import Paginator
from pytest_django.asserts import assertURLEqual
from rest_framework.utils.urls import replace_query_param


@pytest.mark.django_db
def test_nested_paginator(api_client, api_request_factory, load_big_fixtures):
    # make paginated response
    response = api_client.get("/api/todo/98/?page=2&page_size=50&test=40")
    data = response.data

    request = api_request_factory.get("/api/todo/98/?page=2&page_size=50&test=40")
    query_set = ToDo.objects.filter(id=98).first().comments_in.all()
    paginator = Paginator(query_set, 50)
    paginated_query_set_v2 = paginator.page(2)
    paginated_data_v2 = CommentSerializer(
        instance=paginated_query_set_v2, many=True, context={"request": request}
    ).data
    assert paginated_data_v2 == data["comments"]["results"]
    assertURLEqual(
        data["comments"]["next"],
        replace_query_param(request.build_absolute_uri(), 'page', 3),
    )
    assert data['comments']['count'] == query_set.count()
    assertURLEqual(
        data["comments"]["previous"],
        replace_query_param(request.build_absolute_uri(), 'page', 1),
    )

@pytest.mark.django_db
def test_query_param_nested_paginator(api_client, load_fixtures):
    response = api_client.get('/api/todo/98/?page=bad_para&page_size=bad_para')
    assert response.data['comments']['detail'] == 'Size bad_para is not integer'
    response = api_client.get('/api/todo/98/?page=20&page_size=bad_para')
    assert response.data['comments']['detail'] == 'Size bad_para is not integer'
    response = api_client.get('/api/todo/98/?page=bad_para&page_size=20')
    assert response.data['comments']['detail'] == 'That page number is not an integer'
    response = api_client.get('/api/todo/98/?page=last&page_size=20')
    assert response.data["comments"]["previous"] == ''

@pytest.mark.django_db
def test_query_param_page_too_big(api_client, load_fixtures):
    response = api_client.get('/api/todo/98/?page=454564654168&page_size=20')
    assert response.data["comments"]['detail'] == 'That page contains no results'

