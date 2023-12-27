from rest_framework import serializers
from .models import Shift
from django import forms
from django.core.exceptions import ValidationError
from .models import GuardRound

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class GuardRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardRound
        fields = '__all__'
        extra_kwargs = {
            'start_date': {'input_formats': ['%d-%m-%Y']},
            'end_date': {'input_formats': ['%d-%m-%Y']}
        }

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date cannot be later than end date.")

        return data
