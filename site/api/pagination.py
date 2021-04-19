from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class PagesizePagination(PageNumberPagination):
    def get_paginated_response(self, data):

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('per_page', self.page.paginator.per_page),
            ('num_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_paginated_response_schema(self, schema):
        res = super().get_paginated_response_schema(schema)

        res['properties']['page'] = {
            'type': 'integer',
            'example': 3
        }
        res['properties']['per_page'] = {
            'type': 'integer',
            'example': 30
        }
        res['properties']['num_pages'] = {
            'type': 'integer',
            'example': 5
        }
        return res