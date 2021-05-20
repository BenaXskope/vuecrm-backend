from accounting_logic import models
from rest_framework import serializers
from random import shuffle
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'limit'
        )


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Record
        fields = (
            'id',
            'category',
            'amount',
            'type',
            'description',
            'date'
        )