from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('results/page/<int:page>', views.recipe_results, name='recipe_results'),
    path('ingredients/', views.all_ingredients, name='all_ingredients'),
    path('ingredients/create/', views.add_ingredient, name='ingredient_create'),
    path('ingredients/associate/<int:ingredient_id>/', views.assoc_ingredient, name='assoc_ingredient'), 
    path('ingredients/remove/<int:ingredient_id>/', views.remove_ingredient, name='remove_ingredient'),
    path('ingredients/<int:pk>/update/', views.Ingredient_Update.as_view(), name='ingredient_update'), 
    path('results/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('results/<int:recipe_id>/add/', views.add_meal, name='add_meal'),
    path('meals/', views.all_meals, name='all_meals'),
]