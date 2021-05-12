from django.forms import ModelForm
from .models import Ingredient, Meal


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'aisle']

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal', 'recipe_name', 'recipe_url']