from django.db import models

# Import the User
from django.contrib.auth.models import User

# Create your models here.



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