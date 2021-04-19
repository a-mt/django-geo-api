from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'regions', views.RegionViewSet)
router.register(r'departements', views.DepartementViewSet)
router.register(r'communes', views.CommuneViewSet)

urlpatterns  = router.urls
urlpatterns += [
    path('schema', get_schema_view(title='Geo API', version=1)),
    path('docs', get_swagger_view(title='Geo API'), name='docs')
]