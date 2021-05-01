from django.db import models
from django.contrib.auth.models import User

AISLE = (
    ('Spices and Seasonings', 'Spices and Seasonings'),
    ('Pasta and Rice', 'Pasta and Rice'),
    ('Bakery/Bread', 'Bakery/Bread'),
    ('Produce', 'Produce'),
    ('Seafood', 'Seafood'),
    ('Cheese', 'Cheese'),
    ('Dried Fruits', 'Dried Fruits'), 
    ('Nut butters, Jams, and Honey', 'Nut butters, Jams, and Honey'),
    ('Oil, Vinegar, Salad Dressing', 'Oil, Vinegar, Salad Dressing'),
    ('Condiments', 'Condiments'),
    ('Milk, Eggs, Other Dairy', 'Milk, Eggs, Other Dairy'),
    ('Ethnic Foods', 'Ethnic Foods'),
    ('Tea and Coffee', 'Tea and Coffee'),
    ('Refrigerated', 'Refrigerated'),
    ('Canned and Jarred', 'Canned and Jarred'),
    ('Frozen', 'Frozen'),
    ('Alcoholic Beverages', 'Alcoholic Beverages'),
)

MEALS = (
    ('B', 'Breakfast'),
    ('R', 'Brunch'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    aisle = models.CharField(max_length=50, choices=AISLE, default=AISLE[0][0])

    def __str__(self):
        return f"{self.name}: {self.amount}{self.unit}"


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

class Foodie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pantry = models.ManyToManyField(Ingredient)
