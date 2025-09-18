from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'master-ingredients', MasterIngredientViewSet)
router.register(r'units', UnitViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("api/login/", simple_login),
    path('api/meta/', get_meta_data),
    path('api/recipes/<int:recipe_id>/ingredients/', get_recipe_ingredients),
    path('api/recipes/<int:recipe_id>/ingredients/save/', save_recipe_ingredients),
    path('api/recipes/<int:recipe_id>/ingredients/<str:ingredient_name>/delete/', delete_recipe_ingredient),
]
