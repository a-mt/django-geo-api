from django.contrib import admin
from . import models

admin.site.register(models.Region)
admin.site.register(models.Departement)

@admin.register(models.Commune)
class CommuneAdmin(admin.ModelAdmin):
    readonly_fields = ['nom_norm']

@admin.register(models.CodePostal)
class CodePostalAdmin(admin.ModelAdmin):
    list_display  = ['code', 'commune_id']
    search_fields = ['code']