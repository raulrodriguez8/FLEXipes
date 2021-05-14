from django.forms import ModelForm, DateInput
from .models import Ingredient, Meal


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'aisle']

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal']

        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)