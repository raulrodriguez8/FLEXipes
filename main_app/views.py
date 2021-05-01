from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests
import json
from .models import Ingredient
from .models import User
from .forms import IngredientForm

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

def all_ingredients(request):
    user_ingredients = User.objects.get(id=request.user.id).profile.pantry.all()
    # print(my_ingredients)
    # print(request.user.profile.pantry.all())
    all_ingredients_not_in_user_pantry = Ingredient.objects.exclude(id__in=user_ingredients.values_list('id'))
    print(all_ingredients_not_in_user_pantry)
    ingredient_form = IngredientForm()
    context = {
        'ingredients': all_ingredients_not_in_user_pantry,
        'ingredient_form': ingredient_form
        }
    return render(request, 'ingredients/index.html', context)

@login_required
def add_ingredient(request):
    form = IngredientForm(request.POST)
    if form.is_valid():
        new_ingredient = form.save(commit=False)
        new_ingredient.save()
    return redirect('all_ingredients')

class Ingredient_Update(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = ['aisle']

class Ingredient_Delete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = '/ingredients/'


