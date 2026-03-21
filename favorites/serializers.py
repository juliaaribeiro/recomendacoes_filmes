from rest_framework import serializers
from .models import Favorito

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = '__all__'
        read_only_fields = ['usuario', 'data']