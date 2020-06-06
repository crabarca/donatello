from rest_framework import serializers
from .models import Deputy, Operational


class DeputySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deputy
        fields = ( 'nombre', 'comuna', 'distrito', 'region', 'partido', 'bancada', 'periodo')


class OperationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operational
