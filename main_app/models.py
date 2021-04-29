from django.db import models

# Import the User
from django.contrib.auth.models import User

UNITS = (
    ('gm', 'Grams'),
    ('cups', 'Cups'),
    ('items', 'Each'),
    ('oz', 'Ounces'),
    ('Tbsp', 'Tablespoons'),
    ('tsp', 'Teaspoons'),
    ('lbs', 'Pounds'),
    ('gallons', 'Gallon'),
    ('ml', 'Milliliters'),
    ('pint', 'Pint'),
)

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    unit = models.CharField(max_length=7, choices=UNITS, default=UNITS[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.amount}{self.unit}"

MEALS = (
    ('B', 'Breakfast'),
    ('R', 'Brunch'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Meal(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'user_id': self.id})
