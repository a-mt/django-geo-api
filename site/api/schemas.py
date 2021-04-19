from rest_framework.schemas import AutoSchema
from rest_framework.schemas.utils import is_list_view
from rest_framework.compat import coreapi, coreschema

class CommuneViewSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        if is_list_view(path, method, self.view) and method.lower() == "get":
            return [
                coreapi.Field(
                    name="q",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        title='Query',
                        description='A city name or zip code.'
                    ))
            ]
        return []