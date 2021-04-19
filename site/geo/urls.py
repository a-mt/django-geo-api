from django.urls import path
from . import views

app_name = 'geo'

urlpatterns = [
    path('', views.home, name="homepage"),
    path('communes/', views.commune_create, name="commune_create"),
    path('communes/<slug:code>/', views.commune_edit, name="commune_edit"),
]