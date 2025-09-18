from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import *
from .serializers import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def simple_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        password = data.get("password")

        if password == settings.APP_PASSWORD:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False}, status=401)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MasterIngredientViewSet(viewsets.ModelViewSet):
    queryset = MasterIngredient.objects.all().order_by('-last_updated')
    serializer_class = MasterIngredientSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


@api_view(['GET'])
def get_meta_data(request):
    units = Unit.objects.all()
    ingredients = MasterIngredient.objects.all()

    unit_data = UnitSerializer(units, many=True).data
    ingredient_data = MasterIngredientSerializer(ingredients, many=True).data

    return Response({
        'units': unit_data,
        'ingredients': ingredient_data
    })


@api_view(['GET'])
def get_recipe_ingredients(request, recipe_id):
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    serializer = RecipeIngredientSerializer(ingredients, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def save_recipe_ingredients(request, recipe_id):
    data = request.data.get('ingredients', [])

    for ing in data:
        name = ing.get('ingredient_name')
        qty = ing.get('qty')
        unit_id = ing.get('unit')

        if not name or qty is None or not unit_id:
            continue

        # Get or create the MasterIngredient
        ingredient_obj, _ = MasterIngredient.objects.get_or_create(ingredient=name)

        # Efficient upsert
        RecipeIngredient.objects.update_or_create(
            recipe_id=recipe_id,
            ingredient=ingredient_obj,
            defaults={'qty': qty, 'unit_id': unit_id}
        )

    return Response({'status': 'success'})


@api_view(['DELETE'])
def delete_recipe_ingredient(request, recipe_id, ingredient_name):
    try:
        RecipeIngredient.objects.filter(
            recipe_id=recipe_id,
            ingredient__ingredient=ingredient_name
        ).delete()
        return Response({'status': 'deleted'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
