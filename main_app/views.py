from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests

# Create your views here.

def home(request):
    response = requests.get("https://api.spoonacular.com/recipes/findByIngredients?ingredients=pasta&number=2&apiKey=2b13a7c2199445e08d4a4ff0b3f3cf99")
    spoondata = response.json()
    print(spoondata[0]['title'])
    return render(request, 'home.html', {
        'title': spoondata[0]['title']
    })

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
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
            # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
