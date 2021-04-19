from rest_framework import viewsets
from geo.models import Region, Departement, Commune, CodePostal
from . import serializers, schemas

from django.db.models.aggregates import Count
from django.db.models import Q
from django.db.models.query import QuerySet

class RegionViewSet(viewsets.ModelViewSet):
    queryset          = Region.objects.all()
    serializer_class  = serializers.RegionSerializer
    http_method_names = ['get', 'head', 'options']

class DepartementViewSet(viewsets.ModelViewSet):
    queryset          = Departement.objects.all().select_related('region')
    serializer_class  = serializers.DepartementSerializer
    http_method_names = ['get', 'head', 'options']

class CommuneViewSet(viewsets.ModelViewSet):
    queryset          = Commune.objects.all() \
                               .select_related('departement', 'departement__region') \
                               .prefetch_related('codepostal_set')
    serializer_class  = serializers.CommuneSerializer

    # Add q parameter to schema (for doc)
    schema            = schemas.CommuneViewSchema()

    def get_queryset(self):
        q = self.request.query_params.get('q')

        if q:
            if q.isnumeric():
                return self.queryset.filter(codepostal__code=q)
            else:
                return self.queryset.filter(nom_norm__contains=Commune.normalize(q))

        return self.queryset
