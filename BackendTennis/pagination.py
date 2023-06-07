from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def _get_paginated_response(element, data):
    return Response({
        'status': 'success',
        'count': element.page.paginator.count,
        'links': {
            'next': element.get_next_link(),
            'previous': element.get_previous_link()
        },
        'data': data
    })


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = None

    def get_paginated_response(self, data):
        return _get_paginated_response(self, data)


class NewsPagination(CustomPagination):
    page_size = 5


class ImagePagination(CustomPagination):
    page_size = 40


class EventPagination(CustomPagination):
    page_size = 5


class TagPagination(CustomPagination):
    page_size = 100

class TagPagination(CustomPagination):
    page_size = 100

