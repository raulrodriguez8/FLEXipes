from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
import requests
import json
from .models import Ingredient

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
            # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def recipe_results(request):
    # api_key = 7276efa6287b40cc9b9703a7ed323fb3
    api_ingredients = Ingredient.objects.all()
    print(api_ingredients)
    test_string = api_ingredients.all().values_list('name')
    print(str(test_string))

    url = 'https://api.spoonacular.com/recipes/findByIngredients?ingredients=%s&number=10&ranking=1&ignorePantry=true&apiKey=7276efa6287b40cc9b9703a7ed323fb3' % api_ingredients
    
    res = requests.get(url)
    data = json.loads(res.text)
    context = {'data': data}
    return render(request, 'recipes/results.html', context)

def recipe_details(request, recipe_id):
    print(recipe_id)
    url = 'https://api.spoonacular.com/recipes/%s/information?includeNutrition=false&apiKey=7276efa6287b40cc9b9703a7ed323fb3' % recipe_id

    res = requests.get(url)
    data = json.loads(res.text)
    print(data)
    context = {
        'data': data,
        }

    return render(request, 'recipes/details.html', context)
