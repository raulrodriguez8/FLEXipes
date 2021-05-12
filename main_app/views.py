from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests
import json
from .models import User, Ingredient, Meal, Profile
from .forms import IngredientForm, MealForm
from .utils import Calendar
from dotted_dict import DottedDict

import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

API_KEY = env('API_KEY')

# Default Views

def home(request):
    url  = 'https://api.spoonacular.com/food/trivia/random?apiKey='+API_KEY+''
    res = requests.get(url)
    data = json.loads(res.text)
    context = {
        'food_trivia': data['text']
    }
    return render(request, 'home.html', context)

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

#Recipe Views
@login_required
def recipe_results(request):

    pantry_ingredients = User.objects.get(id=request.user.id).profile.pantry.all()
    all_pantry_ingredients = pantry_ingredients.all()
    
    pantry_ingredients_string = ""
    for i in all_pantry_ingredients:
        pantry_ingredients_string = pantry_ingredients_string + i.name + ','
    

    url = 'https://api.spoonacular.com/recipes/findByIngredients?ingredients='+pantry_ingredients_string+'&number=10&ranking=1&ignorePantry=true&apiKey='+API_KEY+''
    
    res = requests.get(url)
    data = json.loads(res.text)

    context = {'data': data}
    return render(request, 'recipes/results.html', context)


def recipe_details(request, recipe_id):
    id = str(recipe_id)
    url = 'https://api.spoonacular.com/recipes/'+id+'/information?includeNutrition=false&apiKey='+API_KEY+''

    res = requests.get(url)
    data = json.loads(res.text)
    print(data)
    meal_form = MealForm()
    # print(data)
    context = {
        'data': data,
        'meal_form'  : meal_form,
        }

    return render(request, 'recipes/details.html', context)

#Ingredients Views
def all_ingredients(request):
    user_ingredients = User.objects.get(id=request.user.id).profile.pantry.all()
    # print(my_ingredients)
    # print(request.user.profile.pantry.all())
    all_ingredients_not_in_user_pantry = Ingredient.objects.exclude(id__in=user_ingredients.values_list('id'))
    # print(all_ingredients_not_in_user_pantry)
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
        request.user.profile.pantry.add(new_ingredient.id)
    return redirect('all_ingredients')

@login_required
def assoc_ingredient(request, ingredient_id):
    User.objects.get(id=request.user.id).profile.pantry.add(ingredient_id)
    # print(User.objects.get(id=request.user.id).profile.pantry.all())
    return redirect('all_ingredients')

@login_required
def remove_ingredient(request, ingredient_id):
    User.objects.get(id=request.user.id).profile.pantry.remove(ingredient_id)
    return redirect('all_ingredients')

class Ingredient_Update(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = ['name', 'aisle']


#Meals Views
@login_required
def add_meal(request, recipe_id):
    id = str(recipe_id)
    user_id=request.user.id
    form = MealForm(request.POST)
    url = 'https://api.spoonacular.com/recipes/'+id+'/information?includeNutrition=false&apiKey=7276efa6287b40cc9b9703a7ed323fb3'
    
    res = requests.get(url)
    data = json.loads(res.text)
    print(data['title'])
    recipe_name = data['title']
    recipe_url = data['spoonacularSourceUrl']  
    
    if form.is_valid():
        new_meal = form.save(commit=False)
        new_meal.recipe_id = recipe_id
        new_meal.user_id = user_id
        new_meal.recipe_name = recipe_name
        new_meal.recipe_url = recipe_url
        new_meal.save()

    context = {
        'recipe_id': recipe_id, 
        'user_id': user_id,
    }

    return render(request, 'meals/calendar.html', context)

@login_required
def all_meals(request):
    meals = Meal.objects.all()
    context = {'meals': meals}
    print(meals)
    return render(request, 'meals/index.html', context)

class Meal_Delete(LoginRequiredMixin, DeleteView):
    model = Meal
    success_url = '/meals/'

class Meal_Update(LoginRequiredMixin, UpdateView):
    model = Meal
    fields = ['date', 'meal', 'recipe_name', 'recipe_url']

#Calendar Views
class CalendarView(LoginRequiredMixin,generic.ListView):
    model = Meal
    template_name = 'meals/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        print(context)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

