from rest_framework import serializers
from .models import *

class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ['id', 'name', 'description']

class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedInventory
        fields = ['id', 'name', 'description']

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'name', 'amount']

class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Money
        fields = ['amount']

