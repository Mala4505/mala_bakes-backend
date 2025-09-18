from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MasterIngredient(models.Model):
    ingredient = models.CharField(max_length=100, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='ingredients')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def cost_per_unit(self):
        if self.qty > 0:
            return round(self.price / self.qty, 2)
        return 0.00

    def __str__(self):
        return f"{self.ingredient} ({self.qty} {self.unit.name} @ {self.price})"

class Recipe(models.Model):
    dish = models.CharField(max_length=100)
    servings = models.IntegerField()

    def __str__(self):
        return self.dish

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(MasterIngredient, on_delete=models.CASCADE)
    qty = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.qty} {self.unit.name} of {self.ingredient.ingredient} for {self.recipe.dish}"
