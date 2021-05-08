from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

AISLE = (
    ('Spices and Seasonings', 'Spices and Seasonings'),
    ('Pasta and Rice', 'Pasta and Rice'),
    ('Bakery/Bread', 'Bakery/Bread'),
    ('Produce', 'Produce'),
    ('Meat/Sausages', 'Meat/Sausages'),
    ('Poultry', 'Poultry'),
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
    ('B', 'Breakfast',),
    ('R', 'Brunch'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    aisle = models.CharField(max_length=50, choices=AISLE, default=AISLE[0][0])

    def __str__(self):
        return f"{self.name}"


class Meal(models.Model):
    date = models.DateTimeField('Planned Meal Date')
    #meal is a string with 4 choices, starting with 'B', 'Breakfast' as default
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    # #recipe_name will be used to store the name of the recipe pulled back from the API call (if necessary)
    recipe_name = models.CharField(max_length= 300)
    # #recipe_url will be used to store the URL pulled back from the API call (if necessary)
    recipe_url  = models.CharField(max_length= 300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date} is {self.recipe_name}"

    # Add this method
    def get_absolute_url(self):
        return reverse('all_meals', kwargs={'meal_id': self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pantry = models.ManyToManyField(Ingredient)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()