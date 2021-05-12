from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

AISLE = (
    ('Spices and Seasonings', 'Spices and Seasonings'),
    ('Produce', 'Produce'),
    ('Meat and Sausages', 'Meat and Sausages'),
    ('Poultry', 'Poultry'),
    ('Milk Eggs and Other Dairy', 'Milk Eggs and Other Dairy'),
    ('Seafood', 'Seafood'),    
    ('Bakery and Bread', 'Bakery and Bread'),
    ('Pasta and Rice', 'Pasta and Rice'),
    ('Cheese', 'Cheese'),
    ('Oil Vinegar and Salad Dressing', 'Oil Vinegar and Salad Dressing'),
    ('Dried Fruits', 'Dried Fruits'), 
    ('Nut butters Jams and Honey', 'Nut butters Jams and Honey'),
    ('Ethnic Foods', 'Ethnic Foods'),
    ('Tea and Coffee', 'Tea and Coffee'),
    ('Alcoholic Beverages', 'Alcoholic Beverages'),
    ('Canned and Jarred', 'Canned and Jarred'),
    ('Frozen', 'Frozen'),
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
    aisle = models.CharField(max_length=100, choices=AISLE, default=AISLE[0][0])

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('all_ingredients')

    class Meta:
        ordering = ['-aisle']


class Meal(models.Model):
    date = models.DateTimeField('Planned Meal Date/Time:')
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