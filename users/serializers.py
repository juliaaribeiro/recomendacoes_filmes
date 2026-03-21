from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'tipo_usuario', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirmPassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['nome', 'email', 'password', 'confirmPassword']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirmPassword'):
            raise serializers.ValidationError({'password': 'As senhas não conferem'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword', None)
        validated_data['tipo_usuario'] = 'user'
        user = User.objects.create_user(**validated_data)
        return user