from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('results/', views.recipe_results, name='recipe_results'),
    path('ingredients/', views.all_ingredients, name='all_ingredients'),
    path('ingredients/create/', views.add_ingredient, name='ingredient_create'),
    path('ingredients/<int:pk>/update/', views.Ingredient_Update.as_view(), name='ingredient_update'),
    path('ingredients/<int:pk>/delete/', views.Ingredient_Delete.as_view(), name='ingredient_delete'),   
]