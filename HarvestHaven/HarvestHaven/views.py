from django.http import JsonResponse
from .models import *
from .serializers import *


def tools_list(request):
    tools = Tools.objects.all()
    toolsSerializer = ToolsSerializer(tools, many=True)
    return JsonResponse(toolsSerializer.data, safe=False)

def seeds_list(request):
    seeds = SeedInventory.objects.all()
    seedsSerializer = SeedSerializer(seeds, many=True)
    return JsonResponse(seedsSerializer.data, safe=False)

def inventory_list(request):
    inventory = Inventory.objects.all()
    inventorySerializer = InventorySerializer(inventory, many=True)
    return JsonResponse(inventorySerializer.data, safe=False)

def money_list(request):
    money = Money.objects.all()
    moneySerializer = MoneySerializer(money, many=True)
    return JsonResponse(moneySerializer.data, safe=False)