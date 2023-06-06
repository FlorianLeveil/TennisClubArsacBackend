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


class NewsPagination(PageNumberPagination):
    page_size = 2  # Nombre d'éléments par page
    page_size_query_param = 'page_size'
    max_page_size = None

    def get_paginated_response(self, data):
        return _get_paginated_response(self, data)


class ImagePagination(PageNumberPagination):
    page_size = 30  # Nombre d'éléments par page
    page_size_query_param = 'page_size'
    max_page_size = None

    def get_paginated_response(self, data):
        return _get_paginated_response(self, data)


class EventPagination(PageNumberPagination):
    page_size = 1  # Nombre d'éléments par page
    page_size_query_param = 'page_size'
    max_page_size = None

    def get_paginated_response(self, data):
        return _get_paginated_response(self, data)
