from django.contrib import admin
from .models import MasterIngredient

@admin.register(MasterIngredient)
class MasterIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'unit', 'qty', 'price', 'cost_per_unit', 'last_updated')
    search_fields = ('ingredient',)
