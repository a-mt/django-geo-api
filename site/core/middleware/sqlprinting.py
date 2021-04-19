"""
https://gist.github.com/vstoykov/1390853
"""
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.db import connection

class SQLPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed. This is only useful for debugging.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

        if not settings.DEBUG:
            raise MiddlewareNotUsed

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        if (len(connection.queries) == 0 or
            request.path_info.startswith('/favicon.ico') or
            request.path_info.startswith(settings.STATIC_URL)):
            return response

        indentation = 2
        print("\n\n{indent:s}\033[1;35m[SQL Queries for]\033[1;34m {path:s}\033[0m\n".format(
            indent=" " * indentation,
            path=request.path_info))

        total_time = 0.0
        for query in connection.queries:
            total_time = total_time + float(query['time'])

            print("{indent:s}\033[1;31m[{time:s}]\033[0m {query:s}\n".format(
                indent=" " * indentation,
                time=query['time'],
                query=query['sql'].replace('"', '').replace(',', ', ')))

        print("{indent:s}\033[1;32m[TOTAL TIME: {time:s} seconds ({n:d} queries)]\033[0m".format(
            indent=" " * indentation,
            time=str(total_time),
            n=len(connection.queries)))

        return response