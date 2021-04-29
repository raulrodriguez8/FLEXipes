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
    ('gallon', 'Gallon'),
    ('ml', 'Milliliters'),
    ('pint', 'Pint'),
)

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    unit = models.models.CharField(max_length=1, choices=UNITS, default=UNITS[0][0])

    def __str__(self):
        return f"{self.name}: {self.amount}{self.unit}"
