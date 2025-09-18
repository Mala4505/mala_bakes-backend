from rest_framework import serializers
from .models import Unit, MasterIngredient, Recipe, RecipeIngredient

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']

class MasterIngredientSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source='unit.name', read_only=True)

    class Meta:
        model = MasterIngredient
        fields = ['id', 'ingredient', 'unit', 'unit_name', 'price', 'qty', 'last_updated']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.ingredient', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = [
            'id',
            'recipe',
            'ingredient',
            'ingredient_name',
            'qty',
            'unit',
            'unit_name'
        ]

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'dish', 'servings', 'ingredients']
