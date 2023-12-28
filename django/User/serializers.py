from rest_framework import serializers
from .models import User


class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value:
            return value.date()
        return None
    

class UserSerializer(serializers.ModelSerializer):
    birth_date = CustomDateField()
    class Meta:
        model = User
        fields = '__all__'
