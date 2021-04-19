from rest_framework import serializers
from .fields import InputCommaSeparatedField
from geo.models import Region, Departement, Commune, CodePostal

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Region
        fields = ('code', 'nom')

class DepartementSerializer(serializers.ModelSerializer):
    region       = RegionSerializer(read_only=True)
    codeRegion   = serializers.StringRelatedField(source='region.code')

    class Meta:
        model  = Departement
        fields = ('code', 'nom', 'codeRegion', 'region')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        # Remove fields we don't select
        if fields:
            for field_name in self.fields.keys() - fields:
                self.fields.pop(field_name)

class CodePostalStringSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CodePostal
        fields = ('code',)

    def to_representation(self, instance):
        return str(instance)

    def to_internal_value(self, value):
        # ModelSerializer validates the values 
        return super().to_internal_value({'code': value})

class CommuneSerializer(serializers.ModelSerializer):
    codeDepartement = serializers.SlugRelatedField(
                        allow_null=True,
                        queryset=Departement.objects.all(),
                        source='departement',
                        slug_field='code',
                        label='Code département')

    codesPostaux    = InputCommaSeparatedField(
                        child_relation=CodePostalStringSerializer(),
                        source='codepostal_set',
                        label='Codes postaux',
                        help_text='Liste séparée par des virgules')

    departement     = DepartementSerializer(
                        read_only=True,
                        fields=['code', 'nom'])

    region          = RegionSerializer(
                        read_only=True,
                        source='departement.region')

    codeRegion      = serializers.StringRelatedField(
                        read_only=True,
                        source='departement.region.code')

    class Meta:
        model  = Commune
        fields = (
            'code',
            'nom',
            'population',
            'codeDepartement',
            'codeRegion',
            'departement',
            'region',
            'codesPostaux')

    def create(self, validated_data):
        cp_toadd = set([ x['code'] for x in validated_data.pop('codepostal_set', []) ])
        instance = super().create(validated_data)

        if cp_toadd:
            instance.setCodesPostaux(cp_toadd, checkExisting=False)
        return instance

    def update(self, instance, validated_data):
        cp_toadd = set([ x['code'] for x in validated_data.pop('codepostal_set', []) ])
        instance = super().update(instance, validated_data)

        # NB update does insert if we change the pk
        # so we have to update related fields after
        instance.setCodesPostaux(cp_toadd)
        return instance