from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import Ingredient
from .models import User

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

def all_ingredients(request):
    user_ingredients = User.objects.get(id=request.user.id).profile.pantry.all()
    # print(my_ingredients)
    # print(request.user.profile.pantry.all())
    all_ingredients_not_in_user_pantry = Ingredient.objects.exclude(id__in=user_ingredients.values_list('id'))
    print(all_ingredients_not_in_user_pantry)
    context = {
        'ingredients': all_ingredients_not_in_user_pantry,
        }
    return render(request, 'ingredients/index.html', context)

class Ingredient_Create(LoginRequiredMixin, CreateView):
  model = Ingredient
  fields = ['name', 'aisle']

class Ingredient_Update(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = ['aisle']

class Ingredient_Delete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = '/ingredients/'
