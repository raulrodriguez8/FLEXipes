from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests
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

def recipe_results(request):
    # api_key = 2b13a7c2199445e08d4a4ff0b3f3cf99
    api_ingredients = Ingredient.objects.all()
    print(api_ingredients)
    test_string = api_ingredients.all().values_list('name')
    print(str(test_string))

    url = 'https://api.spoonacular.com/recipes/findByIngredients?ingredients=%s&number=10&apiKey=2b13a7c2199445e08d4a4ff0b3f3cf99' % api_ingredients
    
    response = requests.get(url)
    spoondata = response.json()
    print(spoondata)
    return render(request, 'home.html')

def ingredients(request):
    return render(request, 'ingredients/index.html')